#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule("datasource_programs",
    "special_agents:rdspostgres",
    Tuple(
        title = _("Amazon RDS Postgres"),
        help = _( "Monitoring of Amazon AWS RDS Postgres"),
        elements = [
           TextAscii(title = _("Username")),
           Password( title = _("Password")),
        ]
    ),
    factory_default = Rulespec.FACTORY_DEFAULT_UNUSED,
    match = "first")
