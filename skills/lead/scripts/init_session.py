#!/usr/bin/env python3
from pathlib import Path
from lead.sessions.session_manager import init_session
import argparse

p=argparse.ArgumentParser(); p.add_argument('--project',required=True); p.add_argument('--session-id',required=True)
a=p.parse_args(); s=init_session(Path(a.project), a.session_id); print(s)
