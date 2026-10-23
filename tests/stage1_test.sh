cd "$(dirname "$0")/.."

FAILED=0

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

INPUT=$'ls\ncd /home\nls -l "my folder" file.txt\nexit' \
    run_test "1. Заглушки ls и cd печатают имя и аргументы" 0 "ls \[" 
INPUT=$'ls "my folder" a.txt\nexit' \
    run_test "2. Аргумент в кавычках - один аргумент" 0 "my folder" 
INPUT=$'foo\nexit' \
    run_test "3. Ошибка: неизвестная команда" 0 "команда не найдена" 
INPUT=$'exit extra\nexit' \
    run_test "4. Ошибка: неверные аргументы exit" 0 "не принимает" 
INPUT=$'ls "unclosed\nexit' \
    run_test "5. Ошибка: незакрытая кавычка" 0 "ошибка разбора" 
run_test "6. Приглашение содержит имя VFS" 0 "user@vfs:/\\$"

echo "=============================="
if [ "$FAILED" -eq 0 ]; then
    echo "ИТОГ: ошибок нет, все тесты пройдены"
    exit 0
else
    echo "ИТОГ: тестов с ошибками: $FAILED"
    exit 1
fi
