from __future__ import annotations

from pathlib import Path
from lead.types import ConfigSnapshot
from lead.constants import SUPPORTED_CONFIG
from lead.utils.paths import find_first
from lead.utils.yaml_utils import load_yaml


def load_config(run_dir: Path) -> ConfigSnapshot | None:
    cfg = find_first(run_dir, SUPPORTED_CONFIG)
    if not cfg:
        return None
    return ConfigSnapshot(source=str(cfg.name), values=load_yaml(cfg))
