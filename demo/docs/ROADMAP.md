# Step-by-Step Development Roadmap

## Phase 1: Foundation

1. Create modular project structure.
2. Define case schema and output conventions.
3. Implement logging, hashing, and chain-of-custody components.
4. Add CLI entrypoint.

## Phase 2: Core Forensic Collection

1. Build live system collector.
2. Build EFS file scanner.
3. Build certificate and key discovery module.
4. Build registry analyzer.
5. Add offline image abstraction for RAW and E01.

## Phase 3: Correlation and Persistence

1. Build orchestrator to merge findings.
2. Create timeline engine.
3. Add suspicious activity alerting.
4. Persist all results in SQLite.

## Phase 4: Reporting and Presentation

1. Export JSON and CSV.
2. Add HTML report.
3. Add PDF report for project defense presentation.
4. Build GUI dashboard.

## Phase 5: Validation and Demo

1. Create a safe synthetic dataset.
2. Run known-case scans.
3. Capture screenshots.
4. Document findings and limitations.

## Phase 6: Advanced Forensic Enhancements

1. Deleted registry value recovery.
2. Transaction-log awareness.
3. Better Windows certificate store parsing.
4. Enterprise bulk scanning mode.
5. Auto evidence package export.
