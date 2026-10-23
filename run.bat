@echo off
rem Запуск эмулятора: run.bat --vfs <путь> [--script <путь>]
cd /d "%~dp0"
python src\emulator.py %*
