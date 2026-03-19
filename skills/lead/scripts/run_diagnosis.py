#!/usr/bin/env python3
from pathlib import Path
from lead.pipeline import diagnose_single_run
from lead.reports.renderers import render_json, render_markdown
import argparse
p=argparse.ArgumentParser(); p.add_argument('--run-dir',required=True); p.add_argument('--out',required=True); p.add_argument('--md-out')
a=p.parse_args(); rep=diagnose_single_run(Path(a.run_dir)); render_json(rep, Path(a.out));
if a.md_out: Path(a.md_out).write_text(render_markdown(rep))
