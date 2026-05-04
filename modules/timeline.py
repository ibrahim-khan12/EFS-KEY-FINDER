from __future__ import annotations

from typing import Any


class TimelineBuilder:
    def build(self, results: dict[str, Any]) -> list[dict[str, Any]]:
        timeline: list[dict[str, Any]] = []
        for file_item in results.get("encrypted_files", []):
            timeline.append(
                {
                    "timestamp": file_item.get("modified") or file_item.get("created"),
                    "artifact_type": "encrypted_file",
                    "description": f"Potential EFS file: {file_item.get('path')}",
                    "source": file_item.get("source", ""),
                }
            )
        for cert in results.get("certificates", []):
            timeline.append(
                {
                    "timestamp": cert.get("not_before"),
                    "artifact_type": "certificate",
                    "description": f"Certificate for {cert.get('user')}: {cert.get('thumbprint')}",
                    "source": cert.get("source", ""),
                }
            )
        for reg in results.get("registry", []):
            timeline.append(
                {
                    "timestamp": reg.get("last_written"),
                    "artifact_type": "registry",
                    "description": f"Registry value {reg.get('value_name')} at {reg.get('key_path')}",
                    "source": reg.get("source", ""),
                }
            )
        timeline.sort(key=lambda item: item.get("timestamp") or "")
        return timeline

    def suspicious_activity_alerts(self, results: dict[str, Any]) -> list[str]:
        alerts: list[str] = []
        encrypted_count = len(results.get("encrypted_files", []))
        if encrypted_count > 25:
            alerts.append("High volume of candidate EFS files detected; investigate possible mass encryption event.")
        for file_item in results.get("encrypted_files", []):
            path = (file_item.get("path") or "").lower()
            if any(keyword in path for keyword in ["payroll", "salary", "contracts", "executive"]):
                alerts.append(f"Sensitive business data candidate detected: {file_item.get('path')}")
        return sorted(set(alerts))
