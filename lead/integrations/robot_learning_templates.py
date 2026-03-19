from __future__ import annotations

ROBOT_CHECKLIST = [
    "reward term drift",
    "action clipping/saturation",
    "observation normalization mismatch",
    "rollout truncation changes",
    "train/eval domain mismatch",
    "control-frequency mismatch",
    "reset/wrapper bugs",
    "replay contamination",
    "metric gaming",
]
