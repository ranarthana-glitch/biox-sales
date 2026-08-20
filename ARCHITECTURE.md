# BioX Autonomous Revenue OS Architecture

## Assessment basis
The existing repo has strong sales doctrine, funnel logic, BioX-native skills and a focused upstream skill library. The major gap is execution architecture: persistent state, orchestration, specialist agents, action governance, forecasting and learning.

This design upgrades rather than replaces the existing skills.

## System loop

`Targets → Commercial State → Revenue Orchestrator → Specialist Agents → Action Queue → Approval Policy → Tools/Execution → Outcomes → Learning → Updated State`

## Layers

### 1. Skills
Reusable methods: ICP, research, messaging, discovery, pilot conversion, pricing, negotiation, writing voice, etc.

### 2. Agents
Role-specific workers:
- revenue-orchestrator
- account-intelligence
- prospecting
- conversation
- meeting-intelligence
- deal-strategy
- pilot-management
- forecasting
- learning

### 3. Orchestrator
Owns the commercial objective and selects work. Specialist agents cannot independently optimize vanity metrics.

Inputs:
- current revenue/flow targets
- actual revenue/flow
- pipeline/opportunities
- funnel conversion rates
- sales-cycle data
- account/contact coverage
- activity and outcome history

Outputs:
- diagnosed constraint
- ranked opportunities
- ranked next-best actions
- expected value/confidence
- required approvals

### 4. Memory / system of record
Persistent commercial data should ultimately live in a database/CRM rather than Markdown files. Repo schemas define the contract; the runtime database stores the state.

### 5. Tools
External action adapters may include web research, CRM/database, email, calendar, permitted social/browser automation, meeting transcripts and document generation.

### 6. Governance
All actions pass through autonomy, evidence and approval policies.

### 7. Observability and learning
Record recommendations/actions/outcomes so agent performance and commercial signals can be measured.

## Dual north stars

### Revenue Engine
Near-term survival/growth: ARR, contracted revenue, paid pilots, pipeline, conversion, sales velocity.

### Flow Engine
Long-term strategic scale: capital facilitated, environmental assets transacted, projects originated, capital deployed, annual/cumulative flow. Founder-set objective: $3T facilitated by 2035.

Do not substitute speculative flow estimates for actual revenue during the current enterprise SaaS stage.

## Build sequence

### Phase 1 — Executable brain
Implement Revenue Orchestrator + schemas + deterministic constraint diagnosis + ranked next-best actions.

### Phase 2 — Persistent memory
Connect a database/CRM and interaction history. The agent must know what happened yesterday without relying on chat context.

### Phase 3 — Tools
Connect research, email, calendar, CRM, permitted social/browser workflows, meeting inputs and document generation.

### Phase 4 — Meeting intelligence
Calls update opportunity state, forecast, stakeholder map, objections, commitments and next action.

### Phase 5 — Flow intelligence
Introduce evidenced Expected Flow Value and expand ICP coverage into capital providers, originators and intermediaries when strategically appropriate.

### Phase 6 — Learning loop
Connect recommendation → human/agent action → customer outcome → revenue/flow outcome and update scoring/playbooks from sufficient evidence.

## Proposed repository structure

```text
biox-sales/
├── AGENTS.md
├── ARCHITECTURE.md
├── README.md
├── SKILLS.md
├── skills/
├── agents/
│   ├── revenue-orchestrator/
│   ├── account-intelligence/
│   ├── prospecting/
│   ├── conversation/
│   ├── meeting-intelligence/
│   ├── deal-strategy/
│   ├── pilot-management/
│   ├── forecasting/
│   └── learning/
├── schemas/
├── policies/
├── workflows/
├── analytics/
├── runtime/
│   ├── orchestrator/
│   ├── scheduler/
│   ├── memory/
│   ├── tools/
│   └── observability/
└── scripts/
```

## Important constraint
Do not install every available sales skill. Keep a focused library and retrieve capabilities on demand. Add a new skill when a measured bottleneck requires it.