from __future__ import annotations


def lightning_batch_hook(batch_idx: int, loss_value: float) -> dict[str, float]:
    return {"batch_idx": float(batch_idx), "loss": float(loss_value)}
