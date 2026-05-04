# Demo Scenario

## Scenario

An employee is suspected of encrypting insider company data with Windows EFS before resignation.

## Investigation Goals

- identify encrypted files
- map them to the responsible user profile
- locate certificate and key artifacts
- correlate timestamps
- produce an evidence package for management and faculty evaluation

## Suggested Demo Story

User `employee1` stores sensitive files in:
- `C:\Users\employee1\Documents\Sensitive\`
- `C:\Users\employee1\Documents\Payroll\`
- `C:\Users\employee1\AppData\Roaming\Microsoft\Crypto\`
- `C:\Users\employee1\AppData\Roaming\Microsoft\SystemCertificates\`

## Walkthrough

1. Prepare a test folder with sensitive filenames such as:
   - `salary_plan_2026.xlsx`
   - `executive_contracts.docx`
   - `confidential_budget.txt`
2. Create dummy certificate artifacts for the same user profile.
3. Launch the GUI or CLI.
4. Run the scan.
5. Show:
   - encrypted file findings
   - user artifact roots
   - certificate thumbprints
   - timeline
   - alerts
   - exported PDF report

## Expected Findings

- candidate encrypted files in sensitive paths
- user profile mapped to crypto directories
- certificate artifacts linked to the same user
- suspicious activity alert for executive or payroll files
- chain-of-custody entries showing scan start and completion
