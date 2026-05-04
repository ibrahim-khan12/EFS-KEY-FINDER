from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)

try:
    from Registry import Registry  # type: ignore
except ImportError:  # pragma: no cover
    Registry = None

from core.config import EFS_REGISTRY_PATHS


class RegistryAnalyzer:
    def analyze_live_placeholders(self) -> list[dict[str, Any]]:
        return [
            {
                "hive": "HKCU",
                "key_path": EFS_REGISTRY_PATHS["hkcu_efs"],
                "value_name": "Placeholder",
                "value": "Use winreg/python-registry on a Windows host during live execution.",
                "last_written": datetime.utcnow().isoformat(),
                "source": "live_registry_placeholder",
            }
        ]

    def analyze_hive(self, hive_path: str | Path, root_label: str = "OfflineHive") -> list[dict[str, Any]]:
        hive_file = Path(hive_path)
        if Registry is None or not hive_file.exists():
            LOGGER.info("Registry library unavailable or hive missing: %s", hive_file)
            return []

        findings: list[dict[str, Any]] = []
        hive = Registry.Registry(str(hive_file))
        for _key_name, registry_path in EFS_REGISTRY_PATHS.items():
            try:
                key = hive.open(registry_path)
            except Exception:
                continue
            for value in key.values():
                findings.append(
                    {
                        "hive": root_label,
                        "key_path": key.path(),
                        "value_name": value.name(),
                        "value": str(value.value()),
                        "last_written": key.timestamp().isoformat() if key.timestamp() else "",
                        "source": str(hive_file),
                    }
                )
        return findings

    def deleted_value_recovery_notes(self) -> dict[str, str]:
        return {
            "status": "best-effort",
            "notes": "Deleted registry recovery usually requires hive slack parsing, transaction logs, or specialized carving. The project architecture leaves a plug-in point for this advanced feature.",
        }
