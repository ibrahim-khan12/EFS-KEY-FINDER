from __future__ import annotations

import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)

try:
    import win32crypt  # type: ignore
except ImportError:  # pragma: no cover
    win32crypt = None


class CertificateLocator:
    def discover(self, user_artifact_roots: list[dict[str, str]]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        for root in user_artifact_roots:
            path = Path(root["path"])
            if not path.exists():
                continue
            for file_path in path.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.suffix.lower() not in {".pfx", ".p12", ".cer", ".crt", ".key", ".pvk"}:
                    continue
                findings.append(
                    {
                        "user": root["user"],
                        "store": path.name,
                        "thumbprint": self._sha1_thumbprint(file_path),
                        "subject": file_path.stem,
                        "issuer": "Unknown / filesystem artifact",
                        "not_before": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
                        "not_after": "Unknown",
                        "source": str(file_path),
                    }
                )
        return findings

    @staticmethod
    def _sha1_thumbprint(path: Path) -> str:
        digest = hashlib.sha1()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest().upper()

    def enumerate_live_store(self) -> list[dict[str, Any]]:
        if win32crypt is None:
            LOGGER.info("win32crypt unavailable; live certificate store enumeration skipped")
            return []
        return [
            {
                "user": "Current User",
                "store": "MY",
                "thumbprint": "LIVE-ENUM-PLACEHOLDER",
                "subject": "Use CertOpenSystemStore integration on Windows",
                "issuer": "Windows CryptoAPI",
                "not_before": "N/A",
                "not_after": "N/A",
                "source": "live_certificate_store",
            }
        ]
