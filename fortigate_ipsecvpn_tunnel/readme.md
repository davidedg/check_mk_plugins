# Fortigate IPSEC VPN Tunnel CheckMK plugin #
----------------------------

Check_MK plugin for Fortigate IPSEC VPN Tunnels (single check per-tunnel)


## Installation ##

As site user, download latest MKP
Install the package.

    $ cmk -vP install fortigate_ipsecvpn_tunnel-<version>.mkp


## Features ##

- A single check will be created for every Phase-2 tunnel.
- Tunnel interface traffic statistics are recorded
- Optionally you can override the state of single VPN tunnels via WATO rules
