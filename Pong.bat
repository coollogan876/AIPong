@echo off
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Python...

    bitsadmin /transfer PythonInstallerJob /download /priority normal https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe %CD%\python-installer.exe

    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    del python-installer.exe
    echo Python installed successfully.
) else (
    echo Python is already installed.
)

python StupidChatGPTThing.py
