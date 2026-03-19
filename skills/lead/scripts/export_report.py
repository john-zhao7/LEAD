#!/usr/bin/env python3
from pathlib import Path
import json, argparse
p=argparse.ArgumentParser(); p.add_argument('--input', required=True); p.add_argument('--out', required=True)
a=p.parse_args(); data=json.loads(Path(a.input).read_text()); Path(a.out).write_text(json.dumps(data, indent=2))
