@echo off
title QuantumShield 3.0 Starter
cls
echo ===============================
echo     Starte QuantumShield 3.0
echo ===============================
powershell -ExecutionPolicy Bypass -File quantumshield_banner.ps1
python core\quantumshield.py
pause
exit
