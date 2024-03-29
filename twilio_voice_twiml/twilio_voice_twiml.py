#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://github.com/davidedg/check_mk_plugins
__author__ = 'DavideDG'
__version__ = '2.0.0'

#import socket

#import cmk.utils.version as cmk_version
#import cmk.gui.config as config
from cmk.gui.i18n import _
#from cmk.gui.globals import html
from cmk.gui.valuespec import (
#    Age,
#    Alternative,
    CascadingDropdown,
#    DEF_VALUE,
    Dictionary,
    DropdownChoice,
#    EmailAddress,
#    FixedValue,
#    HTTPUrl,
#    Integer,
#    IPv4Address,
#    ListChoice,
#    ListOfStrings,
    Password,
#    TextAreaUnicode,
    TextAscii,
#    TextUnicode,
#    Transform,
#    Tuple,
)

from cmk.gui.plugins.wato import (
    notification_parameter_registry,
    NotificationParameter,
    passwordstore_choices,
)

#from cmk.gui.plugins.wato.utils import (
#    PasswordFromStore,)


@notification_parameter_registry.register
class NotificationParameterTwilioVoiceTWIML(NotificationParameter):
    @property
    def ident(self):
        return "twilio_voice_twiml"

    @property
    def spec(self):
        return Dictionary(
            title=_("Create notification with the following parameters:"),
            elements=[
                ("credentials", CascadingDropdown(
                    title=_("Twilio Credentials"),
                    help=_("Please provide <a href=\"https://www.twilio.com\" target=\"_blank\">Twilio</a> project account credentials"),
                    choices=[("plain", _("Credentials in format 'account_sid:auth_token'"),
                              Password(
                                  size=67,
                                  regex="^AC[0-9,a-z]{32}:[0-9,a-z]{32}$",
                                  regex_error=_("Twilio credentials format: ACCOUNT_SID:AUTH_TOKEN")
                              )),
                             ("env",
                              _("Credentials from Environment Variables: 'TWILIO_ACCOUNT_SID' and 'TWILIO_AUTH_TOKEN'")),
                             ("jsonstore", _("Credentials from json store: ~/.twilio.secrets  -- see context help --"),
                              TextAscii(
                                  help=_(
                                      "The name of the json profile to load from <b>~/.twilio.secrets</b><br>Example file:"
                                      "<tt>"
                                      "<br>" "{"
                                      "<br>" "&nbsp;&nbsp;\"profilename01\": {"
                                      "<br>" "&nbsp;&nbsp;&nbsp;&nbsp;\"account_sid\": \"AC0123456789abcdef0123456789abcdef\","
                                      "<br>" "&nbsp;&nbsp;&nbsp;&nbsp;\"auth_token\": \"abcdef0123456789abcdef0123456789\""
                                      "<br>" "&nbsp;&nbsp;},"
                                      "<br>" "&nbsp;&nbsp;\"profilename02\": {"
                                      "<br>" "&nbsp;&nbsp;&nbsp;&nbsp;\"account_sid\": \"AC1123456789abcdef0123456789abcde0\","
                                      "<br>" "&nbsp;&nbsp;&nbsp;&nbsp;\"auth_token\": \"dbcdef0123456789abcdef0123456789\""
                                      "<br>" "&nbsp;&nbsp;}"
                                      "<br>" "}"
                                      "</tt>"
                                  ))),
                             ("store",
                              _("Credentials in format 'account_sid:auth_token' retrieved from CMK password store"),
                              DropdownChoice(sorted=True, choices=passwordstore_choices))],
                )),
                ("source_phone", TextAscii(
                    title=_("Originating Phone Number"),
                    help=_("Originating Phone Number (must be first validated in Twilio), in <a href=\"https://www.twilio.com/docs/glossary/what-e164\" target=\"_blank\">E.164 format</a>"),
                    regex="^\+[1-9]\d{1,14}$",
                    regex_error=_("Phone Number must conform to E.164 format"),
                    size=20
                )),
                ("twilio_params", TextAreaUnicode(
                    title=_("Twilio Programmable Voice Request Parameters"),
                    monospaced=True,
                    cols=80,
                    rows=8,
                    default_value="record=false\ntwiml=<Response><Say>Please check monitoring system.</Say></Response>",
                    help=_(
                        "See <a href=\"https://www.twilio.com/docs/voice/twiml#request-parameters\" target=\"_blank\">Twilio Docs</a>."
                        "<br>" "Note: these Request Parameters must not be specified here: <tt>From, To, AccountSid</tt>"
                        "<br>" "Example:"
                        "<br>" "<tt>twiml=<Response><Say>Ahoy there!</Say></Response>,record=true</tt>"
                        "<br>For the <b><tt>twiml</tt></b> block syntax, consult <a href=\"https://www.twilio.com/docs/voice/twiml\" target=\"_blank\">Twilio Markup Language</a>"
                    ),

                )),
            ]
        )
