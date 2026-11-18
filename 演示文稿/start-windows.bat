@echo off
chcp 65001 >nul
title Buffer Pool Replacement Demo - Local Server
cd /d "%~dp0"

rem ===================================================================
rem  One-click launcher for Windows.
rem  Usage: double-click this file, or run in cmd:
rem    start-windows.bat [port]     (default port 8642)
rem  Stop the demo: press Ctrl+C or close this window.
rem ===================================================================

set "PORT=8642"
if not "%~1"=="" set "PORT=%~1"

echo ==========================================================
echo  Buffer Pool Page Replacement Demo (LRU vs LFU)
echo ==========================================================
echo.

rem --- Locate a usable Python launcher ---
where py >nul 2>nul
if %errorlevel%==0 goto :has_py
where python >nul 2>nul
if %errorlevel%==0 goto :has_python

echo [ERROR] Python was not found on this machine.
echo.
echo  Option A: install Python from https://www.python.org/downloads/
echo            (remember to check "Add python.exe to PATH")
echo  Option B: skip the server - just double-click index.html
echo            in this same folder. The page runs fully offline.
echo.
pause
exit /b 1

:has_py
echo [1/2] Opening browser at http://127.0.0.1:%PORT%/index.html ...
start "" "http://127.0.0.1:%PORT%/index.html"
echo [2/2] Local server running. Press Ctrl+C or close this window to stop.
echo.
py -3 -m http.server %PORT% --bind 127.0.0.1
exit /b %errorlevel%

:has_python
echo [1/2] Opening browser at http://127.0.0.1:%PORT%/index.html ...
start "" "http://127.0.0.1:%PORT%/index.html"
echo [2/2] Local server running. Press Ctrl+C or close this window to stop.
echo.
python -m http.server %PORT% --bind 127.0.0.1
exit /b %errorlevel%
