# VEEAM Plugin for Check_MK

v1.0 - initial release:
Author: Davide Del Grande <davide.delgrande _ lanewan.it> / <delgrande.davide _ gmail.com>
Based on original veeam_backup_status.ps1 in Check_MK 1.2.6p2

Enhancements over the original plugin:
- Supports "retried" jobs by searching all sessions started within last $HoursToCheck hours
- No Duplicates: a VM is reported only ONCE, even if it's in multiple Jobs (most recent state)
- VMs are reported based on session Creationtime rather than EndTime (most recent snapshot creation = more recent data)

v1.1 - fixes:
- Enhancements to PS console, taken from original plugin in Check_MK 1.2.6p12
- Fixed broken output on some non-english systems (time separator)
- Spaces in VM names are now replaced with underscores, to behave better together with VMWare checks

v1.2 - fixes:
- Now supports "retrying" jobs by ignoring JOBs/VMs if they are going to be retried.
  For a VM, its previous backup state will be reported.
  For a JOB, it will be reported as "Working" until its last retry

v1.3 - fixes:
- VMs backup state was uncorreclty reported also for Backup Copy Jobs, together with Backup Jobs

v1.4 - Compatibility with Veeam 9.5U3:
- Added support for changed attributes Progress.StartTimeLocal and Progress.StopTimeLocal
