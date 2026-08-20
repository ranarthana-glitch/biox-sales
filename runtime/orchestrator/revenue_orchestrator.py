#!/usr/bin/env python3
"""BioX Phase 1 Revenue Orchestrator.

Pure-stdlib executable brain for constraint diagnosis and next-best-action ranking.
Persistent database integration comes in Phase 2; this version reads JSON state.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


STAGE_WEIGHTS = {
    "prospect": 0.05,
    "connected": 0.08,
    "conversation": 0.12,
    "qualified": 0.20,
    "discovery": 0.30,
    "demo": 0.40,
    "pilot_scoping": 0.50,
    "pilot_proposed": 0.60,
    "pilot": 0.70,
    "loi": 0.80,
    "contracting": 0.90,
    "won": 1.00,
    "lost": 0.00,
}


@dataclass
class Diagnosis:
    constraint: str
    reason: str
    severity: float


def num(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def ratio(numerator: float, denominator: float) -> Optional[float]:
    if denominator <= 0:
        return None
    return numerator / denominator


def opportunity_probability(opp: Dict[str, Any]) -> float:
    if opp.get("probability") is not None:
        p = num(opp.get("probability"))
        return max(0.0, min(1.0, p))
    return STAGE_WEIGHTS.get(str(opp.get("stage", "prospect")), 0.05)


def expected_flow_value(opp: Dict[str, Any]) -> Optional[float]:
    annual = opp.get("expected_annual_facilitated_flow")
    years = opp.get("expected_relationship_years")
    if annual is None or years is None:
        return None
    return opportunity_probability(opp) * num(annual) * num(years)


def qualified_pipeline(opportunities: List[Dict[str, Any]]) -> float:
    qualifying = {"qualified", "discovery", "demo", "pilot_scoping", "pilot_proposed", "pilot", "loi", "contracting", "won"}
    return sum(num(o.get("plausible_deal_value")) for o in opportunities if o.get("stage") in qualifying)


def weighted_pipeline(opportunities: List[Dict[str, Any]]) -> float:
    return sum(num(o.get("plausible_deal_value")) * opportunity_probability(o) for o in opportunities if o.get("stage") != "lost")


def diagnose(state: Dict[str, Any]) -> Diagnosis:
    targets = state.get("targets", {})
    metrics = state.get("funnel_metrics", {})
    opportunities = state.get("opportunities", [])
    accounts = state.get("accounts", [])

    revenue_target = num(targets.get("contracted_revenue_target") or targets.get("revenue_target"))
    revenue_actual = num(state.get("actuals", {}).get("contracted_revenue") or state.get("actuals", {}).get("revenue"))
    qpipe_target = num(targets.get("qualified_pipeline_target"))
    qpipe = num(metrics.get("qualified_pipeline"), qualified_pipeline(opportunities))

    if revenue_target > revenue_actual and qpipe_target > 0 and qpipe < qpipe_target:
        gap = qpipe_target - qpipe
        return Diagnosis("insufficient_qualified_pipeline", f"Qualified pipeline is {qpipe:.0f} against target {qpipe_target:.0f}; gap {gap:.0f}.", min(1.0, gap / qpipe_target))

    senior_coverage = ratio(num(metrics.get("accounts_with_senior_buyer")), num(metrics.get("priority_accounts"), len(accounts)))
    if senior_coverage is not None and senior_coverage < 0.70:
        return Diagnosis("weak_senior_buyer_coverage", f"Only {senior_coverage:.0%} of priority accounts have a verified senior buyer mapped.", 1 - senior_coverage)

    reply_rate = metrics.get("reply_rate")
    if reply_rate is not None and num(reply_rate) < num(metrics.get("reply_rate_floor"), 0.08):
        return Diagnosis("weak_reply_rate", f"Reply rate is {num(reply_rate):.1%}; targeting/message fit is the likely constraint.", 0.75)

    meeting_conversion = metrics.get("conversation_to_meeting_rate")
    if meeting_conversion is not None and num(meeting_conversion) < num(metrics.get("conversation_to_meeting_floor"), 0.20):
        return Diagnosis("weak_meeting_conversion", f"Conversation-to-meeting conversion is {num(meeting_conversion):.1%}.", 0.70)

    pilot_conversion = metrics.get("meeting_to_pilot_rate")
    if pilot_conversion is not None and num(pilot_conversion) < num(metrics.get("meeting_to_pilot_floor"), 0.15):
        return Diagnosis("weak_pilot_conversion", f"Meeting-to-pilot conversion is {num(pilot_conversion):.1%}.", 0.70)

    close_rate = metrics.get("pilot_to_contract_rate")
    if close_rate is not None and num(close_rate) < num(metrics.get("pilot_to_contract_floor"), 0.30):
        return Diagnosis("weak_pilot_close", f"Pilot-to-contract conversion is {num(close_rate):.1%}.", 0.75)

    stale = [o for o in opportunities if o.get("stale") and o.get("stage") not in {"lost", "won"}]
    if stale:
        return Diagnosis("stale_opportunities", f"{len(stale)} active opportunities are stale and should be advanced or disqualified.", 0.60)

    return Diagnosis("advance_best_active_opportunities", "No stronger downstream constraint is evidenced; prioritize the highest-value active opportunities.", 0.40)


def next_action_for(opp: Dict[str, Any], constraint: str) -> str:
    stage = str(opp.get("stage", "prospect"))
    if constraint == "weak_senior_buyer_coverage" or not opp.get("economic_buyer"):
        return "Map and secure access to the senior economic buyer"
    if constraint == "weak_reply_rate" and stage in {"prospect", "connected"}:
        return "Rework outreach around a verified regulatory/operational trigger before sending"
    if constraint == "weak_meeting_conversion" and stage in {"conversation", "qualified"}:
        return "Use a low-friction discovery CTA tied to the buyer's specific carbon workflow"
    if constraint == "weak_pilot_conversion" and stage in {"discovery", "demo", "qualified"}:
        return "Define a narrow paid pilot with dataset, success metric, owner and conversion condition"
    if constraint == "weak_pilot_close" and stage in {"pilot", "pilot_proposed", "loi", "contracting"}:
        return "Resolve the dominant commercial blocker: ROI, procurement, authority, pricing or implementation risk"
    if opp.get("stale"):
        return "Reactivate with a specific decision-oriented next step or disqualify"
    return str(opp.get("next_action") or "Advance to the next explicit commercial commitment")


def score_opportunity(opp: Dict[str, Any], constraint: str) -> float:
    deal = num(opp.get("plausible_deal_value"))
    probability = opportunity_probability(opp)
    strategic = num(opp.get("strategic_account_value"), 0.5)
    urgency = num(opp.get("urgency_score"), 0.5)
    confidence = num(opp.get("confidence"), 0.5)
    stale_bonus = 0.12 if opp.get("stale") else 0.0
    stage_bonus = probability * 0.35
    revenue_signal = min(1.0, deal / max(1.0, num(opp.get("normalization_deal_value"), 1_000_000)))
    score = 0.35 * revenue_signal + stage_bonus + 0.10 * strategic + 0.10 * urgency + 0.10 * confidence + stale_bonus
    if constraint == "weak_senior_buyer_coverage" and not opp.get("economic_buyer"):
        score += 0.15
    return score


def rank_actions(state: Dict[str, Any], diagnosis: Diagnosis, limit: int = 5) -> List[Dict[str, Any]]:
    actions: List[Dict[str, Any]] = []
    for opp in state.get("opportunities", []):
        if opp.get("stage") in {"won", "lost"}:
            continue
        efv = expected_flow_value(opp)
        actions.append({
            "account": opp.get("account") or opp.get("account_id") or "Unknown account",
            "opportunity_id": opp.get("id"),
            "stage": opp.get("stage", "prospect"),
            "action": next_action_for(opp, diagnosis.constraint),
            "why_now": opp.get("pain") or opp.get("trigger") or diagnosis.reason,
            "expected_revenue_impact": num(opp.get("plausible_deal_value")) * opportunity_probability(opp),
            "expected_flow_value": efv,
            "confidence": num(opp.get("confidence"), 0.5),
            "owner": "human" if opp.get("stage") in {"pilot_proposed", "pilot", "loi", "contracting"} else "agent+human",
            "approval_required": True,
            "deadline": opp.get("next_action_date"),
            "score": score_opportunity(opp, diagnosis.constraint),
        })
    actions.sort(key=lambda x: x["score"], reverse=True)
    return actions[:limit]


def build_report(state: Dict[str, Any]) -> Dict[str, Any]:
    opps = state.get("opportunities", [])
    diag = diagnose(state)
    metrics = state.setdefault("funnel_metrics", {})
    metrics.setdefault("qualified_pipeline", qualified_pipeline(opps))
    metrics.setdefault("weighted_pipeline", weighted_pipeline(opps))
    target = state.get("targets", {})
    qpt = num(target.get("qualified_pipeline_target"))
    coverage = ratio(num(metrics.get("qualified_pipeline")), qpt)

    return {
        "current_milestone": target.get("current_milestone", "first paid enterprise pilot"),
        "constraint": diag.constraint,
        "constraint_reason": diag.reason,
        "constraint_severity": round(diag.severity, 3),
        "qualified_pipeline": metrics.get("qualified_pipeline"),
        "weighted_pipeline": metrics.get("weighted_pipeline"),
        "pipeline_coverage": coverage,
        "highest_value_actions": rank_actions(state, diag),
        "what_not_to_do": "Do not add more top-of-funnel volume unless the diagnosed constraint is insufficient qualified pipeline or buyer coverage.",
        "data_warnings": state.get("data_warnings", []),
    }


def render_text(report: Dict[str, Any]) -> str:
    lines = [
        "BioX Revenue OS — Today",
        f"Current milestone: {report['current_milestone']}",
        f"Current constraint: {report['constraint']}",
        f"Evidence: {report['constraint_reason']}",
        f"Qualified pipeline: {report['qualified_pipeline']:.0f}",
        f"Weighted pipeline: {report['weighted_pipeline']:.0f}",
    ]
    if report.get("pipeline_coverage") is not None:
        lines.append(f"Pipeline coverage: {report['pipeline_coverage']:.2f}x")
    lines.append("\nHighest-value actions:")
    for i, action in enumerate(report["highest_value_actions"], 1):
        efv = action.get("expected_flow_value")
        lines.extend([
            f"{i}. {action['account']} — {action['action']}",
            f"   Why now: {action['why_now']}",
            f"   Expected revenue impact: {action['expected_revenue_impact']:.0f}",
            f"   EFV: {'unknown' if efv is None else f'{efv:.0f}'}",
            f"   Confidence: {action['confidence']:.0%}",
            f"   Owner: {action['owner']} | Approval required: {action['approval_required']}",
        ])
    lines.append(f"\nWhat not to do today: {report['what_not_to_do']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the BioX Phase 1 Revenue Orchestrator")
    parser.add_argument("state", type=Path, help="Path to commercial-state JSON")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output machine-readable JSON")
    args = parser.parse_args()

    state = json.loads(args.state.read_text(encoding="utf-8"))
    report = build_report(state)
    print(json.dumps(report, indent=2) if args.as_json else render_text(report))


if __name__ == "__main__":
    main()
