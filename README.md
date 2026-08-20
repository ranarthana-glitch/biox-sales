# BioX Revenue Operating System

Purpose-built AI-assisted commercial operating system for BioX.

## North Stars

### BioX Revenue
Near-term operating engine: contracted revenue, ARR, paid pilots, qualified/weighted pipeline, conversion rates and sales velocity.

### BioX Flow
Founder-set long-term strategic objective: **facilitate $3 trillion of climate/economic flows by 2035**. Track capital facilitated, environmental assets transacted, projects originated, capital deployed, annual flow and cumulative flow. This is not a $3T SaaS-revenue forecast.

## Operating principle
Work backwards:

2035 strategic objective → current commercial milestone → revenue/flow target → qualified pipeline → active opportunities → current funnel constraint → ranked next-best actions → approved execution → outcomes → learning.

Optimize for **qualified conversations, pilots, contracts, revenue and eventually evidenced Expected Flow Value**, not vanity activity metrics.

## Immediate commercial gates
1. First qualified enterprise discovery
2. First enterprise pilot
3. First paid pilot
4. Repeatable pilot-to-contract motion
5. ₹10L cumulative contracted BioX revenue
6. ₹1Cr ARR
7. ₹10Cr ARR
8. Recalculate later targets from observed pricing, win rates, sales cycles, retention, expansion and delivery capacity

## Phase 1 runtime
The repo now contains an executable deterministic Revenue Orchestrator at:

`runtime/orchestrator/revenue_orchestrator.py`

It consumes a JSON snapshot of BioX commercial state and outputs:
- current funnel constraint
- evidence for the diagnosis
- qualified and weighted pipeline
- pipeline coverage when target data exists
- ranked next-best actions
- expected revenue impact
- Expected Flow Value only when supportable inputs exist
- confidence, action owner and approval requirement
- what not to spend time on today

Run the example:

```bash
bash scripts/run-revenue-os.sh
```

Run with your own state file:

```bash
bash scripts/run-revenue-os.sh path/to/your-state.json
```

Machine-readable output:

```bash
python3 runtime/orchestrator/revenue_orchestrator.py path/to/your-state.json --json
```

The file `data/example_state.json` is illustrative only. Replace its values with verified live pipeline data before using the output commercially.

## Tests

```bash
python3 -m pytest -q
```

## Governing question
**Given BioX's current revenue/flow target, commercial state and funnel constraint, what actions have the highest expected commercial impact now?**

A connection request is not pipeline. A friendly reply is not an opportunity. Assign pipeline value only when there is a credible buyer/problem/use-case, commercial next step and plausible deal value.

See `AGENTS.md` for governance, `ARCHITECTURE.md` for the system design, `schemas/commercial-state.md` for persistent-state contracts, and `policies/autonomy.md` for approval boundaries.
