set CURDIR=%~dp0
set WORDIR=%CURDIR%
cd /D %WORDIR%
cd /D ../
locust -f api/UserTask.py