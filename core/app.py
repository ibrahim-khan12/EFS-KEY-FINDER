from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from core.config import APP_NAME, OUTPUT_DIR
from core.logging_config import setup_logging
from modules.case_database import CaseDatabase
from modules.collector import EFSArtifactCollector
from reports.exporter import ReportExporter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="efs-key-finder", description=APP_NAME)
    parser.add_argument("--source", required=False, default="C:/", help="Live drive, mounted path, or forensic image path")
    parser.add_argument("--mode", choices=["live", "image", "auto"], default="auto", help="Collection mode")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="Output directory")
    parser.add_argument("--export", nargs="*", default=["json", "csv", "html"], choices=["json", "csv", "html", "pdf"])
    parser.add_argument("--case-id", default="CASE-001", help="Case identifier")
    parser.add_argument("--investigator", default="Examiner", help="Examiner name")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    setup_logging()

    logging.info("Starting scan against source=%s mode=%s", args.source, args.mode)
    collector = EFSArtifactCollector(case_id=args.case_id, investigator=args.investigator)
    results = collector.run(source=args.source, mode=args.mode)

    db = CaseDatabase(output_dir / "efs_case.db")
    db.initialize()
    db.store_case_results(results)

    exporter = ReportExporter(output_dir=output_dir)
    generated = exporter.export(results, formats=args.export)

    summary_path = output_dir / "scan_summary.json"
    summary_path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    logging.info("Generated outputs: %s", generated)

    print(json.dumps({"status": "ok", "generated": [str(p) for p in generated], "summary": str(summary_path)}, indent=2))
    return 0
