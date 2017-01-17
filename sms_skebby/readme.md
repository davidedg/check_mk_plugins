# SMS Skebby Notifications #
----------------------------

Check_MK plugin for SMS Notifications via Skebby.it


## Installation ##

As site user, download latest MKP
Install the package.

    $ cmk -vP install sms_skebby-<version>.mkp


## WATO Configuration ##

In WATO, Users, create or modify a user for which you want to enable SMS Notifications, then choose Properties.

Set PAGER ADDRESS with the mobile number, without '+' or '00'.
Example: 393331234567
-> Italy (+39), TIM (333), Number (1234567)

You can also specify multiple addresses, separated by comma


Then enable a Flexible Custom Notification using `SMS using Skebby.it via https` and use these parameters:

Parameter | Value
------------- | -------------
Username | Your Skebby.it username
Password | Your Skebby.it password
SMS Type (optional) | One of: *send_sms, send_sms_basic, `send_sms_classic`, send_sms_classic_report, test_send_sms_classic, test_send_sms_classic_report, test_send_sms_basic*
