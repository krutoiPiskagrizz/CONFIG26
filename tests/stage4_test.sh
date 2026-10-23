#!/bin/bash
# Этап 4: команды ls, cd, uptime, cal
# В конце выводится итог: были ли ошибки в самих тестах.
cd "$(dirname "$0")/.."

FAILED=0

# run_test <описание> <код> <текст> <ввод> <args...>
run_test() {
    local title="$1" expected="$2" pattern="$3" input="$4"
    shift 4
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
    if [ "$ok" -eq 1 ]; then
        echo ">>> OK (код возврата $code)"
    else
        echo ">>> ОШИБКА: ожидался код $expected и текст '$pattern'," \
            "получен код $code"
        FAILED=$((FAILED + 1))
    fi
    echo
}

run_test "1. Команды этапа 4, глубокая VFS" 0 "projects/" \
    $'ls /home/user\nls -l /home/user/projects/app/main.py\ncd /home/user/projects\nls\nexit' \
    --vfs vfs/deep.csv
run_test "2. Календарь cal 2 2024" 0 "February 2024" \
    $'cal 2 2024\nexit' --vfs vfs/deep.csv
run_test "3. Ошибка ls: нет такого пути" 0 "ls: nonexistent: нет" \
    $'ls nonexistent\nexit' --vfs vfs/several.csv
run_test "4. Ошибка cd: это не каталог" 0 "не является каталогом" \
    $'cd /home/user/projects/app/main.py\nexit' --vfs vfs/deep.csv
run_test "5. Команды на минимальной VFS" 0 "up 00:" \
    $'uptime\ncal 2 2024\nexit' --vfs vfs/minimal.csv
run_test "6. Ошибка загрузки VFS" 1 "не найден" "exit" \
    --vfs vfs/missing.csv

echo "=============================="
if [ "$FAILED" -eq 0 ]; then
    echo "ИТОГ: ошибок нет, все тесты пройдены"
    exit 0
else
    echo "ИТОГ: тестов с ошибками: $FAILED"
    exit 1
fi
