#!/bin/bash
# Этап 5: команды rm, help; VFS на диске не меняется
# В конце выводится итог: были ли ошибки в самих тестах.
cd "$(dirname "$0")/.."

FAILED=0

# run_test <описание> <код> <текст> <ввод> <запрещённый текст> <args...>
run_test() {
    local title="$1" expected="$2" pattern="$3" input="$4" absent="$5"
    shift 5
    echo "=== $title ==="
    local output
    output=$(printf '%s\n' "$input" | ./run.sh "$@" 2>&1)
    local code=$?
    echo "$output"
    local ok=1
    [ "$code" -eq "$expected" ] || ok=0
    if [ -n "$pattern" ] && ! grep -q -- "$pattern" <<< "$output"; then
        ok=0
    fi
    if [ -n "$absent" ] && grep -Eq -- "$absent" <<< "$output"; then
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

run_test "1. help выводит список команд" 0 "rm \[-r\]" \
    $'help\nexit' "" --vfs vfs/several.csv
run_test "2. rm удаляет файл и каталог" 0 "bin/" \
    $'rm hello.txt\nrm -r docs\nls /\nexit' 'hello.txt|docs/' \
    --vfs vfs/several.csv
run_test "3. Ошибка: каталог без -r" 0 "нужен ключ -r" \
    $'rm docs\nexit' "" --vfs vfs/several.csv
run_test "4. Ошибка: удаление корня" 0 "корневой каталог" \
    $'rm -r /\nexit' "" --vfs vfs/several.csv
run_test "5. Ошибка: удаление текущего каталога" 0 "текущий каталог" \
    $'cd docs\nrm -r .\nexit' "" --vfs vfs/several.csv
run_test "6. Скрипт на глубокой VFS (нет путей - ошибки пропущены)" 0 \
    "ошибка в строке" "exit" "" \
    --vfs vfs/deep.csv --script tests/all_commands.emu
run_test "7. Ошибка загрузки VFS" 1 "не найден" "exit" "" \
    --vfs vfs/missing.csv

echo "=== 8. Файл VFS на диске не изменился после rm ==="
BEFORE=$(cksum < vfs/several.csv)
printf 'rm -r docs\nrm hello.txt\nexit\n' \
    | ./run.sh --vfs vfs/several.csv > /dev/null
AFTER=$(cksum < vfs/several.csv)
if [ "$BEFORE" = "$AFTER" ]; then
    echo ">>> OK (файл не изменился)"
else
    echo ">>> ОШИБКА: файл VFS был изменён"
    FAILED=$((FAILED + 1))
fi
echo

echo "=============================="
if [ "$FAILED" -eq 0 ]; then
    echo "ИТОГ: ошибок нет, все тесты пройдены"
    exit 0
else
    echo "ИТОГ: тестов с ошибками: $FAILED"
    exit 1
fi
