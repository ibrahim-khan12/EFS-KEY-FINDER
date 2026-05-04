$base = Join-Path $PSScriptRoot "DemoEvidence"
$paths = @(
    "Users\\employee1\\Documents\\Sensitive",
    "Users\\employee1\\Documents\\Payroll",
    "Users\\employee1\\AppData\\Roaming\\Microsoft\\Crypto",
    "Users\\employee1\\AppData\\Roaming\\Microsoft\\Protect",
    "Users\\employee1\\AppData\\Roaming\\Microsoft\\SystemCertificates"
)

foreach ($path in $paths) {
    New-Item -ItemType Directory -Force -Path (Join-Path $base $path) | Out-Null
}

$files = @{
    "Users\\employee1\\Documents\\Sensitive\\confidential_budget.txt" = "Synthetic budget note for demo use only."
    "Users\\employee1\\Documents\\Payroll\\salary_plan_2026.xlsx" = "Demo payroll workbook placeholder."
    "Users\\employee1\\Documents\\Sensitive\\executive_contracts.docx" = "Demo executive contracts placeholder."
    "Users\\employee1\\Documents\\Sensitive\\finance_sensitive_notes.txt" = "Synthetic finance note."
    "Users\\employee1\\AppData\\Roaming\\Microsoft\\SystemCertificates\\efs_user_cert.cer" = "Synthetic certificate bytes placeholder."
    "Users\\employee1\\AppData\\Roaming\\Microsoft\\SystemCertificates\\efs_backup_cert.pfx" = "Synthetic PFX placeholder."
    "Users\\employee1\\AppData\\Roaming\\Microsoft\\Crypto\\userkey.key" = "Synthetic key placeholder."
}

foreach ($relative in $files.Keys) {
    $target = Join-Path $base $relative
    Set-Content -Encoding UTF8 -Path $target -Value $files[$relative]
}

(Get-Item (Join-Path $base "Users\\employee1\\Documents\\Sensitive\\confidential_budget.txt")).CreationTime = "2026-04-15 10:30:00"
(Get-Item (Join-Path $base "Users\\employee1\\Documents\\Payroll\\salary_plan_2026.xlsx")).LastWriteTime = "2026-04-16 11:15:00"
(Get-Item (Join-Path $base "Users\\employee1\\AppData\\Roaming\\Microsoft\\SystemCertificates\\efs_user_cert.cer")).LastWriteTime = "2026-04-16 11:20:00"

Write-Output "Demo dataset created at: $base"
