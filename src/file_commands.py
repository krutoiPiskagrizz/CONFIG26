"""Команды работы с каталогами и файлами VFS."""
import posixpath

from command_utils import MAX_CD_ARGS, MULTI_PATHS, ShellError
from command_utils import format_entry, listing, split_opts


def cmd_ls(shell, args):
    """Выводит содержимое каталогов или имена файлов."""
    flags, paths = split_opts(args, "l", "ls")
    entries = [(path, shell.require(path, "ls"))
               for path in paths or ["."]]
    last = len(entries) - 1
    for index, (path, node) in enumerate(entries):
        if len(entries) >= MULTI_PATHS:
            print(f"{path}:")
        for label, item in listing(path, node):
            print(format_entry(label, item, "l" in flags))
        if len(entries) >= MULTI_PATHS and index < last:
            print()


def cmd_cd(shell, args):
    """Меняет текущий каталог; без аргумента переходит в корень."""
    if len(args) > MAX_CD_ARGS:
        raise ShellError("cd: слишком много аргументов")
    path = args[0] if args else "/"
    if not shell.require(path, "cd").is_dir:
        raise ShellError(f"cd: {path}: не является каталогом")
    shell.cwd = shell.abspath(path)


def cmd_rm(shell, args):
    """Удаляет файлы и каталоги с ключом -r."""
    flags, paths = split_opts(args, "r", "rm")
    if not paths:
        raise ShellError("rm: не указан операнд")
    for path in paths:
        remove(shell, path, "r" in flags)


def remove(shell, path, recursive):
    """Удаляет элемент VFS после проверки пути и текущего каталога."""
    node = shell.require(path, "rm")
    absolute = shell.abspath(path)
    if absolute == "/":
        raise ShellError("rm: нельзя удалить корневой каталог")
    if node.is_dir and not recursive:
        raise ShellError(f"rm: {path}: это каталог (нужен ключ -r)")
    if shell.cwd == absolute or shell.cwd.startswith(absolute + "/"):
        raise ShellError(f"rm: {path}: это текущий каталог или его родитель")
    parent = shell.vfs.find(posixpath.dirname(absolute))
    del parent.children[node.name]