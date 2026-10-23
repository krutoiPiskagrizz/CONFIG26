"""Дерево виртуальной файловой системы."""
from dataclasses import dataclass, field


class VfsError(Exception):
    """Ошибка загрузки VFS."""


@dataclass
class Node:
    """Каталог или файл в виртуальной файловой системе."""
    name: str
    is_dir: bool
    data: bytes = b""
    children: dict = field(default_factory=dict)


class VFS:
    """Виртуальная файловая система, целиком в памяти."""

    def __init__(self, name):
        self.name = name
        self.root = Node("", True)

    @classmethod
    def from_csv(cls, path):
        """Создаёт VFS из CSV-файла."""
        from vfs_loader import load_csv
        return load_csv(path, cls)

    def add_path(self, path, is_dir, data, lineno):
        """Добавляет путь, создавая отсутствующие родительские каталоги."""
        *parents, name = path.strip("/").split("/")
        node = self.root
        for part in parents:
            node = node.children.setdefault(part, Node(part, True))
            if not node.is_dir:
                raise VfsError(f"строка {lineno}: '{part}' - не каталог")
        existing = node.children.get(name)
        if is_dir:
            if existing is not None and not existing.is_dir:
                raise VfsError(
                    f"строка {lineno}: '{path}' уже существует как файл")
            node.children.setdefault(name, Node(name, True))
        else:
            if existing is not None:
                raise VfsError(f"строка {lineno}: '{path}' уже существует")
            node.children[name] = Node(name, False, data)

    def count(self):
        """Возвращает число каталогов и файлов без корня."""
        dirs = files = 0
        stack = [self.root]
        while stack:
            for child in stack.pop().children.values():
                if child.is_dir:
                    dirs += 1
                    stack.append(child)
                else:
                    files += 1
        return dirs, files

    def find(self, abspath):
        """Возвращает элемент по абсолютному пути или None."""
        node = self.root
        for part in [item for item in abspath.split("/") if item]:
            if not node.is_dir or part not in node.children:
                return None
            node = node.children[part]
        return node