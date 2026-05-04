from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class CaseDatabase:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def initialize(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS case_metadata (
                    case_id TEXT,
                    investigator TEXT,
                    source TEXT,
                    mode TEXT,
                    collected_at TEXT
                );
                CREATE TABLE IF NOT EXISTS encrypted_files (
                    path TEXT,
                    size INTEGER,
                    created TEXT,
                    modified TEXT,
                    efs_status TEXT,
                    efs_detected_by TEXT,
                    algorithm TEXT,
                    key_length TEXT,
                    decrypt_users TEXT,
                    decrypt_thumbprints TEXT,
                    source TEXT
                );
                CREATE TABLE IF NOT EXISTS certificates (
                    user TEXT,
                    store TEXT,
                    thumbprint TEXT,
                    subject TEXT,
                    issuer TEXT,
                    not_before TEXT,
                    not_after TEXT,
                    source TEXT
                );
                CREATE TABLE IF NOT EXISTS registry_artifacts (
                    hive TEXT,
                    key_path TEXT,
                    value_name TEXT,
                    value TEXT,
                    last_written TEXT,
                    source TEXT
                );
                CREATE TABLE IF NOT EXISTS timeline (
                    timestamp TEXT,
                    artifact_type TEXT,
                    description TEXT,
                    source TEXT
                );
                """
            )
            self._ensure_column(conn, "encrypted_files", "efs_status", "TEXT")
            self._ensure_column(conn, "encrypted_files", "algorithm", "TEXT")
            self._ensure_column(conn, "encrypted_files", "key_length", "TEXT")
            self._ensure_column(conn, "encrypted_files", "decrypt_users", "TEXT")
            self._ensure_column(conn, "encrypted_files", "decrypt_thumbprints", "TEXT")

    def store_case_results(self, results: dict[str, Any]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO case_metadata VALUES (?, ?, ?, ?, ?)",
                (
                    results.get("case", {}).get("case_id"),
                    results.get("case", {}).get("investigator"),
                    results.get("case", {}).get("source"),
                    results.get("case", {}).get("mode"),
                    results.get("case", {}).get("collected_at"),
                ),
            )
            conn.executemany(
                """
                INSERT INTO encrypted_files
                (path, size, created, modified, efs_status, efs_detected_by, algorithm, key_length, decrypt_users, decrypt_thumbprints, source)
                VALUES
                (:path, :size, :created, :modified, :efs_status, :efs_detected_by, :algorithm, :key_length, :decrypt_users, :decrypt_thumbprints, :source)
                """,
                results.get("encrypted_files", []),
            )
            conn.executemany(
                "INSERT INTO certificates VALUES (:user, :store, :thumbprint, :subject, :issuer, :not_before, :not_after, :source)",
                results.get("certificates", []),
            )
            conn.executemany(
                "INSERT INTO registry_artifacts VALUES (:hive, :key_path, :value_name, :value, :last_written, :source)",
                results.get("registry", []),
            )
            conn.executemany(
                "INSERT INTO timeline VALUES (:timestamp, :artifact_type, :description, :source)",
                results.get("timeline", []),
            )

    @staticmethod
    def _ensure_column(conn: sqlite3.Connection, table: str, column: str, column_type: str) -> None:
        existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        if column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
