#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "datasource_programs"

register_rule(group,
    "special_agents:rdspostgres",
    Dictionary(
        title=_("Amazon RDS Postgres"),
        elements=[
               ('username', TextAscii(title=_("Username"))),
               ('password', Password(title=_("Password"))),
        ],
        optional_keys = None,
    ),
)
