"""Эмулятор оболочки. Этап 2: конфигурация и скрипт."""
import argparse
import os
import sys

from commands import repl, run_script

EXIT_OK = 0
VFS_HELP = "путь к физическому расположению VFS"


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


def main():
    """Выводит параметры, выполняет скрипт и запускает REPL."""
    args = parse_args()
    print_params(args)
    name = os.path.splitext(os.path.basename(args.vfs))[0] or "vfs"
    prompt = f"user@{name}:/$ "
    if args.script:
        run_script(args.script, prompt)
    repl(prompt)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
