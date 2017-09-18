# Special Agent (Datasource) for Amazon RDS Postgres

v1.0 - initial release:
Author: Davide Del Grande <davide.delgrande _ lanewan.it> / <delgrande.davide _ gmail.com>

This special agent replaces the mk_postgres plugin for Amazon RDS, where:
- you can't install anything, let alone cmk plugins
- the database "rdsadmin" is restricted and would give access denied if queried

