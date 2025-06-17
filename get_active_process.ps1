Start-Sleep -Seconds 3

Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class Tricks {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
}
"@

$a = [Tricks]::GetForegroundWindow()

Get-Process | Where-Object { $_.MainWindowHandle -eq $a } | ForEach-Object { $_.MainWindowTitle }
