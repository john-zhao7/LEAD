from __future__ import annotations

from lead.types import Confound, ExperimentRun


def detect_confounds(runs: list[ExperimentRun]) -> list[Confound]:
    confounds: list[Confound] = []
    if len(runs) < 2:
        return confounds
    run_ids = [r.run_id for r in runs]
    seeds = {r.config.values.get("seed") for r in runs if r.config}
    if len(seeds) > 1:
        confounds.append(Confound(run_ids=run_ids, name="seed_mismatch", description="Runs use different random seeds", severity=0.6))
    budgets = {r.config.values.get("train_steps") for r in runs if r.config}
    if len(budgets) > 1:
        confounds.append(Confound(run_ids=run_ids, name="budget_mismatch", description="Training budgets differ across compared runs", severity=0.8))
    dirty = [r.run_id for r in runs if r.git and r.git.dirty]
    if dirty:
        confounds.append(Confound(run_ids=dirty, name="dirty_git_state", description="One or more runs were executed with dirty git state", severity=0.7))
    branches = {r.git.branch for r in runs if r.git and r.git.branch}
    if len(branches) > 1:
        confounds.append(Confound(run_ids=run_ids, name="branch_mismatch", description="Runs come from different git branches", severity=0.7))
    return confounds
