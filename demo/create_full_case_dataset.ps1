$base = Join-Path $PSScriptRoot "FullCaseDataset"
$userRoot = Join-Path $base "Users\\employee1"
$docsSensitive = Join-Path $userRoot "Documents\\Sensitive"
$docsFinance = Join-Path $userRoot "Documents\\Finance"
$docsProjects = Join-Path $userRoot "Documents\\Projects"
$cryptoRoot = Join-Path $userRoot "AppData\\Roaming\\Microsoft\\Crypto"
$certRoot = Join-Path $userRoot "AppData\\Roaming\\Microsoft\\SystemCertificates"
$protectRoot = Join-Path $userRoot "AppData\\Roaming\\Microsoft\\Protect"
$notesRoot = Join-Path $base "CaseNotes"

$dirs = @($docsSensitive, $docsFinance, $docsProjects, $cryptoRoot, $certRoot, $protectRoot, $notesRoot)
New-Item -ItemType Directory -Force -Path $dirs | Out-Null

$files = @{
    (Join-Path $docsSensitive "executive_merger_strategy.txt") = "Synthetic executive merger strategy used for forensic EFS validation."
    (Join-Path $docsFinance "payroll_adjustments_2026.csv") = "employee,adjustment`nAamir,15000`nSara,22000`nZoya,30500"
    (Join-Path $docsSensitive "confidential_client_list.txt") = "Customer list placeholder for evidence scanning."
    (Join-Path $docsFinance "finance_sensitive_notes.txt") = "Quarterly notes marked sensitive for artifact correlation testing."
    (Join-Path $docsProjects "incident_response_checklist.txt") = "Plaintext IR checklist to demonstrate mixed evidence."
    (Join-Path $cryptoRoot "userkey.key") = "Synthetic key container placeholder for demo use."
    (Join-Path $cryptoRoot "backupkey.pvk") = "Synthetic PVK placeholder."
    (Join-Path $certRoot "efs_user_cert.cer") = "Synthetic EFS certificate placeholder."
    (Join-Path $certRoot "efs_backup_cert.pfx") = "Synthetic EFS PFX placeholder."
    (Join-Path $protectRoot "sid_mapping.dat") = "Synthetic protect-folder mapping placeholder."
    (Join-Path $notesRoot "scenario.txt") = "Employee encrypted sensitive company files before resignation. Use this dataset for end-to-end testing."
}

foreach ($path in $files.Keys) {
    Set-Content -Encoding UTF8 -Path $path -Value $files[$path]
}

$encryptedTargets = @(
    (Join-Path $docsSensitive "executive_merger_strategy.txt"),
    (Join-Path $docsFinance "payroll_adjustments_2026.csv")
)

$cipherLog = @()
foreach ($file in $encryptedTargets) {
    $cipherLog += "=== Encrypting: $file ==="
    $cipherLog += (cipher /e $file | Out-String)
    $cipherLog += "=== Inspecting: $file ==="
    $cipherLog += (cipher /c $file | Out-String)
}

$thumbprintOutput = cipher /y | Out-String
$metaPath = Join-Path $notesRoot "case_metadata.txt"
$metaBody = @(
    "Full forensic demo dataset generated on: $(Get-Date -Format s)"
    "Case narrative: Insider employee encrypted sensitive financial and executive files using EFS."
    ""
    "Current EFS certificate thumbprint:"
    $thumbprintOutput
    ""
    "Cipher output:"
    $cipherLog
)
Set-Content -Encoding UTF8 -Path $metaPath -Value $metaBody

# Set distinct timestamps for timeline testing.
(Get-Item (Join-Path $docsSensitive "executive_merger_strategy.txt")).CreationTime = "2026-04-20 09:15:00"
(Get-Item (Join-Path $docsSensitive "executive_merger_strategy.txt")).LastWriteTime = "2026-04-20 09:18:00"
(Get-Item (Join-Path $docsFinance "payroll_adjustments_2026.csv")).CreationTime = "2026-04-20 09:22:00"
(Get-Item (Join-Path $docsFinance "payroll_adjustments_2026.csv")).LastWriteTime = "2026-04-20 09:25:00"
(Get-Item (Join-Path $docsSensitive "confidential_client_list.txt")).LastWriteTime = "2026-04-20 10:05:00"
(Get-Item (Join-Path $cryptoRoot "userkey.key")).LastWriteTime = "2026-04-20 09:30:00"
(Get-Item (Join-Path $certRoot "efs_user_cert.cer")).LastWriteTime = "2026-04-20 09:32:00"

Write-Output "Full case dataset created at: $base"
