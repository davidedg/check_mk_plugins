register_check_parameters(
    subgroup_networking,
    "fortigate_ipsecvpn_tunnel",
    _("Fortigate VPN Tunnel"),
    Dictionary(
        elements = [
            ( "tunnels",
              ListOf(
                  Tuple(
                      title = ("VPN Tunnel Endpoints"),
                      elements = [
                      TextAscii(
                          title = _("Name of Phase-2 tunnel"),
                          help = _("The configured value must match a Phase-2 tunnel."),
                          allow_empty = False,
                      ),
                      MonitoringState(
                          default_value = 2,
                          title = _("Report the tunnel always with this state"),
                          )]),
                  add_label = _("Add tunnel"),
                  movable = False,
                  title = _("VPN tunnel specific configuration"),
                  )),
            ( "missingstate",
              MonitoringState(
                  title = _("Default state to report when tunnel can not be found anymore"),
                  help = _("Default state if a tunnel, which is not listed above in this rule, "
                           "can no longer be found."),
                  ),
            ),
        ],
    ),
    TextAscii( title = _("Name of Phase-2 tunnel")),
    match_type = "dict",
)