@ECHO OFF
REM version 1.1
REM Put this file in cmk Plugins-Folder *only* if you need to run
REM the veeam_backup_status_v2.ps1 powershell script and you
REM have no 64 bit check_mk agent available
REM In this case the powershell script needs to be put somewhere else
REM (see example here) and is called from this .bat script with the 64 bit powershell
%systemroot%\sysnative\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Unrestricted " & ""C:\check_mk\veeam_backup_status_v2.ps1"""
