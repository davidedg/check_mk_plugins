# This powershell script needs to be run with the 64bit powershell
# and thus from a 64bit check_mk agent
# If a 64 bit check_mk agent is available it just needs to be renamed with
# the extension .ps1
# If only a 32bit  check_mk agent is available it needs to be relocated to a
# directory given in veeam_backup_status.bat and the .bat file needs to be
# started by the check_mk agent instead.

# v1.0
# Author: Davide Del Grande <davide.delgrande _ lanewan.it> / <delgrande.davide _ gmail.com>
# Based on original veeam_backup_status.ps1 in Check_MK 1.2.6p2
# Enhancements over the original plugin:
# - Supports "retried" jobs by searching all sessions started within last $HoursToCheck hours
# - No Duplicates: a VM is reported only ONCE, even if it's in multiple Jobs (most recent state)
# - VMs are reported based on session Creationtime rather than EndTime (most recent snapshot creation = more recent data)


# The script will check ALL Sessions that have been *STARTED* by ENABLED backups within last $HoursToCheck:
# This will still honour the warning/critical thresholds implemented on the check_mk side
$HoursToCheck = 168 # change this at your needs.

# If True, it will include Jobs' LAST SESSION, even if it falls outside $HoursToCheck search window
# This mimics the original plugin behaviour
$AlwaysIncludeLastSession = $True

# Load Veeam Backup and Replication Powershell Snapin
$snapin="VeeamPSSnapIn"
if (-not (Get-PSSnapin $snapin -ErrorAction "SilentlyContinue"))
{
	if (Get-PSSnapin $snapin -registered -ErrorAction "SilentlyContinue") {
		Add-PSSnapin $snapin -ErrorAction "SilentlyContinue"
	}
	else {
		Write-Error "VeeamPSSnapIn NOT REGISTERED"
	}
}

# Error Handling is still poor - just catch for totally unexpected errors.
# If any error occurs during check, a field might just remain blank

