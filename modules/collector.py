from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from modules.certificate_locator import CertificateLocator
from modules.efs_scanner import EFSScanner
from modules.image_analyzer import ImageAnalyzer
from modules.live_collector import LiveSystemCollector
from modules.registry_analyzer import RegistryAnalyzer
from modules.timeline import TimelineBuilder
from utils.chain_of_custody import ChainOfCustodyEntry, ChainOfCustodyLogger
from utils.hashing import sha256_file


@dataclass
class CaseMetadata:
    case_id: str
    investigator: str
    source: str
    mode: str
    collected_at: str


class EFSArtifactCollector:
    def __init__(self, case_id: str, investigator: str) -> None:
        self.case_id = case_id
        self.investigator = investigator
        self.scanner = EFSScanner()
        self.live_collector = LiveSystemCollector()
        self.cert_locator = CertificateLocator()
        self.registry_analyzer = RegistryAnalyzer()
        self.image_analyzer = ImageAnalyzer()
        self.timeline_builder = TimelineBuilder()
        self.coc = ChainOfCustodyLogger()

    def run(self, source: str, mode: str = "auto") -> dict[str, Any]:
        resolved_mode = self._resolve_mode(source, mode)
        source_path = Path(source)
        source_hash = sha256_file(source_path) if source_path.is_file() else None

        self.coc.record(
            ChainOfCustodyEntry(
                case_id=self.case_id,
                examiner=self.investigator,
                action="scan_started",
                source=source,
                notes=f"Mode resolved to {resolved_mode}",
            )
        )

        live_context = self.live_collector.collect() if resolved_mode == "live" else None
        user_roots = self.live_collector.enumerate_user_artifact_roots(source) if resolved_mode == "live" else []
        encrypted_files = self.scanner.scan_path(source)
        certificates = self.cert_locator.discover(user_roots)
        if resolved_mode == "live":
            certificates.extend(self.cert_locator.enumerate_live_store())
            registry = self.registry_analyzer.analyze_live_placeholders()
            image_summary = None
        else:
            registry = []
            image_summary = self.image_analyzer.summarize_image(source)

        results = {
            "case": asdict(
                CaseMetadata(
                    case_id=self.case_id,
                    investigator=self.investigator,
                    source=source,
                    mode=resolved_mode,
                    collected_at=datetime.now(timezone.utc).isoformat(),
                )
            ),
            "evidence_integrity": {
                "sha256": source_hash,
                "read_only": True,
                "mountless": resolved_mode == "image",
            },
            "live_context": asdict(live_context) if live_context else None,
            "image_summary": image_summary,
            "user_artifact_roots": user_roots,
            "encrypted_files": encrypted_files,
            "certificates": certificates,
            "registry": registry,
            "deleted_registry_recovery": self.registry_analyzer.deleted_value_recovery_notes(),
        }
        results["timeline"] = self.timeline_builder.build(results)
        results["alerts"] = self.timeline_builder.suspicious_activity_alerts(results)

        self.coc.record(
            ChainOfCustodyEntry(
                case_id=self.case_id,
                examiner=self.investigator,
                action="scan_completed",
                source=source,
                notes=f"Found {len(encrypted_files)} candidate encrypted files and {len(certificates)} certificates.",
            )
        )
        return results

    @staticmethod
    def _resolve_mode(source: str, requested: str) -> str:
        if requested != "auto":
            return requested
        suffix = Path(source).suffix.lower()
        if suffix in {".e01", ".dd", ".raw", ".001"}:
            return "image"
        return "live"
