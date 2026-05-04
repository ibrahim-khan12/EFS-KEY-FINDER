# Demo Dataset Creation Guide

Create a fully legal, synthetic training dataset for classroom demonstration.

## 1. Create the folder structure

```text
DemoEvidence/
  Users/
    employee1/
      Documents/
        Sensitive/
        Payroll/
      AppData/
        Roaming/
          Microsoft/
            Crypto/
            Protect/
            SystemCertificates/
```

## 2. Add sample user documents

Create harmless placeholder files:
- `confidential_budget.txt`
- `salary_plan_2026.xlsx`
- `executive_contracts.docx`
- `finance_sensitive_notes.txt`

The scanner will flag these as candidate EFS artifacts because they resemble sensitive business content.

## 3. Add mock certificate artifacts

Inside `SystemCertificates` or `Crypto`, create empty or dummy files named:
- `efs_user_cert.cer`
- `efs_backup_cert.pfx`
- `userkey.key`

## 4. Simulate timestamps

Modify file timestamps on Windows to create a timeline:

```powershell
(Get-Item .\\confidential_budget.txt).CreationTime = '2026-04-15 10:30:00'
(Get-Item .\\salary_plan_2026.xlsx).LastWriteTime = '2026-04-16 11:15:00'
```

## 5. Optional E01 / RAW preparation

- Place the demo folder inside a mounted training image.
- Or export a small RAW/E01 training image using a forensic lab tool.
- Keep the image read-only for demonstration.

## 6. Expected classroom output

- identified sensitive files
- certificate thumbprints based on file content
- mapped user profile artifact roots
- timeline of file and artifact discovery
- integrity hashes for source files

## 7. Safety note

Do not use real employee data, real keys, or active corporate certificate material in the demo dataset.

## 8. Real EFS dataset option

If your Windows machine and the target volume support EFS, you can generate a true encrypted dataset with:

```powershell
powershell -ExecutionPolicy Bypass -File .\demo\create_real_efs_dataset.ps1
```

This creates `demo/RealEfsDataset/` and encrypts selected files using Windows EFS so the scanner can label them as `confirmed`.

## 9. Full end-to-end case dataset

For a stronger classroom or viva test that exercises more of the project, generate:

```powershell
powershell -ExecutionPolicy Bypass -File .\demo\create_full_case_dataset.ps1
```

This creates `demo/FullCaseDataset/` with:
- real EFS-encrypted files
- additional sensitive plaintext files for heuristic correlation
- crypto, certificate, and protect-folder artifacts
- timeline-friendly timestamps
- case narrative metadata

Recommended test source:

```text
D:\8th SEMESTER\DF\PROJECT\demo\FullCaseDataset
```

Expected project coverage:
- confirmed EFS file detection
- exact certificate thumbprint extraction from encrypted files
- user artifact root discovery
- certificate/key artifact discovery
- alert generation for sensitive content
- timeline generation
- HTML/PDF/CSV/JSON reporting
