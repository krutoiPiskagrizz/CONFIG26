#!/bin/bash
# Запуск эмулятора: ./run.sh --vfs <путь> [--script <путь>]
cd "$(dirname "$0")"
python3 src/emulator.py "$@"
