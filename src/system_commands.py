"""Команды времени, календаря и завершения оболочки."""
import calendar
import datetime
import time

from command_utils import ShellError, check_cal_range, no_args
from command_utils import parse_cal_args
from command_utils import SECONDS_IN_HOUR, SECONDS_IN_MINUTE


def cmd_uptime(shell, args):
    """Показывает время работы эмулятора."""
    no_args("uptime", args)
    secs = int(time.time() - shell.start)
    hours, rest = divmod(secs, SECONDS_IN_HOUR)
    minutes, seconds = divmod(rest, SECONDS_IN_MINUTE)
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f" {now} up {hours:02d}:{minutes:02d}:{seconds:02d}, 1 user")


def cmd_cal(shell, args):
    """Печатает текущий месяц, месяц года или целый год."""
    year, month = parse_cal_args(args)
    check_cal_range(year, month)
    cal = calendar.TextCalendar(calendar.MONDAY)
    print(cal.formatyear(year) if month is None
          else cal.formatmonth(year, month))


def cmd_exit(shell, args):
    """Завершает работу эмулятора."""
    no_args("exit", args)
    shell.running = False