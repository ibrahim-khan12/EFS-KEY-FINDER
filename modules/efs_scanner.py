from __future__ import annotations

import logging
import os
import stat
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


class EFSScanner:
    """Detect candidate EFS-encrypted files.

    True EFS attribute inspection is Windows-specific and may require win32 APIs.
    This scanner combines extension-independent heuristics with optional attribute checks.
    """

    def scan_path(self, root: str | Path) -> list[dict[str, Any]]:
        root_path = Path(root)
        findings: list[dict[str, Any]] = []
        if not root_path.exists():
            LOGGER.warning("Scan root does not exist: %s", root_path)
            return findings

        for path in root_path.rglob("*"):
            if not path.is_file():
                continue
            detected_by = []
            try:
                st = path.stat()
                cipher_metadata = self._inspect_with_cipher(path)
                if self._has_windows_encrypted_flag(st):
                    detected_by.append("windows_encrypted_attribute")
                if cipher_metadata.get("confirmed"):
                    detected_by.append("cipher_confirmation")
                if self._looks_like_efs_candidate(path):
                    detected_by.append("artifact_correlation")
                if detected_by:
                    findings.append(
                        {
                            "path": str(path),
                            "size": st.st_size,
                            "created": datetime.fromtimestamp(st.st_ctime).isoformat(),
                            "modified": datetime.fromtimestamp(st.st_mtime).isoformat(),
                            "efs_status": "confirmed" if cipher_metadata.get("confirmed") or self._has_windows_encrypted_flag(st) else "suspected",
                            "efs_detected_by": ", ".join(sorted(set(detected_by))),
                            "algorithm": cipher_metadata.get("algorithm", ""),
                            "key_length": cipher_metadata.get("key_length", ""),
                            "decrypt_users": "; ".join(cipher_metadata.get("decrypt_users", [])),
                            "decrypt_thumbprints": "; ".join(cipher_metadata.get("decrypt_thumbprints", [])),
                            "source": str(root_path),
                        }
                    )
            except (OSError, PermissionError) as exc:
                LOGGER.debug("Skipping %s: %s", path, exc)
        return findings

    @staticmethod
    def _has_windows_encrypted_flag(st_result: os.stat_result) -> bool:
        file_attributes = getattr(st_result, "st_file_attributes", 0)
        encrypted_flag = getattr(stat, "FILE_ATTRIBUTE_ENCRYPTED", 0x4000)
        return bool(file_attributes & encrypted_flag)

    @staticmethod
    def _looks_like_efs_candidate(path: Path) -> bool:
        lowered = str(path).lower()
        return any(token in lowered for token in ["sensitive", "confidential", "finance", "hr", "legal"])

    @staticmethod
    def _inspect_with_cipher(path: Path) -> dict[str, Any]:
        if os.name != "nt":
            return {"confirmed": False, "decrypt_users": []}
        try:
            result = subprocess.run(
                ["cipher", "/c", str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                timeout=6,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return {"confirmed": False, "decrypt_users": []}

        output = ((result.stdout or "") + "\n" + (result.stderr or "")).replace("\x00", "")
        if "Users who can decrypt:" not in output:
            return {"confirmed": False, "decrypt_users": [], "decrypt_thumbprints": []}

        decrypt_users: list[str] = []
        decrypt_thumbprints: list[str] = []
        algorithm = ""
        key_length = ""
        in_user_block = False

        for raw_line in output.splitlines():
            line = raw_line.replace("\x00", "").strip()
            if not line:
                if in_user_block:
                    in_user_block = False
                continue
            if line.startswith("Users who can decrypt:"):
                in_user_block = True
                continue
            if line.startswith("No recovery certificate found."):
                in_user_block = False
            if line.startswith("Key Information:"):
                in_user_block = False
                continue
            if in_user_block and "[" in line:
                decrypt_users.append(line)
            if line.startswith("Certificate thumbprint:"):
                decrypt_thumbprints.append(line.split(":", 1)[1].strip())
            if line.startswith("Algorithm:"):
                algorithm = line.split(":", 1)[1].strip()
            if line.startswith("Key Length:"):
                key_length = line.split(":", 1)[1].strip()

        return {
            "confirmed": True,
            "decrypt_users": decrypt_users,
            "decrypt_thumbprints": decrypt_thumbprints,
            "algorithm": algorithm,
            "key_length": key_length,
        }
