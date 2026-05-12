@echo off
cd /d "C:\Dev\Agente007"
echo.
echo  1. Bakunin (tecnico - wake word: "Bakunin")
echo  2. Durruti (CEO FORRARSE - wake word: "Durruti")
echo.
set /p opcion="Elige 1 o 2: "
if "%opcion%"=="1" uv run python scripts/bakunin_escucha.py
if "%opcion%"=="2" uv run python scripts/durruti_escucha.py
pause
