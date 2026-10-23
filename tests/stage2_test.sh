#!/bin/bash
# Этап 2: параметры командной строки и скрипт
# В конце выводится итог: были ли ошибки в самих тестах.
cd "$(dirname "$0")/.."

FAILED=0

# run_test <описание> <ожидаемый код> <ожидаемый текст в выводе> <args...>
# Ввод эмулятору берётся из переменной INPUT (по умолчанию: exit).
run_test() {
    local title="$1" expected="$2" pattern="$3"
    shift 3
    echo "=== $title ==="
    local output
    output=$(printf '%s\n' "${INPUT:-exit}" | ./run.sh "$@" 2>&1)
    local code=$?
    echo "$output"
    local ok=1
    [ "$code" -eq "$expected" ] || ok=0
    if [ -n "$pattern" ] && ! grep -q -- "$pattern" <<< "$output"; then
        ok=0
    fi
    if [ "$ok" -eq 1 ]; then
        echo ">>> OK (код возврата $code)"
    else
        echo ">>> ОШИБКА: ожидался код $expected и текст '$pattern'," \
            "получен код $code"
        FAILED=$((FAILED + 1))
    fi
    echo
}

run_test "1. Только --vfs" 0 "script = None" --vfs vfs/minimal.csv
run_test "2. --vfs и --script" 0 "команда не найдена" \
    --vfs vfs/minimal.csv --script tests/start.emu
run_test "3. Несуществующий скрипт" 0 "не удалось открыть скрипт" \
    --vfs vfs/minimal.csv --script tests/no_such.emu
run_test "4. Нет обязательного --vfs (ожидается ошибка)" 2 "required" \
    --script tests/start.emu

echo "=============================="
if [ "$FAILED" -eq 0 ]; then
    echo "ИТОГ: ошибок нет, все тесты пройдены"
    exit 0
else
    echo "ИТОГ: тестов с ошибками: $FAILED"
    exit 1
fi
