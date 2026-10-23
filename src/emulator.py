"""Эмулятор оболочки. Этап 3: VFS в памяти из CSV."""
import argparse
import os
import sys

from commands import EXIT_OK, repl, run_script
from vfs import VFS, VfsError

EXIT_VFS_ERROR = 1
VFS_HELP = "путь к CSV-файлу с VFS"
def parse_args():
    """Разбирает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    parser.add_argument("--vfs", required=True, help=VFS_HELP)
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args()


def print_params(args):
    """Отладочный вывод всех заданных параметров."""
    print("[debug] Параметры запуска:")
    print(f"[debug]   vfs    = {args.vfs}")
    print(f"[debug]   script = {args.script}")


def load_vfs(path):
    """Загружает VFS и печатает отладочную сводку; None при ошибке."""
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
    """Загружает VFS, выполняет скрипт и запускает REPL."""
    args = parse_args()
    print_params(args)
    vfs = load_vfs(args.vfs)
    if vfs is None:
        return EXIT_VFS_ERROR
    prompt = f"user@{vfs.name}:/$ "
    if args.script:
        run_script(args.script, prompt)
    repl(prompt)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
