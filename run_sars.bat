@echo off
cd /d %~dp0

echo ==============================
echo  SARS ONE CLICK RUNNER
echo ==============================

py run_sars.py

echo.
echo Done. Press any key to close.
pause >nul