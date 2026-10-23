"""Реализация команд и общий runtime эмулятора оболочки."""
import shlex
import sys

EXIT_OK = 0

class ShellError(Exception):
    """Ошибка выполнения команды."""

def cmd_ls(args):
    """Заглушка ls: печатает имя команды и аргументы."""
    print("ls", args)

def cmd_cd(args):
    """Заглушка cd: печатает имя команды и аргументы."""
    print("cd", args)

def cmd_exit(args):
    """Завершает работу эмулятора."""
    sys.exit(EXIT_OK)

COMMANDS = {"ls": cmd_ls, "cd": cmd_cd, "exit": cmd_exit}

def execute(line):
    """Разбирает строку (с учётом кавычек) и выполняет команду."""
    try:
        argv = shlex.split(line)
    except ValueError as err:
        raise ShellError(f"ошибка разбора: {err}")
    if not argv:
        return
    name, args = argv[0], argv[1:]
    if name not in COMMANDS:
        raise ShellError(f"{name}: команда не найдена")
    if name == "exit" and args:
        raise ShellError("exit: команда не принимает аргументов")
    COMMANDS[name](args)


def read_line(prompt):
    """Читает строку ввода; None означает конец ввода (Ctrl+D)."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return None
    except KeyboardInterrupt:
        print()
        return ""
def repl(prompt):
    """Интерактивный цикл: ввод команды, выполнение, вывод ошибок."""
    while True:
        line = read_line(prompt)
        if line is None:
            break
        try:
            execute(line)
        except ShellError as err:
            print(err, file=sys.stderr)
def run_line(line, number):
    """Выполняет строку скрипта; ошибочные строки пропускает."""
    if not line.strip() or line.lstrip().startswith("#"):
        return
    try:
        execute(line)
    except ShellError as err:
        print(err, file=sys.stderr)
        print(f"[скрипт] ошибка в строке {number}, строка пропущена",
              file=sys.stderr)
def run_script(path, prompt):
    """Выполняет стартовый скрипт, показывая ввод и вывод как диалог."""
    try:
        with open(path, encoding="utf-8") as src:
            lines = src.read().splitlines()
    except OSError as err:
        print(f"Ошибка: не удалось открыть скрипт: {err}", file=sys.stderr)
        return
    for number, line in enumerate(lines, start=1):
        print(prompt + line)
        run_line(line, number)