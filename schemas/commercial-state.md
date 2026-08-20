# Commercial State Contracts

These are logical contracts for the future persistent database/CRM. Unknown values must remain unknown; do not fabricate completeness.

## Account
```yaml
id:
organization:
icp_layer: enterprise | capital_provider | originator | intermediary
sector:
geography:
icp_score:
strategic_account_value:
triggers: []
key_people: []
estimated_annual_flow:
flow_estimate_basis:
confidence:
last_researched_at:
```

## Contact
```yaml
id:
account_id:
name:
title:
role_type: economic_buyer | champion | influencer | blocker | unknown
influence:
sentiment:
communication_history: []
source:
last_verified_at:
```

## Opportunity
```yaml
id:
account_id:
stage:
pain:
trigger:
economic_buyer_id:
champion_id:
stakeholders: []
plausible_deal_value:
probability:
expected_annual_facilitated_flow:
expected_relationship_years:
expected_flow_value:
flow_assumptions: []
confidence:
decision_criteria:
decision_process:
timeline:
competition:
next_best_action:
next_action_date:
```

## Next Best Action
```yaml
action:
why:
evidence: []
expected_revenue_impact:
expected_flow_value:
confidence:
urgency:
owner: agent | human
approval_required:
deadline:
status:
```

## Pilot
```yaml
id:
opportunity_id:
status:
biox_owner:
customer_owner:
scope:
dataset:
success_metric:
baseline:
target:
start_date:
end_date:
commercial_value:
price:
conversion_condition:
conversion_probability:
next_action:
next_action_date:
```

## Interaction
```yaml
id:
account_id:
contact_id:
opportunity_id:
type: email | linkedin | call | meeting | response | other
occurred_at:
summary:
sentiment:
buying_signals: []
objections: []
commitments: []
evidence_ref:
```

## Agent Action
```yaml
id:
timestamp:
agent:
account_id:
opportunity_id:
action:
reason:
evidence: []
expected_revenue_impact:
expected_flow_value:
confidence:
approval_required:
approval_status:
approved_by:
outcome:
```

## Target
```yaml
period:
revenue_target:
arr_target:
contracted_revenue_target:
qualified_pipeline_target:
flow_target:
cumulative_flow_target:
notes:
```

## Expected Flow Value
`EFV = probability × expected_annual_BioX_facilitated_flow × expected_relationship_years`

Only calculate when all three components have a supportable basis. Store assumptions and confidence next to the number.