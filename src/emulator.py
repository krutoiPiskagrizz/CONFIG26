"""Точка входа эмулятора оболочки."""
import argparse
import sys

from shell import Shell
from vfs import VFS, VfsError

EXIT_OK = 0
EXIT_VFS_ERROR = 1
VFS_HELP = "путь к CSV-файлу с VFS"


def parse_args():
    """Разбирает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    parser.add_argument("--vfs", required=True, help=VFS_HELP)
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args()


def print_params(args):
    """Печатает заданные параметры запуска."""
    print("[debug] Параметры запуска:")
    print(f"[debug]   vfs    = {args.vfs}")
    print(f"[debug]   script = {args.script}")


def load_vfs(path):
    """Загружает VFS и печатает сводку; None при ошибке."""
    try:
        vfs = VFS.from_csv(path)
    except VfsError as err:
        print(f"Ошибка загрузки VFS: {err}", file=sys.stderr)
        return None
    dirs, files = vfs.count()
    print(f"[debug] VFS '{vfs.name}' загружена: "
          f"каталогов {dirs}, файлов {files}")
    return vfs


def main():
    """Загружает VFS и запускает оболочку."""
    args = parse_args()
    print_params(args)
    vfs = load_vfs(args.vfs)
    if vfs is None:
        return EXIT_VFS_ERROR
    shell = Shell(vfs)
    if args.script:
        shell.run_script(args.script)
    shell.repl()
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
