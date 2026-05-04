# EFS Artifact Discovery Toolkit

A professional-grade forensic toolkit for Windows systems, designed to discover, correlate, and report Microsoft Encrypting File System (EFS) artifacts from live systems or forensic disk images. Developed as a semester project for digital forensics education and research.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Example Investigation Questions](#example-investigation-questions)
- [Outputs](#outputs)
- [Troubleshooting](#troubleshooting)
- [Compatibility](#compatibility)
- [Legal and Ethics Notice](#legal-and-ethics-notice)

## Overview

This toolkit is tailored for digital forensic investigations, including incident response, triage, insider threat analysis, and academic research on Windows EFS artifact analysis. It supports both command-line operations for forensic analysts and a graphical user interface for demonstrations and guided examinations.

The tool facilitates comprehensive EFS artifact collection, ensuring evidence integrity through hashing, chain-of-custody logging, and structured reporting.

## Key Features

- **File Scanning**: Identify candidate EFS-encrypted files across specified sources.
- **Artifact Discovery**: Locate user cryptographic and certificate artifact paths.
- **Registry Parsing**: Analyze EFS-related registry locations for key insights.
- **Workflow Support**: Handle both live-system and forensic-image workflows.
- **Evidence Integrity**: Generate SHA-256 hashes for all collected evidence.
- **Chain of Custody**: Maintain detailed logs of investigative actions.
- **Data Storage**: Store case results in a SQLite database for structured querying.
- **Report Generation**: Export findings in JSON, CSV, HTML, and PDF formats.
- **Timeline Analysis**: Construct timeline views and detect suspicious activities.
- **User Interface**: Provide a dark-themed forensic dashboard for result visualization.

## Architecture

The project is organized into modular components for maintainability and extensibility:

- `core/`: Core configuration, logging, and application entry points.
- `modules/`: Forensic collection and artifact analysis engines.
- `gui/`: Tkinter-based investigation dashboard.
- `reports/`: Logic for generating various report formats.
- `utils/`: Utilities for hashing and chain-of-custody management.
- `docs/`: Documentation, including user guides, roadmaps, and screenshot placeholders.
- `demo/`: Sample investigation scenarios and materials.
- `tests/`: Testing strategies and placeholders.

## Installation

### Prerequisites

- Windows operating system (primary target: Windows 10/11).
- Python 3.12 or newer.
- Administrative privileges recommended for live system collection.

### Steps

1. **Install Python**: Ensure Python 3.12 or later is installed on your Windows system.

2. **Create Virtual Environment**:
   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Optional Packages**: For enhanced Windows integration, install additional packages:
   - `pywin32` for advanced system access.
   - Ensure administrative privileges for deeper live collection capabilities.

## Usage

### Command-Line Interface (CLI)

Run the toolkit via command line for automated forensic workflows:

```powershell
py main.py --source C:\ --mode live --case-id CASE-IR-001 --investigator "DF Team" --export json csv html pdf
```

**Parameters**:
- `--source`: Path to the source directory or drive (e.g., `C:\` for live system).
- `--mode`: Operation mode (`live` for live systems, `image` for forensic images).
- `--case-id`: Unique identifier for the investigation case.
- `--investigator`: Name or identifier of the investigator.
- `--export`: Formats for report export (options: `json`, `csv`, `html`, `pdf`).

### Generating a Real EFS Demo Dataset

To create a realistic EFS-encrypted dataset for testing:

```powershell
powershell -ExecutionPolicy Bypass -File .\demo\create_real_efs_dataset.ps1
py main.py --source .\demo\RealEfsDataset --mode live --case-id CASE-REAL-EFS
```

### Graphical User Interface (GUI)

Launch the desktop dashboard for interactive investigation:

```powershell
py -m gui.app
```

### Web User Interface

Start the web-based interface for remote access:

```powershell
py -m webui.server --host 127.0.0.1 --port 8765
```

Access the interface at: `http://127.0.0.1:8765/`

## Example Investigation Questions

The toolkit aids in answering key forensic questions such as:

- Which files exhibit signs of EFS encryption?
- Which user profiles contain EFS-related cryptographic material?
- Which certificate artifacts correspond to potential insider threats?
- Are EFS artifacts disproportionately located in sensitive directories?
- What integrity hashes were computed for the evidence sources?

## Outputs

Investigation results are stored in the `output/` directory, including:

- **SQLite Database**: Structured case data for querying and analysis.
- **JSON Summary**: Machine-readable overview of findings.
- **CSV Tables**: Tabular data of artifacts for spreadsheet analysis.
- **HTML Report**: Web-viewable investigation summary.
- **PDF Report**: Printable executive summary.
- **Chain-of-Custody Log**: Detailed record of all actions taken.
- **Runtime Logs**: Forensic execution logs for audit purposes.

## Troubleshooting

- **Python Not Recognized**: Use the Windows `py` launcher (e.g., `py -3.12`).
- **Empty Certificate Store**: Verify `pywin32` installation and administrative privileges.
- **Limited Image Parsing**: Ensure `pytsk3` and `pyewf` are correctly installed for forensic image support.
- **Missing Live Artifacts**: Re-run with elevated privileges for comprehensive collection.
- **Incomplete Registry Recovery**: Note that deleted value recovery is best-effort; advanced carving may be required for full recovery.

## Compatibility

- **Primary Platform**: Windows 10 and Windows 11.
- **Secondary Support**: Cross-platform code for offline parsing and reporting on other systems.
- **Optimal Performance**: Windows execution with read-only evidence handling for maximum forensic integrity.

## Legal and Ethics Notice

This toolkit is intended for authorized forensic use only. Always handle evidence in read-only mode, maintain a strict chain of custody, adhere to privacy laws and organizational policies, and document all investigative actions for potential legal scrutiny. Unauthorized use may violate laws and ethical standards.
