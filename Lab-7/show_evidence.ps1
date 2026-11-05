param([ValidateSet('buggy_app','failing_tests','fixed_app','passing_tests')][string]$Stage)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$Host.UI.RawUI.WindowTitle = "SE Lab7 Evidence - $Stage"
try {
    $buffer = $Host.UI.RawUI.BufferSize
    $buffer.Width = 110
    $buffer.Height = 500
    $Host.UI.RawUI.BufferSize = $buffer
    $window = $Host.UI.RawUI.WindowSize
    $window.Width = 110
    $window.Height = 27
    $Host.UI.RawUI.WindowSize = $window
} catch { }
Clear-Host
$env:PYTHONIOENCODING = 'utf-8'
$env:COLUMNS = '100'
& '.\.venv\Scripts\python.exe' tools\run_evidence.py $Stage --compact
if ($LASTEXITCODE -ne 0) { throw 'Evidence runner failed its expected-outcome check' }
[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot "reports\.ready-$Stage"),'ready')
Read-Host 'Results ready; press Enter to close'
