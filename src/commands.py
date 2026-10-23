"""Диспетчер команд оболочки."""
import shlex

from command_utils import ShellError
from file_commands import cmd_cd, cmd_ls
from system_commands import cmd_cal, cmd_exit, cmd_uptime

COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "uptime": cmd_uptime,
    "cal": cmd_cal,
    "exit": cmd_exit,
}


def execute(shell, line):
    """Разбирает строку с учётом кавычек и вызывает команду."""
    try:
        argv = shlex.split(line)
    except ValueError as err:
        raise ShellError(f"ошибка разбора: {err}")
    if not argv:
        return
    handler = COMMANDS.get(argv[0])
    if handler is None:
        raise ShellError(f"{argv[0]}: команда не найдена")
    handler(shell, argv[1:])