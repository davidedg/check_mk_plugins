# Fortigate WTP CheckMK plugin #
----------------------------

Check_MK plugin for Fortigate WTP (Managed Access Points)


## Installation ##

As site user, download latest MKP
Install the package.

    $ cmk -vP install fortigate_wtp-<version>.mkp


## Features ##

- A single check will be created for every Access Point
- Performance Metrics: State, CPU, RAM, Traffic In/Out
- Alerts: only on State

## Version 1.3 ##
Compatibility with CheckMK 1.6

## Version 1.2 ##
Removed unused python imports, thanks to Simon Betz

## Version 1.1 ##
Previous version 1.0 failed to work on newer fortigate firmwares
This is tested only on new firmwares (5.4+) 
