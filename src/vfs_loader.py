"""Загрузка виртуальной файловой системы из CSV."""
import base64
import binascii
import csv
import os
import posixpath

from vfs import VfsError

HEADER = ["path", "type", "content"]
ROOT = "/"


def load_csv(path, vfs_class):
    """Читает CSV, проверяет его и возвращает заполненную VFS."""
    if not os.path.isfile(path):
        raise VfsError(f"файл VFS не найден: {path}")
    vfs = vfs_class(os.path.splitext(os.path.basename(path))[0])
    try:
        with open(path, newline="", encoding="utf-8") as src:
            reader = csv.DictReader(src)
            header = [name.strip() for name in reader.fieldnames or []]
            if header != HEADER:
                raise VfsError(
                    "неверный формат VFS: ожидается заголовок "
                    "path,type,content")
            for lineno, row in enumerate(reader, start=2):
                add_row(vfs, row, lineno)
    except (UnicodeDecodeError, csv.Error) as err:
        raise VfsError(f"неверный формат VFS: {err}")
    return vfs


def add_row(vfs, row, lineno):
    """Проверяет CSV-строку и добавляет описанный ею путь."""
    if None in row or None in row.values():
        raise VfsError(f"строка {lineno}: неверное число столбцов")
    path = posixpath.normpath("/" + row["path"].strip())
    kind = row["type"].strip()
    if path == ROOT:
        raise VfsError(f"строка {lineno}: недопустимый путь")
    if kind not in ("dir", "file"):
        raise VfsError(f"строка {lineno}: неизвестный тип '{kind}'")
    data = b""
    if kind == "file":
        try:
            data = base64.b64decode(row["content"].strip(), validate=True)
        except (binascii.Error, ValueError):
            raise VfsError(
                f"строка {lineno}: содержимое не является base64")
    vfs.add_path(path, kind == "dir", data, lineno)