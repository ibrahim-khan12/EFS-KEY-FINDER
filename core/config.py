from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = OUTPUT_DIR / "logs"
REPORT_DIR = OUTPUT_DIR / "reports"
DB_PATH = OUTPUT_DIR / "efs_case.db"
CHAIN_OF_CUSTODY = OUTPUT_DIR / "chain_of_custody.log"

APP_NAME = "EFS Key Finder / EFS Key Extractor"
APP_VERSION = "1.0.0"
DEFAULT_HASH_CHUNK_SIZE = 1024 * 1024
WINDOWS_ONLY_WARNING = "Some live-collection features require Windows and administrative context."

EFS_REGISTRY_PATHS = {
    "hkcu_efs": r"Software\\Microsoft\\Windows NT\\CurrentVersion\\EFS",
    "hklm_efs": r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\EFS",
    "hklm_policy": r"SOFTWARE\\Policies\\Microsoft\\SystemCertificates\\EFS",
}

USER_ARTIFACT_SUBPATHS = [
    Path("AppData/Roaming/Microsoft/Crypto"),
    Path("AppData/Roaming/Microsoft/SystemCertificates"),
    Path("AppData/Roaming/Microsoft/Protect"),
]

REPORT_COLUMNS = {
    "encrypted_files": [
        "path",
        "size",
        "created",
        "modified",
        "efs_status",
        "efs_detected_by",
        "algorithm",
        "key_length",
        "decrypt_users",
        "decrypt_thumbprints",
        "source",
    ],
    "certificates": ["user", "store", "thumbprint", "subject", "issuer", "not_before", "not_after", "source"],
    "registry": ["hive", "key_path", "value_name", "value", "last_written", "source"],
    "timeline": ["timestamp", "artifact_type", "description", "source"],
}
