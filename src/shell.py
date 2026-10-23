"""Состояние и интерактивный цикл оболочки."""
import posixpath
import sys
import time

from commands import execute
from command_utils import ShellError

ROOT = "/"


class Shell:
    """Оболочка над VFS с текущим каталогом и временем запуска."""

    def __init__(self, vfs):
        self.vfs = vfs
        self.cwd = ROOT
        self.start = time.time()
        self.running = True

    def prompt(self):
        return f"user@{self.vfs.name}:{self.cwd}$ "

    def abspath(self, path):
        return posixpath.normpath(posixpath.join(self.cwd, path))

    def require(self, path, cmd):
        node = self.vfs.find(self.abspath(path))
        if node is None:
            raise ShellError(
                f"{cmd}: {path}: нет такого файла или каталога")
        return node

    def execute(self, line):
        execute(self, line)

    def run_line(self, line, number):
        if not line.strip() or line.lstrip().startswith("#"):
            return
        try:
            self.execute(line)
        except ShellError as err:
            print(err, file=sys.stderr)
            print(f"[скрипт] ошибка в строке {number}, строка пропущена",
                  file=sys.stderr)

    def run_script(self, path):
        try:
            with open(path, encoding="utf-8") as src:
                lines = src.read().splitlines()
        except OSError as err:
            print(f"Ошибка: не удалось открыть скрипт: {err}",
                  file=sys.stderr)
            return
        for number, line in enumerate(lines, start=1):
            if not self.running:
                break
            print(self.prompt() + line)
            self.run_line(line, number)

    def repl(self):
        while self.running:
            try:
                line = input(self.prompt())
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()
                continue
            try:
                self.execute(line)
            except ShellError as err:
                print(err, file=sys.stderr)