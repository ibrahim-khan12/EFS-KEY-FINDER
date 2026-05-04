$base = Join-Path $PSScriptRoot "RealEfsDataset"
$secureDir = Join-Path $base "Users\\employee1\\Documents\\EfsConfirmed"
$mixedDir = Join-Path $base "Users\\employee1\\Documents\\MixedEvidence"
$notesDir = Join-Path $base "CaseNotes"

New-Item -ItemType Directory -Force -Path $secureDir, $mixedDir, $notesDir | Out-Null

$plainFiles = @{
    (Join-Path $secureDir "executive_merger_strategy.txt") = "Confidential merger strategy. This file is intended for real EFS demo testing."
    (Join-Path $secureDir "payroll_adjustments_2026.csv") = "employee,adjustment`nAamir,15000`nSara,22000"
    (Join-Path $mixedDir "incident_response_checklist.txt") = "This file remains plaintext to show mixed evidence in the same case."
    (Join-Path $notesDir "dataset_overview.txt") = "Real EFS dataset generated for authorized forensic coursework."
}

foreach ($path in $plainFiles.Keys) {
    Set-Content -Encoding UTF8 -Path $path -Value $plainFiles[$path]
}

$filesToEncrypt = @(
    (Join-Path $secureDir "executive_merger_strategy.txt"),
    (Join-Path $secureDir "payroll_adjustments_2026.csv")
)

$cipherOutput = @()
foreach ($file in $filesToEncrypt) {
    $cipherOutput += "=== Encrypting: $file ==="
    $cipherOutput += (cipher /e $file | Out-String)
    $cipherOutput += "=== Inspecting: $file ==="
    $cipherOutput += (cipher /c $file | Out-String)
}

$thumbprintOutput = cipher /y | Out-String
$metaPath = Join-Path $notesDir "efs_runtime_metadata.txt"
$metaBody = @(
    "Real EFS dataset generated on: $(Get-Date -Format s)"
    "Host user certificate info:"
    $thumbprintOutput
    ""
    "Cipher verification output:"
    $cipherOutput
)
Set-Content -Encoding UTF8 -Path $metaPath -Value $metaBody

Write-Output "Real EFS dataset created at: $base"
