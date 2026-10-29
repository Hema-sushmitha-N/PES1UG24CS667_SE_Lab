param([ValidateSet('line','branch')][string]$Stage)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$Host.UI.RawUI.WindowTitle = "SE Lab6 Evidence - $Stage"
try {
    $buffer = $Host.UI.RawUI.BufferSize
    $buffer.Width = 110
    $buffer.Height = 300
    $Host.UI.RawUI.BufferSize = $buffer
    $window = $Host.UI.RawUI.WindowSize
    $window.Width = 110
    $window.Height = 26
    $Host.UI.RawUI.WindowSize = $window
} catch { }
Clear-Host
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$test = if ($Stage -eq 'line') { 'CodeCoverageTest_coffee_shop_order.py' } else { 'BranchCoverageTest_coffee_shop_order.py' }
$coverageArgs = @('-m','coverage','run',"--data-file=reports/$Stage/.coverage",'--source=coffee_shop_order')
if ($Stage -eq 'branch') { $coverageArgs += '--branch' }
$coverageArgs += @('-m','pytest',$test,'-q','--color=no')
Write-Host "SE Lab 6 | HEMA SUSHMITHA N | PES1UG24CS667"
Write-Host "Stage: $Stage coverage | Application logic unchanged"
Write-Host "Folder: $PSScriptRoot"
Write-Host ''
Write-Host "> python $($coverageArgs -join ' ')"
& $python @coverageArgs
if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
Write-Host ''
Write-Host "> python -m coverage report --data-file=reports/$Stage/.coverage -m"
& $python -m coverage report "--data-file=reports/$Stage/.coverage" -m
if ($LASTEXITCODE -ne 0) { throw 'Coverage report failed' }
Write-Host ''
Write-Host 'Measured application: coffee_shop_order.py only'
Write-Host 'Close this window after capturing the result.'
Read-Host 'Results ready; press Enter to close'
