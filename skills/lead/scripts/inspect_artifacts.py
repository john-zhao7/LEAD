#!/usr/bin/env python3
from pathlib import Path
from lead.inventory import build_inventory
import argparse, json
p=argparse.ArgumentParser(); p.add_argument('--run-dir',required=True)
a=p.parse_args(); inv=build_inventory(Path(a.run_dir), Path(a.run_dir).name); print(json.dumps(inv.__dict__, indent=2))
