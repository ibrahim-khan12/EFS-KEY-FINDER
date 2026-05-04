# Project Architecture

## 1. System Design Goals

- Forensic-readiness
- modular Python architecture
- clean separation between acquisition, parsing, correlation, storage, and reporting
- GUI and CLI over the same analysis engine
- future extensibility for real EFS internals and deleted-artifact recovery

## 2. High-Level Flow

1. Analyst selects evidence source.
2. Collector resolves mode: `live` or `image`.
3. Evidence integrity module hashes the source when applicable.
4. Live collector gathers users, sessions, and artifact roots.
5. File scanner finds candidate EFS-encrypted files.
6. Certificate locator finds crypto material and certificate files.
7. Registry analyzer parses EFS-related keys.
8. Timeline builder correlates activity.
9. SQLite persists the case.
10. Reporting engine exports structured evidence.
11. GUI or CLI presents the findings.

## 3. Module Responsibilities

### `core/config.py`
- central constants
- artifact paths
- output paths
- report schemas

### `core/app.py`
- CLI parsing
- collector execution
- database initialization
- report generation

### `modules/collector.py`
- orchestration layer
- chain-of-custody recording
- mode resolution
- result packaging

### `modules/efs_scanner.py`
- candidate encrypted file discovery
- Windows encrypted attribute check
- heuristic correlation for demo and research workflows

### `modules/certificate_locator.py`
- certificate file discovery
- thumbprint generation
- live store placeholder integration point

### `modules/registry_analyzer.py`
- EFS registry path parsing
- offline hive support
- deleted-value recovery extension point

### `modules/live_collector.py`
- active user enumeration
- process inventory
- explorer context
- per-user artifact root mapping

### `modules/image_analyzer.py`
- RAW and E01 recognition
- read-only image summary
- mountless parsing integration point

### `modules/timeline.py`
- timeline synthesis
- suspicious activity alerting

### `modules/case_database.py`
- SQLite case persistence

### `reports/exporter.py`
- JSON, CSV, HTML, PDF report export

### `gui/app.py`
- dashboard
- source selection
- evidence tree
- result display
- export workflow

## 4. Forensic Design Principles

- Read-only evidence handling
- Explicit chain-of-custody logging
- Source hashing for integrity
- Timestamp preservation
- Clear separation between observation and interpretation
- Audit-friendly outputs

## 5. Advanced Feature Roadmap

- True EFS attribute collection via Windows APIs
- Native certificate store extraction through CryptoAPI
- Offline NTUSER.DAT and SOFTWARE hive correlation
- Registry transaction-log recovery
- Deleted file and slack-space carving
- Enterprise bulk scan controller
- Timeline chart widgets in GUI
