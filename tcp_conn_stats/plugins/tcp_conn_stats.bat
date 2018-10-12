@echo off
echo ^<^<^<tcp_conn_stats^>^>^>

FOR /F "tokens=* USEBACKQ" %%F IN (`C:\check_mk\netstat_listen.bat`) DO (
SET var=%%F
)
ECHO LISTEN %var%

FOR /F "tokens=* USEBACKQ" %%F IN (`C:\check_mk\netstat_established.bat`) DO (
SET var=%%F
)
ECHO ESTABLISHED %var%

FOR /F "tokens=* USEBACKQ" %%F IN (`C:\check_mk\netstat_wait.bat`) DO (
SET var=%%F
)
ECHO TIME_WAIT %var%
