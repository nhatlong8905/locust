set CURDIR=%~dp0
set WORDIR=%CURDIR%
set arg1=%1
set arg2=%2
set arg3=%3
cd /D %WORDIR%
cd /D ../
locust -f api/UserTask.py --csv=report/UserTask --headless -u %arg1% -r %arg2% --run-time %arg3% --master