try {

# Get a list of SCHEDULED JOBS and convert it to a null-HASH (used just for comparison)
$ScheduledJobs_H=@{}
$ScheduledJobs = Get-VBRJob | Where-Object {$_.IsScheduleEnabled -eq $true}
$ScheduledJobs | ForEach-Object { $ScheduledJobs_H[$_.Id] = $null }

# Get a list of all Backup Sessions STARTED within last $HoursToCheck, which also come from SCHEDULED Backups
$Sessions = Get-VBRBackupSession | Where-Object {($_.JobType -eq "Backup") -and ($_.CreationTime -ge (Get-Date).addhours(-$HoursToCheck)) -and ($ScheduledJobs_H.ContainsKey($_.JobId) )}

# Include Last Session from all backup jobs even if it falls outside search time window
if ($AlwaysIncludeLastSession -eq $True){
	$ScheduledJobs | ForEach-Object{
		$Sessions += ($_.FindLastSession())
	}
}

# SORT Sessions BY CreationTime (latest first), to speedup later $vms hash processing
$Sessions = $Sessions | Sort-Object -Descending CreationTime

# Get a list ALL TASKS (VMs) processed in searched sessions
$SessionsTasks=$Sessions|Get-VBRTaskSession

# Now keep a UNIQUE list of VMs with their MOST RECENT STATUS (whose backup snapshot started more recently)
# key=VM-NAME -> value=Veeam.Backup.Core.CBackupTaskSession
$vms=@{}
$SessionsTasks | ForEach-Object {
	if ($vms.ContainsKey($_.Name)) {
		if ($_.Progress.StartTime -gt $vms[$_.Name].Progress.StartTime) { # Having sorted before, this will seldom execute
			$vms[$_.Name] = $_ 	# Overwrite with most recent one
		}
	}
	else {
		$vms.Add($_.Name, $_)	# Add VM to hash
	}
}


#####################################
# NOW FORMAT THE OUTPUT FOR CHECK_MK
#####################################

# Backup Jobs Section
$myJobsText = "<<<veeam_jobs:sep(9)>>>`n" # Create new text string for backup job section. Initialize it with header
$ScheduledJobs | ForEach-Object {
	$myJobLastState = $_.GetLastState()
	$myJobLastResult = $_.GetLastResult()
	$myJobLastSession = $_.FindLastSession()
	$myJobCreationTime = $myJobLastSession.CreationTime |  get-date -Format "dd.MM.yyyy HH:mm:ss"  -ErrorAction SilentlyContinue
	$myJobEndTime = $myJobLastSession.EndTime |  get-date -Format "dd.MM.yyyy HH:mm:ss"  -ErrorAction SilentlyContinue
	$myJobsText = $myJobsText + $_.Name + "`t" + $_.JobType + "`t" + $myJobLastState + "`t" + $myJobLastResult + "`t" + $myJobCreationTime + "`t" + $myJobEndTime + "`n"
}

# VM Section
$myTaskText = "" # Create new text string for backup tasks section.
# $vms.GetEnumerator() | Sort-Object Name | ForEach-Object { ## For DEBUG purposes, you may want to sort output by VM (hash key name)
$vms.GetEnumerator() | ForEach-Object {
	$myTaskStartTime = $_.value.Progress.StartTime |  get-date -Format "dd.MM.yyyy HH:mm:ss"  -ErrorAction SilentlyContinue
	$myTaskStopTime = $_.value.Progress.StopTime |  get-date -Format "dd.MM.yyyy HH:mm:ss"  -ErrorAction SilentlyContinue
	# Result is a value of type System.TimeStamp. I'm sure there is a more elegant way of formatting the output:
	$myTaskDuration = "{0:D2}" -f $_.value.Progress.duration.Days + ":" + "{0:D2}" -f $_.value.Progress.duration.Hours + ":" + "{0:D2}" -f $_.value.Progress.duration.Minutes + ":" + "{0:D2}" -f $_.value.Progress.duration.Seconds

	$myTaskText = $myTaskText + "<<<<" + $_.value.Name + ">>>>" + "`n"
	$myTaskText = $myTaskText + "<<<"+ "veeam_client:sep(9)" +">>>" +"`n"
	$myTaskText = $myTaskText + "Status" + "`t" + $_.value.Status + "`n"
	$myTaskText = $myTaskText + "JobName" + "`t" + $_.value.JobSess.OrigJobName + "`n"
	$myTaskText = $myTaskText + "TotalSizeByte" + "`t" + $_.value.Progress.TotalSize + "`n"
	$myTaskText = $myTaskText + "ReadSizeByte" + "`t" + $_.value.Progress.ReadSize + "`n"
	$myTaskText = $myTaskText + "TransferedSizeByte" + "`t" + $_.value.Progress.TransferedSize + "`n"
	$myTaskText = $myTaskText + "StartTime" + "`t" + $myTaskStartTime + "`n"
	$myTaskText = $myTaskText + "StopTime" + "`t" + $myTaskStopTime + "`n"
	$myTaskText = $myTaskText + "DurationDDHHMMSS" + "`t" + $myTaskDuration + "`n"
	$myTaskText = $myTaskText + "AvgSpeedBps" + "`t" + $_.value.Progress.AvgSpeed + "`n"
	$myTaskText = $myTaskText + "DisplayName" + "`t" + $_.value.Progress.DisplayName + "`n"

	# End of section <<<veeam.client>>>
	$myTaskText = "$myTaskText" + "<<<<" + ">>>>" +"`n"
}

# Final output
Write-host $myJobsText
Write-host $myTaskText
} # END OF TRY BLOCK

# CATCH only totally impossible catastrophic errors
catch
{
$errMsg = $_.Exception.Message
$errItem = $_.Exception.ItemName
Write-Error "Totally unexpected and unhandled error occured:`n Item: $errItem`n Error Message: $errMsg"
Break
}
