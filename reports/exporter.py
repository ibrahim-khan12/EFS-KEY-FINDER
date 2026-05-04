from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

from core.config import REPORT_COLUMNS


class ReportExporter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, results: dict[str, Any], formats: list[str]) -> list[Path]:
        generated: list[Path] = []
        if "json" in formats:
            path = self.output_dir / "report.json"
            path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
            generated.append(path)
        if "csv" in formats:
            generated.extend(self._export_csv(results))
        if "html" in formats:
            generated.append(self._export_html(results))
        if "pdf" in formats:
            generated.append(self._export_pdf(results))
        return generated

    def _export_csv(self, results: dict[str, Any]) -> list[Path]:
        created: list[Path] = []
        for section, columns in REPORT_COLUMNS.items():
            rows = results.get(section, [])
            path = self.output_dir / f"{section}.csv"
            pd.DataFrame(rows, columns=columns).to_csv(path, index=False)
            created.append(path)
        return created

    def _export_html(self, results: dict[str, Any]) -> Path:
        path = self.output_dir / "report.html"
        encrypted_files = results.get("encrypted_files", [])
        confirmed = [item for item in encrypted_files if item.get("efs_status") == "confirmed"]
        certificates = results.get("certificates", [])
        registry = results.get("registry", [])
        timeline = results.get("timeline", [])
        user_roots = results.get("user_artifact_roots", [])
        alerts = results.get("alerts", [])
        top_files = encrypted_files[:8]
        top_timeline = timeline[:8]
        top_certs = certificates[:8]
        top_registry = registry[:8]
        top_roots = user_roots[:8]

        def bullet_list(items: list[str], empty: str) -> str:
            if not items:
                return f"<p>{empty}</p>"
            return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"

        file_lines = [
            f"{item.get('efs_status', 'suspected').upper()} | {item.get('path', 'N/A')} | Thumbprints: {item.get('decrypt_thumbprints', 'N/A') or 'N/A'}"
            for item in top_files
        ]
        cert_lines = [
            f"{item.get('subject', 'N/A')} ({item.get('user', 'N/A')}) | {item.get('thumbprint', 'N/A')}"
            for item in top_certs
        ]
        registry_lines = [
            f"{item.get('key_path', 'N/A')} | {item.get('value_name', 'N/A')}"
            for item in top_registry
        ]
        timeline_lines = [
            f"{item.get('timestamp', 'N/A')} | {item.get('artifact_type', 'artifact')} | {item.get('description', 'N/A')}"
            for item in top_timeline
        ]
        root_lines = [
            f"{item.get('user', 'N/A')} | {item.get('path', 'N/A')}"
            for item in top_roots
        ]
        alert_lines = [str(item) for item in alerts]
        html = f"""
        <html>
        <head>
            <title>EFS Key Finder Report</title>
            <style>
                body {{ font-family: Segoe UI, sans-serif; background: #0f172a; color: #e2e8f0; margin: 2rem; }}
                h1, h2 {{ color: #7dd3fc; }}
                .card {{ background: #111827; padding: 1rem 1.2rem; border-radius: 12px; margin-bottom: 1rem; }}
                .summary-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
                .summary-item {{ background: #0b1220; padding: 0.8rem; border-radius: 10px; }}
                ul {{ margin: 0.5rem 0 0; padding-left: 1.2rem; }}
                p {{ margin: 0.35rem 0; }}
            </style>
        </head>
        <body>
            <h1>EFS Key Finder / EFS Key Extractor</h1>
            <div class="card">
                <h2>Case Overview</h2>
                <p><strong>Case ID:</strong> {results.get('case', {}).get('case_id', 'N/A')}</p>
                <p><strong>Investigator:</strong> {results.get('case', {}).get('investigator', 'N/A')}</p>
                <p><strong>Source:</strong> {results.get('case', {}).get('source', 'N/A')}</p>
                <p><strong>Mode:</strong> {results.get('case', {}).get('mode', 'N/A')}</p>
            </div>
            <div class="card">
                <h2>Executive Summary</h2>
                <div class="summary-grid">
                    <div class="summary-item"><strong>Total Findings</strong><p>{len(encrypted_files)}</p></div>
                    <div class="summary-item"><strong>Confirmed EFS</strong><p>{len(confirmed)}</p></div>
                    <div class="summary-item"><strong>Certificates</strong><p>{len(certificates)}</p></div>
                    <div class="summary-item"><strong>Registry Artifacts</strong><p>{len(registry)}</p></div>
                    <div class="summary-item"><strong>Timeline Entries</strong><p>{len(timeline)}</p></div>
                    <div class="summary-item"><strong>Alerts</strong><p>{len(alerts)}</p></div>
                </div>
            </div>
            <div class="card"><h2>Exact Key Thumbprints</h2>{bullet_list([item.get('decrypt_thumbprints', 'N/A') for item in confirmed if item.get('decrypt_thumbprints')], 'No confirmed EFS thumbprints recorded.')}</div>
            <div class="card"><h2>Top File Findings</h2>{bullet_list(file_lines, 'No encrypted or suspected files recorded.')}</div>
            <div class="card"><h2>Certificate Artifacts</h2>{bullet_list(cert_lines, 'No certificate artifacts recorded.')}</div>
            <div class="card"><h2>Registry Evidence</h2>{bullet_list(registry_lines, 'No registry evidence recorded.')}</div>
            <div class="card"><h2>User Artifact Roots</h2>{bullet_list(root_lines, 'No user artifact roots recorded.')}</div>
            <div class="card"><h2>Timeline Highlights</h2>{bullet_list(timeline_lines, 'No timeline events recorded.')}</div>
            <div class="card"><h2>Alerts</h2>{bullet_list(alert_lines, 'No alerts generated.')}</div>
        </body>
        </html>
        """
        path.write_text(html, encoding="utf-8")
        return path

    def _export_pdf(self, results: dict[str, Any]) -> Path:
        path = self.output_dir / "report.pdf"
        pdf = canvas.Canvas(str(path), pagesize=A4)
        width, height = A4
        margin_x = 42
        y = height - 48

        def new_page() -> None:
            nonlocal y
            pdf.showPage()
            y = height - 48

        def ensure_space(required: int = 24) -> None:
            nonlocal y
            if y < required:
                new_page()

        def draw_title(text: str) -> None:
            nonlocal y
            ensure_space(80)
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawString(margin_x, y, text)
            y -= 24

        def draw_section(title: str) -> None:
            nonlocal y
            ensure_space(40)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(margin_x, y, title)
            y -= 14
            pdf.setLineWidth(0.5)
            pdf.line(margin_x, y, width - margin_x, y)
            y -= 12

        def draw_paragraph(text: str, font: str = "Helvetica", size: int = 9, indent: int = 0) -> None:
            nonlocal y
            wrapped = simpleSplit(text, font, size, width - (margin_x * 2) - indent)
            pdf.setFont(font, size)
            for line in wrapped:
                ensure_space(22)
                pdf.drawString(margin_x + indent, y, line)
                y -= 12

        def draw_kv(label: str, value: Any) -> None:
            draw_paragraph(f"{label}: {value if value not in (None, '') else 'N/A'}")

        case = results.get("case", {})
        integrity = results.get("evidence_integrity", {})
        encrypted_files = results.get("encrypted_files", [])
        certificates = results.get("certificates", [])
        registry = results.get("registry", [])
        timeline = results.get("timeline", [])
        alerts = results.get("alerts", [])
        user_roots = results.get("user_artifact_roots", [])
        confirmed = [item for item in encrypted_files if item.get("efs_status") == "confirmed"]

        draw_title("EFS Key Finder / EFS Key Extractor")
        draw_paragraph("Brief but Complete Forensic Report", font="Helvetica-Bold", size=12)
        y -= 6
        draw_paragraph("Authorized forensic use only. Maintain read-only handling and preserve chain of custody.")

        draw_section("1. Case Overview")
        draw_kv("Case ID", case.get("case_id"))
        draw_kv("Investigator", case.get("investigator"))
        draw_kv("Source", case.get("source"))
        draw_kv("Mode", case.get("mode"))

        draw_section("2. Evidence Integrity")
        draw_kv("SHA256", integrity.get("sha256"))
        draw_kv("Read Only", integrity.get("read_only"))

        draw_section("3. Executive Summary")
        draw_kv("Total EFS Findings", len(encrypted_files))
        draw_kv("Confirmed EFS Files", len(confirmed))
        draw_kv("Certificate / Key Artifacts", len(certificates))
        draw_kv("Registry Artifacts", len(registry))
        draw_kv("Timeline Entries", len(timeline))
        draw_kv("User Artifact Roots", len(user_roots))

        draw_section("4. Exact Key Identifiers")
        if confirmed:
            for index, item in enumerate(confirmed[:8], start=1):
                draw_paragraph(f"{index}. {item.get('path', 'N/A')}", font="Helvetica-Bold", size=9)
                draw_paragraph(
                    f"Thumbprints: {item.get('decrypt_thumbprints', 'N/A')}",
                    indent=12,
                )
                draw_paragraph(
                    f"Decrypt Users: {item.get('decrypt_users', 'N/A')}",
                    indent=12,
                )
                y -= 4
        else:
            draw_paragraph("No confirmed EFS thumbprints were recorded.")

        draw_section("5. Alerts")
        if alerts:
            for index, alert in enumerate(alerts, start=1):
                draw_paragraph(f"{index}. {alert}")
        else:
            draw_paragraph("No high-priority alerts were generated for this run.")

        draw_section("6. Top File Findings")
        if encrypted_files:
            for index, item in enumerate(encrypted_files[:12], start=1):
                draw_paragraph(f"{index}. {item.get('path', 'N/A')}", font="Helvetica-Bold", size=9)
                draw_paragraph(
                    f"Status: {item.get('efs_status', 'suspected')} | Detection: {item.get('efs_detected_by', 'N/A')}",
                    indent=12,
                )
                draw_paragraph(
                    f"Modified: {item.get('modified', 'N/A')} | Users: {item.get('decrypt_users', 'N/A')}",
                    indent=12,
                )
                draw_paragraph(
                    f"Thumbprints: {item.get('decrypt_thumbprints', 'N/A')}",
                    indent=12,
                )
                y -= 4
        else:
            draw_paragraph("No encrypted or suspected EFS files were recorded.")

        draw_section("7. Certificate Artifacts")
        if certificates:
            for index, item in enumerate(certificates[:12], start=1):
                draw_paragraph(f"{index}. {item.get('subject', 'N/A')} ({item.get('user', 'N/A')})", font="Helvetica-Bold", size=9)
                draw_paragraph(
                    f"Thumbprint: {item.get('thumbprint', 'N/A')} | Store: {item.get('store', 'N/A')}",
                    indent=12,
                )
                draw_paragraph(
                    f"Source: {item.get('source', 'N/A')}",
                    indent=12,
                )
                y -= 4
        else:
            draw_paragraph("No certificate or private-key artifacts were recorded.")

        draw_section("8. Registry Evidence")
        if registry:
            for index, item in enumerate(registry[:10], start=1):
                draw_paragraph(f"{index}. {item.get('key_path', 'N/A')}", font="Helvetica-Bold", size=9)
                draw_paragraph(
                    f"Hive: {item.get('hive', 'N/A')} | Value: {item.get('value_name', 'N/A')} | Last Written: {item.get('last_written', 'N/A')}",
                    indent=12,
                )
        else:
            draw_paragraph("No EFS-related registry evidence was recorded.")

        draw_section("9. Timeline Highlights")
        if timeline:
            for index, item in enumerate(timeline[:12], start=1):
                draw_paragraph(
                    f"{index}. {item.get('timestamp', 'N/A')} | {item.get('artifact_type', 'artifact')} | {item.get('description', 'N/A')}"
                )
        else:
            draw_paragraph("No timeline events were generated.")

        draw_section("10. User Artifact Roots")
        if user_roots:
            for index, item in enumerate(user_roots[:10], start=1):
                draw_paragraph(f"{index}. {item.get('user', 'N/A')} | {item.get('path', 'N/A')}")
        else:
            draw_paragraph("No user artifact roots were identified.")

        draw_section("11. Conclusion")
        if confirmed:
            draw_paragraph("The case contains confirmed EFS-encrypted files with exact certificate thumbprints and mapped decrypting user identities.")
        else:
            draw_paragraph("No confirmed EFS-encrypted files were detected; findings are limited to suspected artifacts and supporting evidence.")
        draw_paragraph("Corroborate encrypted file findings with certificate artifacts, registry evidence, user-profile roots, and chain-of-custody records.")

        pdf.save()
        return path
