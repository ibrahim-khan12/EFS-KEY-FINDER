from __future__ import annotations

import logging
import os
import platform
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil

from core.config import USER_ARTIFACT_SUBPATHS, WINDOWS_ONLY_WARNING


LOGGER = logging.getLogger(__name__)


@dataclass
class LiveContext:
    hostname: str
    os_version: str
    active_users: list[str]
    processes: list[dict[str, Any]]
    explorer_sessions: list[dict[str, Any]]
    warnings: list[str]


class LiveSystemCollector:
    def collect(self) -> LiveContext:
        warnings: list[str] = []
        if platform.system() != "Windows":
            warnings.append(WINDOWS_ONLY_WARNING)

        active_users = sorted({user.name for user in psutil.users()})
        processes: list[dict[str, Any]] = []
        explorer_sessions: list[dict[str, Any]] = []

        for proc in psutil.process_iter(attrs=["pid", "name", "username", "create_time"]):
            info = proc.info
            processes.append(info)
            if (info.get("name") or "").lower() == "explorer.exe":
                explorer_sessions.append(info)

        return LiveContext(
            hostname=platform.node(),
            os_version=platform.platform(),
            active_users=active_users,
            processes=processes,
            explorer_sessions=explorer_sessions,
            warnings=warnings,
        )

    def enumerate_user_artifact_roots(self, base_root: str | Path | None = None) -> list[dict[str, str]]:
        roots: list[dict[str, str]] = []
        users_root = self._resolve_users_root(base_root)
        if not users_root.exists():
            return roots

        for user_dir in self._safe_iterdir(users_root):
            if not user_dir.is_dir():
                continue
            for subpath in USER_ARTIFACT_SUBPATHS:
                candidate = user_dir / subpath
                try:
                    if not candidate.exists():
                        continue
                    discovered = datetime.fromtimestamp(candidate.stat().st_mtime).isoformat()
                except (OSError, PermissionError):
                    LOGGER.debug("Skipping inaccessible artifact root: %s", candidate)
                    continue

                roots.append(
                    {
                        "user": user_dir.name,
                        "path": str(candidate),
                        "discovered": discovered,
                    }
                )
        return roots

    @staticmethod
    def _resolve_users_root(base_root: str | Path | None) -> Path:
        if base_root:
            base_path = Path(base_root)
            if base_path.name.lower() == "users":
                return base_path
            nested_users = base_path / "Users"
            if nested_users.exists():
                return nested_users
        return Path(os.environ.get("SystemDrive", "C:")) / "Users"

    @staticmethod
    def _safe_iterdir(root: Path) -> list[Path]:
        try:
            return list(root.iterdir())
        except (OSError, PermissionError):
            LOGGER.debug("Skipping inaccessible users root: %s", root)
            return []
