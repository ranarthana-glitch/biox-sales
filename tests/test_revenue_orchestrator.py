import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "runtime" / "orchestrator" / "revenue_orchestrator.py"
spec = importlib.util.spec_from_file_location("revenue_orchestrator", MODULE)
ro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ro)


def test_expected_flow_value_requires_inputs():
    assert ro.expected_flow_value({"probability": 0.2}) is None
    assert ro.expected_flow_value({
        "probability": 0.2,
        "expected_annual_facilitated_flow": 1000,
        "expected_relationship_years": 5,
    }) == 1000


def test_pipeline_gap_is_first_constraint_when_target_exists():
    state = {
        "targets": {"revenue_target": 100, "qualified_pipeline_target": 400},
        "actuals": {"revenue": 0},
        "funnel_metrics": {"qualified_pipeline": 100},
        "accounts": [],
        "opportunities": [],
    }
    diagnosis = ro.diagnose(state)
    assert diagnosis.constraint == "insufficient_qualified_pipeline"


def test_buyer_coverage_becomes_constraint_after_pipeline_is_adequate():
    state = {
        "targets": {"revenue_target": 100, "qualified_pipeline_target": 100},
        "actuals": {"revenue": 0},
        "funnel_metrics": {
            "qualified_pipeline": 120,
            "priority_accounts": 10,
            "accounts_with_senior_buyer": 3,
        },
        "accounts": [{}] * 10,
        "opportunities": [],
    }
    diagnosis = ro.diagnose(state)
    assert diagnosis.constraint == "weak_senior_buyer_coverage"


def test_active_opportunities_are_ranked_and_do_not_include_lost():
    state = {
        "targets": {"qualified_pipeline_target": 0},
        "actuals": {},
        "funnel_metrics": {},
        "accounts": [],
        "opportunities": [
            {"id": "a", "account": "A", "stage": "discovery", "plausible_deal_value": 1000, "probability": 0.3, "confidence": 0.8},
            {"id": "b", "account": "B", "stage": "lost", "plausible_deal_value": 100000, "probability": 0.9},
        ],
    }
    report = ro.build_report(state)
    assert [a["opportunity_id"] for a in report["highest_value_actions"]] == ["a"]


def test_example_state_runs():
    state = json.loads((ROOT / "data" / "example_state.json").read_text())
    report = ro.build_report(state)
    assert report["current_milestone"] == "first paid enterprise pilot"
    assert report["highest_value_actions"]
