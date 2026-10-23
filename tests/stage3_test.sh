#!/bin/bash
# Этап 3: разные варианты VFS и ошибки загрузки
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

run_test "1. Минимальная VFS (один файл)" 0 "каталогов 0, файлов 1" \
    --vfs vfs/minimal.csv
run_test "2. Несколько файлов и папок" 0 "каталогов 2, файлов 4" \
    --vfs vfs/several.csv
run_test "3. Три и более уровней вложенности" 0 "VFS 'deep' загружена" \
    --vfs vfs/deep.csv
run_test "4. Файл VFS не найден (ожидается ошибка)" 1 "не найден" \
    --vfs vfs/missing.csv
run_test "5. Неверный заголовок (ожидается ошибка)" 1 "заголовок" \
    --vfs vfs/bad_header.csv
run_test "6. Неверный base64 (ожидается ошибка)" 1 "base64" \
    --vfs vfs/bad_base64.csv
run_test "7. Стартовый скрипт со всеми командами" 0 "команда не найдена" \
    --vfs vfs/deep.csv --script tests/all_commands.emu

echo "=============================="
if [ "$FAILED" -eq 0 ]; then
    echo "ИТОГ: ошибок нет, все тесты пройдены"
    exit 0
else
    echo "ИТОГ: тестов с ошибками: $FAILED"
    exit 1
fi
