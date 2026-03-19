"""Optional instrumentation stubs.

These hooks are intentionally minimal and opt-in.
They must not be required by passive mode.
"""

from __future__ import annotations


def collect_grad_norms(model) -> dict[str, float]:
    stats = {}
    for name, p in model.named_parameters():
        if p.grad is not None:
            stats[name] = float(p.grad.data.norm().item())
    return stats
