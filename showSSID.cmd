@echo off

set x=None

@for /f "tokens=1,2,3" %%i in ('netsh WLAN show interfaces') do (

if [%%i]==[SSID] set x=%%k

)
echo %x%