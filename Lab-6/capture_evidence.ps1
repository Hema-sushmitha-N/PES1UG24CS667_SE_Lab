# Capture actual Windows console windows running the tests, not rendered mockups.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class LabEvidenceWindow {
  public delegate bool Callback(IntPtr window, IntPtr parameter);
  [DllImport("user32.dll")] public static extern bool EnumWindows(Callback callback, IntPtr parameter);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr window, StringBuilder text, int count);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr window);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr window, IntPtr after, int x, int y, int width, int height, uint flags);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr window, int command);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr window, out Rect rectangle);
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr window, uint message, IntPtr wParam, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  public struct Rect { public int Left, Top, Right, Bottom; }
}
'@
[LabEvidenceWindow]::SetProcessDPIAware() | Out-Null
foreach ($stage in @('line','branch')) {
    $displayScript = Join-Path $PSScriptRoot 'show_evidence.ps1'
    $arguments = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$displayScript`" -Stage $stage"
    $consoleProcess = Start-Process -FilePath "$env:WINDIR\System32\conhost.exe" -ArgumentList $arguments -PassThru
    Start-Sleep -Seconds 4
    $script:evidenceHandle = [IntPtr]::Zero
    $expectedTitle = "SE Lab6 Evidence - $stage"
    [LabEvidenceWindow]::EnumWindows({
        param($window, $parameter)
        $title = New-Object System.Text.StringBuilder 512
        [LabEvidenceWindow]::GetWindowText($window, $title, 512) | Out-Null
        if ($title.ToString() -eq $expectedTitle) { $script:evidenceHandle = $window; return $false }
        return $true
    }, [IntPtr]::Zero) | Out-Null
    if ($script:evidenceHandle -eq [IntPtr]::Zero) { throw "Cannot find console: $expectedTitle" }
    [LabEvidenceWindow]::ShowWindow($script:evidenceHandle, 9) | Out-Null
    [LabEvidenceWindow]::SetForegroundWindow($script:evidenceHandle) | Out-Null
    [LabEvidenceWindow]::SetWindowPos($script:evidenceHandle, [IntPtr](-1), 0, 0, 0, 0, 0x0043) | Out-Null
    Start-Sleep -Seconds 2
    $rectangle = New-Object LabEvidenceWindow+Rect
    [LabEvidenceWindow]::GetWindowRect($script:evidenceHandle, [ref]$rectangle) | Out-Null
    $bitmap = New-Object System.Drawing.Bitmap ($rectangle.Right-$rectangle.Left),($rectangle.Bottom-$rectangle.Top)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.CopyFromScreen($rectangle.Left,$rectangle.Top,0,0,$bitmap.Size)
        $target = Join-Path $PSScriptRoot "reports\$stage\terminal_screenshot.png"
        $bitmap.Save($target,[System.Drawing.Imaging.ImageFormat]::Png)
        Write-Output "Captured $target"
    } finally {
        $graphics.Dispose()
        $bitmap.Dispose()
        [LabEvidenceWindow]::PostMessage($script:evidenceHandle, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
    }
}
