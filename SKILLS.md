# BioX Selected Sales Skills

This workspace intentionally uses a focused subset of the upstream Sales-Skills library plus one SaaS pricing-strategy skill.

## Prospecting and account intelligence
- ideal-customer-profile-matching
- prospect-research-integration
- decision-maker-identification
- trigger-event-detection
- outbound-prospecting
- social-selling
- personalization-at-scale
- qualifying-leads

## Messaging and writing
- written-communication
- copywriting
- copy-editing
- storytelling
- tone-matching
- response-length-calibration
- email-sequence
- dynamic-script-generation

## Human and emotional selling
- active-listening
- empathy
- building-rapport
- asking-effective-questions
- adaptability
- sentiment-analysis
- negative-sentiment-de-escalation
- conversation-pause-intelligence

## Conversion and revenue execution
- discovery
- objection-handling
- follow-up-discipline
- meeting-conversion
- pipeline-management
- pricing-negotiation
- negotiation
- closing
- ghost-recovery-sequences
- customer-referrals
- micro-commitment-stacking
- multi-stakeholder-thread-management

## Pricing strategy
- pricing-strategy — SaaS/digital-product pricing models, value metrics, tiering, enterprise pricing, competitive positioning, and rollout planning. Source: mohitagw15856/pm-claude-skills.

## Installation
For Codex, run `bash scripts/install-codex-skills.sh` from the repository root.

Keep upstream skill behavior subordinate to the BioX-native rules in `skills/biox-*` and the revenue logic defined in this repository. In particular, use `pricing-strategy` as a framework for pricing decisions, while `biox-revenue-operator` governs BioX revenue targets and commercial priorities.
