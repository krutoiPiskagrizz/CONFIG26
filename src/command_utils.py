"""Общие проверки и форматирование команд."""
import datetime


class ShellError(Exception):
    """Ошибка выполнения команды."""


MAX_CD_ARGS = 1
MULTI_PATHS = 2
YEAR_ONLY = 1
MAX_CAL_ARGS = 2
MIN_YEAR = 1
MAX_YEAR = 9999
FIRST_MONTH = 1
LAST_MONTH = 12
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60


def no_args(cmd, args):
    """Проверяет, что команда вызвана без аргументов."""
    if args:
        raise ShellError(f"{cmd}: команда не принимает аргументов")


def split_opts(args, allowed, cmd):
    """Делит аргументы на ключи и операнды."""
    flags, rest = set(), []
    for arg in args:
        if not arg.startswith("-") or arg == "-":
            rest.append(arg)
            continue
        for char in arg[1:]:
            if char not in allowed:
                raise ShellError(f"{cmd}: неверный ключ -- '{char}'")
            flags.add(char)
    return flags, rest


def listing(path, node):
    """Возвращает пары (подпись, элемент) для ls."""
    if not node.is_dir:
        return [(path, node)]
    items = sorted(node.children.values(), key=lambda item: item.name)
    return [(item.name + ("/" if item.is_dir else ""), item)
            for item in items]


def format_entry(label, node, long_format):
    """Формирует короткую или подробную строку ls."""
    if not long_format:
        return label
    size = 0 if node.is_dir else len(node.data)
    kind = "d" if node.is_dir else "-"
    return f"{kind} {size:>8} {label}"


def parse_cal_args(args):
    """Возвращает год и месяц; None вместо месяца означает весь год."""
    try:
        nums = [int(arg) for arg in args]
    except ValueError:
        raise ShellError("cal: аргументы должны быть числами")
    if len(nums) > MAX_CAL_ARGS:
        raise ShellError("cal: слишком много аргументов")
    today = datetime.date.today()
    if not nums:
        return today.year, today.month
    if len(nums) == YEAR_ONLY:
        return nums[0], None
    month, year = nums
    return year, month


def check_cal_range(year, month):
    """Проверяет допустимость года и месяца."""
    if not MIN_YEAR <= year <= MAX_YEAR:
        raise ShellError(f"cal: неверный год: {year}")
    if month is not None and not FIRST_MONTH <= month <= LAST_MONTH:
        raise ShellError(f"cal: неверный месяц: {month}")