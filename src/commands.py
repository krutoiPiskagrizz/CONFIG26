"""Диспетчер команд оболочки."""
import shlex

from command_utils import ShellError, no_args
from file_commands import cmd_cd, cmd_ls, cmd_rm
from system_commands import cmd_cal, cmd_exit, cmd_uptime

COMMAND_HELP = {
    "ls": ("ls [-l] [путь...]", "список содержимого каталога"),
    "cd": ("cd [путь]", "сменить каталог"),
    "uptime": ("uptime", "время работы эмулятора"),
    "cal": ("cal [[месяц] год]", "календарь"),
    "rm": ("rm [-r] путь...", "удалить файлы или каталоги"),
    "help": ("help", "список команд с описанием"),
    "exit": ("exit", "выйти из эмулятора"),
}


def cmd_help(shell, args):
    """Выводит список команд с описанием."""
    no_args("help", args)
    for usage, text in COMMAND_HELP.values():
        print(f"  {usage:<22} {text}")


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "uptime": cmd_uptime,
    "cal": cmd_cal,
    "rm": cmd_rm,
    "help": cmd_help,
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