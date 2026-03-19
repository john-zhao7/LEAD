#!/usr/bin/env python3
from pathlib import Path
from lead.pipeline import compare_runs
from lead.reports.renderers import render_json
import argparse
p=argparse.ArgumentParser(); p.add_argument('--run-dirs', nargs='+', required=True); p.add_argument('--out', required=True)
a=p.parse_args(); rep=compare_runs([Path(x) for x in a.run_dirs]); render_json(rep, Path(a.out))
