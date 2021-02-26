# Notification via Twilio Voice Calls with TwiML Syntax #
---------------------------------------------------------

Check_MK plugin for Notifications via Twilio Programmable Voice


## Installation ##

As site user, download latest MKP
Install the package.

    $ cmk -vP install twilio_voice_twiml-<version>.mkp


## WATO Configuration ##

In WATO, Users, create or modify a user for which you want to enable Voice Notifications, then choose Properties.

Set PAGER ADDRESS with the mobile number, in E.164 format
Example: +393331234567
-> Italy (+39), TIM (333), Number (1234567)


Then enable a Flexible Custom Notification using `Twilio Voice call with TwiML syntax` and configure parameters (activate help for directions).
Note: you may need to certify the phone numbers on the Twilio web console before being able to place calls.