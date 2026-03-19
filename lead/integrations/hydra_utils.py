from __future__ import annotations


def flatten_hydra_config(cfg: dict) -> dict:
    """MVP helper to normalize nested Hydra configs."""
    out = {}
    def rec(prefix, obj):
        if isinstance(obj, dict):
            for k,v in obj.items():
                rec(f"{prefix}.{k}" if prefix else k, v)
        else:
            out[prefix]=obj
    rec("", cfg)
    return out
