@echo off
netstat -an | find /C "TIME_WAIT"