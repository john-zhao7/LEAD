# LEAD — Learning Experiment Automated Diagnostics

LEAD is an **experiment forensics and diagnosis engine** for ML and robot-learning workflows.

It is built to answer: _what likely went wrong, what evidence supports that claim, what is still uncertain, and what should we try next?_

## Why LEAD is different

LEAD is not:
- an auto-tuner
- a dashboard clone
- a log-only summarizer

LEAD is:
- evidence-weighted and uncertainty-aware
- confound-aware before ablation synthesis
- robust to partial/messy artifacts
- robot-learning specialized (action saturation, reward gaming, rollout pathologies)

## Core workflow (MVP)

1. Artifact inventory (present + missing + quality)
2. Ingestion and normalization
3. Timeline reconstruction
4. Single-run anomaly diagnostics
5. Cross-run comparability/confound audit
6. Evidence-tiered hypothesis ranking
7. Structured post-mortem generation (JSON + Markdown)

## Install

```bash
cd skills/LEAD
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## CLI

```bash
lead init --project ./my_exp --session-id exp-2026-03-19
lead inspect --run-dir ./my_exp/run_001
lead diagnose-run --run-dir ./my_exp/run_001 --out reports/run_001.json
lead compare-runs --run-dirs ./my_exp/run_a ./my_exp/run_b --out reports/compare.json
lead postmortem --run-dirs ./my_exp/run_a ./my_exp/run_b --out reports/postmortem.json --md-out reports/postmortem.md
lead export-report --input reports/postmortem.json --format md --out reports/postmortem_export.md
```

## Supported artifacts (MVP)

- `metrics.jsonl` (canonical local metric log)
- `wandb_history.csv` (offline export)
- `stdout.log`, `stderr.log`
- `config.yaml` / `config.yml`
- `git_meta.json` (or git metadata from repo)

## Passive vs Instrumented mode

### Passive mode
Use existing artifacts only. Works on failed/crashed/partial runs.

### Instrumented mode (optional hooks)
Provides richer signals when available:
- per-layer grad norms
- update/weight ratios
- activation sparsity
- dead-neuron proxies
- effective rank proxies
- NaN/Inf stats

See `lead/integrations/pytorch_hooks.py` and `lead/integrations/lightning_hooks.py`.

## Output structure (fixed)

LEAD post-mortem sections:
1. Experiment Overview
2. Available Artifacts and Data Quality
3. Timeline of Key Events
4. Observed Anomalies
5. Failure Signatures / Health Findings
6. Comparability and Confound Assessment
7. Ranked Causal Hypotheses
8. Evidence Table
9. What is Well Supported vs Uncertain
10. Recommended Next Experiments
11. Limitations of Current Diagnosis
12. Final Confidence Summary

## Example cases included

- `tests/fixtures/single_run/` instability + stderr warnings
- `tests/fixtures/multi_run/` apparent win with hidden confound
- `tests/fixtures/robot_learning_case/` reward up but suspicious action saturation

Also see `examples/*` for sample outputs.

## Roadmap (deferred)

- checkpoint deep introspection
- richer TensorBoard native event parsing
- optional visualization module
- online integrations and distributed orchestration

## Honesty policy

LEAD separates:
- **direct_evidence**
- **strong_inference**
- **weak_hypothesis**

It does not present correlation as guaranteed causality.
