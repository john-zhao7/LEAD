---
name: lead
description: Automated experiment forensics and diagnosis for ML and robot-learning runs. Use when the user asks to inspect failed/noisy/partial runs, reconstruct timelines, audit comparability/confounds, rank evidence-weighted causal hypotheses, and generate structured post-mortems with next-experiment recommendations.
---

# LEAD Skill

## Purpose
Use LEAD to replace vibe-based debugging with structured experiment diagnosis.

## Workflow (must follow)
1. Build artifact inventory and list missing artifacts.
2. Ingest available artifacts only (passive mode by default).
3. Reconstruct timeline and anomaly onset windows.
4. Diagnose single-run pathologies.
5. Audit comparability before cross-run synthesis.
6. Rank hypotheses with explicit evidence tiers.
7. Generate structured 12-section post-mortem.
8. Propose confirmatory, falsification, and cheap salvage experiments.

## Guardrails
- Never overclaim causality.
- Separate observations from hypotheses.
- Mark each major claim as direct_evidence / strong_inference / weak_hypothesis.
- If artifacts are missing, explicitly state diagnosis limitations.

## Prompt files
- `prompts/build_artifact_inventory.md`
- `prompts/align_timeline.md`
- `prompts/audit_comparability.md`
- `prompts/diagnose_pathologies.md`
- `prompts/synthesize_hypotheses.md`
- `prompts/write_postmortem.md`

## Scripts
- `scripts/init_session.py`
- `scripts/inspect_artifacts.py`
- `scripts/run_diagnosis.py`
- `scripts/compare_experiments.py`
- `scripts/generate_postmortem.py`
- `scripts/export_report.py`
