# User Guide

## 1. Introduction to EFS and Digital Forensics

Microsoft Encrypting File System (EFS) is a Windows feature that encrypts files using per-user certificates and associated key material. In digital forensics, EFS artifacts can help investigators identify:
- who encrypted data
- where key material may exist
- which user profiles are involved
- whether encryption activity relates to policy, privacy, or insider threat events

This project helps examiners discover EFS-related evidence without mounting forensic images in read-write mode.

## 2. Legal and Ethical Considerations

- Use only with authorization.
- Maintain read-only handling whenever possible.
- Record chain of custody for every step.
- Avoid unnecessary access to unrelated personal data.
- Document tool limitations in the final report.
- Treat outputs as investigative leads unless independently verified.

## 3. System Requirements

- Windows 10 or Windows 11 preferred
- Python 3.12+
- 8 GB RAM minimum
- Administrative privileges for deeper live analysis
- Optional forensic image libraries: `pytsk3`, `pyewf`

## 4. Installation Steps

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you want full Windows integration, also verify:
- `pywin32`
- access to the evidence source in read-only mode

## 5. Step-by-Step Usage

### CLI workflow

1. Open PowerShell in the project directory.
2. Activate the virtual environment.
3. Run a live scan:

```powershell
py main.py --source C:\ --mode live --case-id CASE-001 --investigator "Ali"
```

4. Run an image scan:

```powershell
py main.py --source D:\evidence\disk.E01 --mode image --export json csv html pdf
```

5. Review the `output/` directory.

### GUI workflow

1. Launch the dashboard:

```powershell
py -m gui.app
```

2. Select a drive, folder, or forensic image.
3. Choose `auto`, `live`, or `image`.
4. Enter the case ID and examiner.
5. Click `Scan`.
6. Review the evidence tree and JSON panel.
7. Export reports.

## 6. Example Investigation Cases

### Case A: Insider encrypted HR payroll data
- Suspect user encrypts salary spreadsheets using EFS.
- Tool identifies candidate encrypted files in a payroll folder.
- User profile analysis locates crypto artifacts.
- Timeline helps correlate encryption activity.

### Case B: Forensic image triage
- Investigator receives an E01 image from a seized laptop.
- Tool analyzes the image path in read-only mode.
- Output shows evidence integrity hash, image summary, and correlated artifacts.

## 7. Screenshot Placeholders

Store screenshots in the `docs/screenshots/` folder:
- dashboard before scan
- populated evidence tree
- exported report view

## 8. Result Interpretation

- `encrypted_files`: candidate EFS targets and their timestamps
- `certificates`: user-linked certificate artifacts and thumbprints
- `registry`: EFS policy and configuration evidence
- `timeline`: merged chronological artifact sequence
- `alerts`: investigator attention markers for suspicious activity
- `evidence_integrity`: SHA-256 and handling posture

Always explain whether a finding is:
- direct evidence
- inferred correlation
- placeholder due to platform limitations

## 9. Team Work Division

Suggested team structure:
- Member 1: EFS research and Windows forensic theory
- Member 2: live collection and artifact scanning modules
- Member 3: GUI and reporting
- Member 4: testing, documentation, and demo case preparation

## 10. Court Admissibility Best Practices

- Record investigator identity and case number
- Hash the evidence source when possible
- Preserve timestamps
- Document read-only methodology
- Separate facts from interpretation
- Describe tool limitations honestly
