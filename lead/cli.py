from __future__ import annotations

import argparse
import json
from pathlib import Path

from lead.pipeline import diagnose_single_run, compare_runs
from lead.sessions.session_manager import init_session
from lead.inventory import build_inventory
from lead.reports.renderers import render_json, render_markdown


def cmd_init(args: argparse.Namespace) -> None:
    sess = init_session(Path(args.project), args.session_id)
    print(f"Initialized session {sess.session_id} at {sess.project_root}")


def cmd_inspect(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir)
    inv = build_inventory(run_dir, run_dir.name)
    print(json.dumps(inv.__dict__, indent=2))


def cmd_diagnose_run(args: argparse.Namespace) -> None:
    rep = diagnose_single_run(Path(args.run_dir), session_id=args.session_id)
    render_json(rep, Path(args.out))
    if args.md_out:
        Path(args.md_out).write_text(render_markdown(rep))
    print(f"Wrote diagnosis to {args.out}")


def cmd_compare_runs(args: argparse.Namespace) -> None:
    rep = compare_runs([Path(p) for p in args.run_dirs], session_id=args.session_id)
    render_json(rep, Path(args.out))
    if args.md_out:
        Path(args.md_out).write_text(render_markdown(rep))
    print(f"Wrote comparison report to {args.out}")


def cmd_postmortem(args: argparse.Namespace) -> None:
    rep = compare_runs([Path(p) for p in args.run_dirs], session_id=args.session_id)
    render_json(rep, Path(args.out))
    if args.md_out:
        Path(args.md_out).write_text(render_markdown(rep))
    print(f"Wrote postmortem report to {args.out}")


def cmd_export_report(args: argparse.Namespace) -> None:
    data = json.loads(Path(args.input).read_text())
    if args.format == "json":
        Path(args.out).write_text(json.dumps(data, indent=2))
    else:
        lines = ["# Exported LEAD report", "", json.dumps(data, indent=2)]
        Path(args.out).write_text("
".join(lines))
    print(f"Exported to {args.out}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lead", description="LEAD experiment diagnostics")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("init")
    a.add_argument("--project", required=True)
    a.add_argument("--session-id", required=True)
    a.set_defaults(func=cmd_init)

    a = sub.add_parser("inspect")
    a.add_argument("--run-dir", required=True)
    a.set_defaults(func=cmd_inspect)

    a = sub.add_parser("diagnose-run")
    a.add_argument("--run-dir", required=True)
    a.add_argument("--session-id", default="adhoc")
    a.add_argument("--out", required=True)
    a.add_argument("--md-out")
    a.set_defaults(func=cmd_diagnose_run)

    a = sub.add_parser("compare-runs")
    a.add_argument("--run-dirs", nargs="+", required=True)
    a.add_argument("--session-id", default="adhoc")
    a.add_argument("--out", required=True)
    a.add_argument("--md-out")
    a.set_defaults(func=cmd_compare_runs)

    a = sub.add_parser("postmortem")
    a.add_argument("--run-dirs", nargs="+", required=True)
    a.add_argument("--session-id", default="adhoc")
    a.add_argument("--out", required=True)
    a.add_argument("--md-out")
    a.set_defaults(func=cmd_postmortem)

    a = sub.add_parser("export-report")
    a.add_argument("--input", required=True)
    a.add_argument("--format", choices=["json", "md"], default="md")
    a.add_argument("--out", required=True)
    a.set_defaults(func=cmd_export_report)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
