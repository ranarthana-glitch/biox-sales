#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
DEST="$CODEX_HOME/skills"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$DEST"

UPSTREAM_SKILLS=(
  ideal-customer-profile-matching
  prospect-research-integration
  decision-maker-identification
  trigger-event-detection
  outbound-prospecting
  social-selling
  personalization-at-scale
  qualifying-leads
  written-communication
  copywriting
  copy-editing
  storytelling
  tone-matching
  response-length-calibration
  email-sequence
  dynamic-script-generation
  active-listening
  empathy
  building-rapport
  asking-effective-questions
  adaptability
  sentiment-analysis
  negative-sentiment-de-escalation
  conversation-pause-intelligence
  discovery
  objection-handling
  follow-up-discipline
  meeting-conversion
  pipeline-management
  pricing-negotiation
  negotiation
  closing
  ghost-recovery-sequences
  customer-referrals
  micro-commitment-stacking
  multi-stakeholder-thread-management
)

echo "Cloning selected upstream sales skills..."
git clone --depth 1 https://github.com/louisblythe/Sales-Skills.git "$TMP/sales-skills" >/dev/null 2>&1

echo "Cloning pricing strategy skill..."
git clone --depth 1 https://github.com/mohitagw15856/pm-claude-skills.git "$TMP/pm-skills" >/dev/null 2>&1

install_dir() {
  local src="$1"
  local name="$2"
  local dst="$DEST/$name"
  if [[ -e "$dst" ]]; then
    echo "skip: $name already exists at $dst"
    return
  fi
  cp -R "$src" "$dst"
  echo "installed: $name"
}

for skill in "${UPSTREAM_SKILLS[@]}"; do
  src="$TMP/sales-skills/skills/$skill"
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "ERROR: upstream skill missing: $skill" >&2
    exit 1
  fi
  install_dir "$src" "$skill"
done

PRICING_SRC="$TMP/pm-skills/skills/pricing-strategy"
if [[ ! -f "$PRICING_SRC/SKILL.md" ]]; then
  echo "ERROR: pricing-strategy skill missing" >&2
  exit 1
fi
install_dir "$PRICING_SRC" "pricing-strategy"

install_biox_skill() {
  local name="$1"
  local description="$2"
  local src="$ROOT/skills/$name/SKILL.md"
  local dst="$DEST/$name"

  if [[ -e "$dst" ]]; then
    echo "skip: $name already exists at $dst"
    return
  fi
  if [[ ! -f "$src" ]]; then
    echo "ERROR: BioX skill missing: $src" >&2
    exit 1
  fi

  mkdir -p "$dst"
  if [[ "$(head -n 1 "$src")" == "---" ]]; then
    cp "$src" "$dst/SKILL.md"
  else
    {
      echo "---"
      echo "name: $name"
      printf 'description: "%s"\n' "$description"
      echo "---"
      echo
      cat "$src"
    } > "$dst/SKILL.md"
  fi
  echo "installed: $name"
}

install_biox_skill "biox-icp" "Select, score, prioritize, and disqualify BioX enterprise accounts and buyer personas using emissions intensity, carbon regulation, data complexity, buyer accessibility, commercial capacity, and timing signals."
install_biox_skill "biox-enterprise-messaging" "Create credible BioX enterprise outreach and positioning around carbon accounting, CCTS, CBAM, MRV, decarbonization, targets, and environmental assets without generic sales language or unsupported claims."
install_biox_skill "biox-pilot-conversion" "Move qualified BioX accounts from discovery through tailored demo, data scoping, measurable paid pilot or LOI, and enterprise contract with explicit owners, success criteria, and next steps."
install_biox_skill "biox-writing-voice" "Write BioX LinkedIn messages, emails, follow-ups, proposals, posts, scripts, and sales collateral in a concise, intelligent, technically credible, warm, non-pushy voice with emotional calibration."
install_biox_skill "biox-revenue-operator" "Run BioX sales planning from the founder-set $3T-by-2035 strategic value ambition down to current milestones, revenue gaps, qualified pipeline, funnel constraints, and the highest-value commercial action today."

echo
echo "Installed BioX Codex skill set into: $DEST"
echo "Restart Codex so it reloads the new skills."
