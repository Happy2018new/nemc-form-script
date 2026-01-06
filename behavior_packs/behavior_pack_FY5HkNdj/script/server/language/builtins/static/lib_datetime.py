# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

import datetime
from .lib_object import BaseManager


class TimeDelta:
    """
    TimeDelta 提供了时间差相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 TimeDelta

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def _deref(self, ptr):  # type: (int) -> datetime.timedelta
        """
        _deref 解引用 ptr 指针，并检查所得对象是否是时间差对象。
        如果所得对象是这样的对象，则将其返回，否则抛出对应的错误

        Args:
            ptr (int): 目标对象的指针

        Raises:
            Exception:
                如果目标对象不是时间差对象，
                则抛出相应的错误

        Returns:
            datetime.timedelta: 解引用所得的对象
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.timedelta):
            raise Exception("_deref: Target object is not a timedelta")
        return obj

    def new(
        self,
        days=0.0,  # type: float
        seconds=0.0,  # type: float
        microseconds=0.0,  # type: float
        milliseconds=0.0,  # type: float
        minutes=0.0,  # type: float
        hours=0.0,  # type: float
        weeks=0.0,  # type: float
    ):  # type: (...) -> int
        """
        new 创建并返回一个新的时间差对象

        Args:
            days (float, optional):
                时间差对象的天数。
                默认值为 0.0
            seconds (float, optional):
                时间差对象的秒数。
                默认值为 0.0
            microseconds (float, optional):
                时间差对象的微秒数。
                默认值为 0.0
            milliseconds (float, optional):
                时间差对象的毫秒数。
                默认值为 0.0
            minutes (float, optional):
                时间差对象的分钟数。
                默认值为 0.0
            hours (float, optional):
                时间差对象的小时数。
                默认值为 0.0
            weeks (float, optional):
                时间差对象的周数。
                默认值为 0.0

        Returns:
            int: 新创建的时间差对象的指针
        """
        return self._manager.ref(
            datetime.timedelta(
                days, seconds, microseconds, milliseconds, minutes, hours, weeks
            )
        )

    def format(self, ptr):  # type: (int) -> str
        """
        format 将时间差对象格式化为其字符串表示

        Args:
            ptr (int): 目标时间差对象的指针

        Raises:
            Exception:
                如果目标对象不是时间差对象，
                则抛出相应的错误

        Returns:
            str: 目标时间差对象的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.timedelta):
            raise Exception(
                "datetime_timedelta.format: Target object is not a timedelta"
            )
        return obj.__repr__()

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 datetime_timedelta 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["datetime_timedelta.new"] = self.new
        funcs["datetime_timedelta.format"] = self.format
        funcs["datetime_timedelta.days"] = lambda ptr: self._deref(ptr).days
        funcs["datetime_timedelta.max"] = lambda: self._manager.ref(
            datetime.timedelta.max
        )
        funcs["datetime_timedelta.microseconds"] = lambda ptr: float(
            self._deref(ptr).microseconds
        )
        funcs["datetime_timedelta.min"] = lambda: self._manager.ref(
            datetime.timedelta.min
        )
        funcs["datetime_timedelta.seconds"] = lambda ptr: float(
            self._deref(ptr).seconds
        )
        funcs["datetime_timedelta.total_seconds"] = lambda ptr: float(
            self._deref(ptr).total_seconds()
        )
        funcs["datetime_timedelta.greater"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) > self._deref(ptr_b)
        funcs["datetime_timedelta.less"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) < self._deref(ptr_b)
        funcs["datetime_timedelta.greater_equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) >= self._deref(ptr_b)
        funcs["datetime_timedelta.less_equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) <= self._deref(ptr_b)
        funcs["datetime_timedelta.equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) == self._deref(ptr_b)
        funcs["datetime_timedelta.add"] = lambda ptr_a, ptr_b: self._manager.ref(
            self._deref(ptr_a) + self._deref(ptr_b)
        )
        funcs["datetime_timedelta.remove"] = lambda ptr_a, ptr_b: self._manager.ref(
            self._deref(ptr_a) - self._deref(ptr_b)
        )
        funcs["datetime_timedelta.times"] = lambda ptr, times: self._manager.ref(
            self._deref(ptr) * times
        )
        funcs["datetime_timedelta.divide"] = lambda ptr, divide: self._manager.ref(
            self._deref(ptr) / divide
        )
        funcs["datetime_timedelta.negative"] = lambda ptr: self._manager.ref(
            -self._deref(ptr)
        )
        funcs["datetime_timedelta.abs"] = lambda ptr: self._manager.ref(
            abs(self._deref(ptr))
        )

        for key, value in funcs.items():
            origin[key] = value


class Time:
    """
    Time 基于 datetime 提供了时间相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Time

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def _deref(self, ptr):  # type: (int) -> datetime.time
        """
        _deref 解引用 ptr 指针，并检查所得对象是否是时间对象。
        如果所得对象是这样的对象，则将其返回，否则抛出对应的错误

        Args:
            ptr (int): 目标对象的指针

        Raises:
            Exception:
                如果目标对象不是时间对象，
                则抛出相应的错误

        Returns:
            datetime.time: 解引用所得的对象
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.time):
            raise Exception("_deref: Target object is not a time")
        return obj

    def new(
        self,
        hour=0,  # type: int
        minute=0,  # type: int
        second=0,  # type: int
        microsecond=0,  # type: int
    ):  # type: (...) -> int
        """
        new 创建并返回一个新的时间对象

        Args:
            hour (int, optional):
                时间对象的小时数。
                默认值为 0
            minute (int, optional):
                时间对象的分钟数。
                默认值为 0
            second (int, optional):
                时间对象的秒数。
                默认值为 0
            microsecond (int, optional):
                时间对象的微秒数。
                默认值为 0

        Returns:
            int: 新创建的时间对象的指针
        """
        return self._manager.ref(datetime.time(hour, minute, second, microsecond))

    def format(self, ptr):  # type: (int) -> str
        """
        format 将时间对象格式化为其字符串表示

        Args:
            ptr (int): 目标时间对象的指针

        Raises:
            Exception:
                如果目标对象不是时间对象，
                则抛出相应的错误

        Returns:
            str: 目标时间对象的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.time):
            raise Exception("datetime_time.format: Target object is not a time")
        return obj.__repr__()

    def replace(
        self,
        ptr,  # type: int
        hour=0,  # type: int
        minute=0,  # type: int
        second=0,  # type: int
        microsecond=0,  # type: int
    ):  # type: (...) -> int
        """
        replace 替换时间对象的各个组成部分，
        并返回一个新的时间对象

        Args:
            ptr (int):
                目标时间对象的指针
            hour (int, optional):
                要替换的小时数。
                默认值为 0
            minute (int, optional):
                要替换的分钟数。
                默认值为 0
            second (int, optional):
                要替换的秒数。
                默认值为 0
            microsecond (int, optional):
                要替换的微秒数。
                默认值为 0

        Raises:
            Exception:
                如果目标对象不是时间对象，
                则抛出相应的错误

        Returns:
            int: 替换后所得时间对象的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.time):
            raise Exception("datetime_time.replace: Target object is not a time")
        return self._manager.ref(obj.replace(hour, minute, second, microsecond))

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 datetime_time 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["datetime_time.new"] = self.new
        funcs["datetime_time.format"] = self.format
        funcs["datetime_time.hour"] = lambda ptr: self._deref(ptr).hour
        funcs["datetime_time.isoformat"] = lambda ptr: self._deref(ptr).isoformat()
        funcs["datetime_time.max"] = lambda: self._manager.ref(datetime.time.max)
        funcs["datetime_time.microsecond"] = lambda ptr: self._deref(ptr).microsecond
        funcs["datetime_time.min"] = lambda: self._manager.ref(datetime.time.min)
        funcs["datetime_time.minute"] = lambda ptr: self._deref(ptr).minute
        funcs["datetime_time.replace"] = self.replace
        funcs["datetime_time.second"] = lambda ptr: self._deref(ptr).second
        funcs["datetime_time.strftime"] = lambda ptr, format: self._deref(ptr).strftime(
            format
        )
        funcs["datetime_time.greater"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) > self._deref(ptr_b)
        funcs["datetime_time.less"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) < self._deref(ptr_b)
        funcs["datetime_time.greater_equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) >= self._deref(ptr_b)
        funcs["datetime_time.less_equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) <= self._deref(ptr_b)
        funcs["datetime_time.equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) == self._deref(ptr_b)

        for key, value in funcs.items():
            origin[key] = value


class Date:
    """
    Date 基于 datetime 提供了日期相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Date

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def _deref(self, ptr):  # type: (int) -> datetime.date
        """
        _deref 解引用 ptr 指针，并检查所得对象是否是日期对象。
        如果所得对象是这样的对象，则将其返回，否则抛出对应的错误

        Args:
            ptr (int): 目标对象的指针

        Raises:
            Exception:
                如果目标对象不是日期对象，
                则抛出相应的错误

        Returns:
            datetime.date: 解引用所得的对象
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.date):
            raise Exception("_deref: Target object is not a date")
        return obj

    def new(self, year, month, day):  # type: (int, int, int) -> int
        """
        new 创建并返回一个新的日期对象

        Args:
            year (int): 该日期的年份
            month (int): 该日期的月份
            day (int): 该日期的天数

        Returns:
            int: 新创建的日期对象的指针
        """
        return self._manager.ref(datetime.date(year, month, day))

    def format(self, ptr):  # type: (int) -> str
        """
        format 将日期对象格式化为其字符串表示

        Args:
            ptr (int): 目标日期对象的指针

        Raises:
            Exception:
                如果目标对象不是日期对象，
                则抛出相应的错误

        Returns:
            str: 目标日期对象的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.date):
            raise Exception("datetime_date.format: Target object is not a date")
        return obj.__repr__()

    def replace(self, ptr, year, month, day):  # type: (int, int, int, int) -> int
        """
        replace 替换日期对象的各个组成部分，
        并返回一个新的日期对象

        Args:
            ptr (int): 目标日期对象的指针
            year (int): 要替换的年份
            month (int): 要替换的月份
            day (int): 要替换的天数

        Raises:
            Exception:
                如果目标对象不是日期对象，
                则抛出相应的错误

        Returns:
            int: 替换后所得日期对象的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.date):
            raise Exception("datetime_date.replace: Target object is not a date")
        return self._manager.ref(obj.replace(year, month, day))

    def add_delta(self, date_ptr, timedelta_ptr):  # type: (int, int) -> int
        """
        add_delta 将时间差添加到日期中，
        并返回相加所得的计算结果

        Args:
            date_ptr (int):
                目标日期对象的指针
            timedelta_ptr (int):
                目标时间差对象的指针

        Raises:
            Exception:
                如果 date_ptr 或 timedelta_ptr 指向了不正确的对象，
                则抛出相应的错误

        Returns:
            int: 相加后所得日期对象的指针
        """
        date_obj = self._manager.deref(date_ptr)
        if not isinstance(date_obj, datetime.date):
            raise Exception(
                "datetime_date.add_delta: The given date argument is not a date"
            )
        delta_obj = self._manager.deref(timedelta_ptr)
        if not isinstance(delta_obj, datetime.timedelta):
            raise Exception(
                "datetime_date.add_delta: The given timedelta argument is not a timedelta"
            )
        return self._manager.ref(date_obj + delta_obj)

    def remove_delta(self, date_ptr, timedelta_ptr):  # type: (int, int) -> int
        """
        remove_delta 从日期中减时间差，
        并返回作差所得的计算结果

        Args:
            date_ptr (int): 目标日期对象的指针
            timedelta_ptr (int): 目标时间差对象的指针

        Raises:
            Exception:
                如果 date_ptr 或 timedelta_ptr 指向了不正确的对象，
                则抛出相应的错误

        Returns:
            int: 作差后所得日期对象的指针
        """
        date_obj = self._manager.deref(date_ptr)
        if not isinstance(date_obj, datetime.date):
            raise Exception(
                "datetime_date.add_delta: The given date argument is not a date"
            )
        delta_obj = self._manager.deref(timedelta_ptr)
        if not isinstance(delta_obj, datetime.timedelta):
            raise Exception(
                "datetime_date.add_delta: The given timedelta argument is not a timedelta"
            )
        return self._manager.ref(date_obj - delta_obj)

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 datetime_date 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["datetime_date.new"] = self.new
        funcs["datetime_date.format"] = self.format
        funcs["datetime_date.ctime"] = lambda ptr: self._deref(ptr).ctime()
        funcs["datetime_date.day"] = lambda ptr: self._deref(ptr).day
        funcs["datetime_date.fromordinal"] = lambda n: self._manager.ref(
            datetime.date.fromordinal(n)
        )
        funcs["datetime_date.fromtimestamp"] = lambda timestamp: self._manager.ref(
            datetime.date.fromtimestamp(timestamp)
        )
        funcs["datetime_date.isocalendar"] = lambda ptr: self._manager.ref(
            self._deref(ptr).isocalendar()
        )
        funcs["datetime_date.isoformat"] = lambda ptr: self._deref(ptr).isoformat()
        funcs["datetime_date.isoweekday"] = lambda ptr: self._deref(ptr).isoweekday()
        funcs["datetime_date.max"] = lambda: self._manager.ref(datetime.date.max)
        funcs["datetime_date.min"] = lambda: self._manager.ref(datetime.date.min)
        funcs["datetime_date.month"] = lambda ptr: self._deref(ptr).month
        funcs["datetime_date.replace"] = self.replace
        funcs["datetime_date.strftime"] = lambda ptr, format: self._deref(ptr).strftime(
            format
        )
        funcs["datetime_date.timetuple"] = lambda ptr: self._manager.ref(
            self._deref(ptr).timetuple()
        )
        funcs["datetime_date.today"] = lambda: self._manager.ref(datetime.date.today())
        funcs["datetime_date.toordinal"] = lambda ptr: self._deref(ptr).toordinal()
        funcs["datetime_date.weekday"] = lambda ptr: self._deref(ptr).weekday()
        funcs["datetime_date.year"] = lambda ptr: self._deref(ptr).year
        funcs["datetime_date.greater"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) > self._deref(ptr_b)
        funcs["datetime_date.less"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) < self._deref(ptr_b)
        funcs["datetime_date.greater_equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) >= self._deref(ptr_b)
        funcs["datetime_date.less_equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) <= self._deref(ptr_b)
        funcs["datetime_date.equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) == self._deref(ptr_b)
        funcs["datetime_date.add_delta"] = self.add_delta
        funcs["datetime_date.remove_delta"] = self.remove_delta
        funcs["datetime_date.remove_date"] = lambda ptr_a, ptr_b: self._manager.ref(
            self._deref(ptr_a) - self._deref(ptr_b)
        )

        for key, value in funcs.items():
            origin[key] = value


class DateTime:
    """
    Date 基于 datetime 提供了日期和时间相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 DateTime

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def _deref(self, ptr):  # type: (int) -> datetime.datetime
        """
        _deref 解引用 ptr 指针，并检查所得对象是否是 DateTime。
        如果所得对象是 DateTime，则将其返回，否则抛出对应的错误

        Args:
            ptr (int): 目标对象的指针

        Raises:
            Exception:
                如果目标对象不是 DateTime，
                则抛出相应的错误

        Returns:
            datetime.date: 解引用所得的对象
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.datetime):
            raise Exception("_deref: Target object is not a datetime")
        return obj

    def new(
        self,
        year,  # type: int
        month,  # type: int
        day,  # type: int
        hour=0,  # type: int
        minute=0,  # type: int
        second=0,  # type: int
        microsecond=0,  # type: int
    ):  # type: (...) -> int
        """new 创建并返回一个新的 DateTime

        Args:
            year (int):
                该 DateTime 的年份
            month (int):
                该 DateTime 的月份
            day (int):
                该 DateTime 的天数
            hour (int, optional):
                该 DateTime 的小时数。
                默认值为 0
            minute (int, optional):
                该 DateTime 的分钟数。
                默认值为 0
            second (int, optional):
                该 DateTime 的秒数。
                默认值为 0
            microsecond (int, optional):
                该 DateTime 的微秒数。
                默认值为 0

        Returns:
            int: 新创建的 DateTime 的指针
        """
        return self._manager.ref(
            datetime.datetime(year, month, day, hour, minute, second, microsecond)
        )

    def format(self, ptr):  # type: (int) -> str
        """
        format 将 DateTime 格式化为其字符串表示

        Args:
            ptr (int): 目标 DateTime 的指针

        Raises:
            Exception:
                如果目标对象不是 DateTime，
                则抛出相应的错误

        Returns:
            str: 目标 DateTime 的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.datetime):
            raise Exception("datetime_datetime.format: Target object is not a datetime")
        return obj.__repr__()

    def combine(self, date_ptr, time_ptr):  # type: (int, int) -> int
        """
        combine 将日期和时间组合为一个 DateTime

        Args:
            date_ptr (int): 目标日期的指针
            time_ptr (int): 目标时间的指针

        Raises:
            Exception:
                如果 date_ptr 或 time_ptr 指向了不正确的对象，
                则抛出相应的错误

        Returns:
            int: 组合后所得的 DateTime 的指针
        """
        date_obj = self._manager.deref(date_ptr)
        if not isinstance(date_obj, datetime.date):
            raise Exception(
                "datetime_datetime.combine: The given date argument is not a date"
            )
        delta_obj = self._manager.deref(time_ptr)
        if not isinstance(delta_obj, datetime.time):
            raise Exception(
                "datetime_datetime.combine: The given time argument is not a time"
            )
        return self._manager.ref(datetime.datetime.combine(date_obj, delta_obj))

    def replace(
        self,
        ptr,  # type: int
        year,  # type: int
        month,  # type: int
        day,  # type: int
        hour=0,  # type: int
        minute=0,  # type: int
        second=0,  # type: int
        microsecond=0,  # type: int
    ):  # type: (...) -> int
        """
        replace 替换 DateTime 的各个组成部分，
        并返回一个新的 DateTime

        Args:
            ptr (int):
                目标 DateTime 的指针
            year (int):
                要替换的年份
            month (int):
                要替换的月份
            day (int):
                要替换的天数
            hour (int, optional):
                要替换的小时数。
                默认值为 0
            minute (int, optional):
                要替换的分钟数。
                默认值为 0
            second (int, optional):
                要替换的秒数。
                默认值为 0
            microsecond (int, optional):
                要替换的微秒数。
                默认值为 0

        Raises:
            Exception:
                如果目标对象不是 DateTime，
                则抛出相应的错误

        Returns:
            int: 替换后所得的 DateTime 的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, datetime.datetime):
            raise Exception(
                "datetime_datetime.replace: Target object is not a datetime"
            )
        return self._manager.ref(
            obj.replace(year, month, day, hour, minute, second, microsecond)
        )

    def add_delta(self, datetime_ptr, timedelta_ptr):  # type: (int, int) -> int
        """
        add_delta 将时间差添加到 DateTime 中，
        并返回相加所得的计算结果

        Args:
            datetime_ptr (int):
                目标 DateTime 的指针
            timedelta_ptr (int):
                目标时间差对象的指针

        Raises:
            Exception:
                如果 datetime_ptr 或 timedelta_ptr 指向了不正确的对象，
                则抛出相应的错误

        Returns:
            int: 相加后所得的 DateTime 的指针
        """
        datetime_obj = self._manager.deref(datetime_ptr)
        if not isinstance(datetime_obj, datetime.datetime):
            raise Exception(
                "datetime_datetime.add_delta: The given date argument is not a datetime"
            )
        delta_obj = self._manager.deref(timedelta_ptr)
        if not isinstance(delta_obj, datetime.timedelta):
            raise Exception(
                "datetime_datetime.add_delta: The given timedelta argument is not a timedelta"
            )
        return self._manager.ref(datetime_obj + delta_obj)

    def remove_delta(self, datetime_ptr, timedelta_ptr):  # type: (int, int) -> int
        """
        remove_delta 从 DateTime 中减去指定的时间差，
        并返回作差所得的计算结果

        Args:
            datetime_ptr (int): 目标 DateTime 的指针
            timedelta_ptr (int): 目标时间差对象的指针

        Raises:
            Exception:
                如果 datetime_ptr 或 timedelta_ptr 指向了不正确的对象，
                则抛出相应的错误

        Returns:
            int: 作差后所得的 DateTime 的指针
        """
        datetime_obj = self._manager.deref(datetime_ptr)
        if not isinstance(datetime_obj, datetime.datetime):
            raise Exception(
                "datetime_datetime.add_delta: The given date argument is not a datetime"
            )
        delta_obj = self._manager.deref(timedelta_ptr)
        if not isinstance(delta_obj, datetime.timedelta):
            raise Exception(
                "datetime_datetime.add_delta: The given timedelta argument is not a timedelta"
            )
        return self._manager.ref(datetime_obj - delta_obj)

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 datetime_datetime 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["datetime_datetime.new"] = self.new
        funcs["datetime_datetime.now"] = lambda: self._manager.ref(
            datetime.datetime.now()
        )
        funcs["datetime_datetime.format"] = self.format
        funcs["datetime_datetime.combine"] = self.combine
        funcs["datetime_datetime.ctime"] = lambda ptr: self._deref(ptr).ctime()
        funcs["datetime_datetime.date"] = lambda ptr: self._manager.ref(
            self._deref(ptr).date()
        )
        funcs["datetime_datetime.day"] = lambda ptr: self._deref(ptr).day
        funcs["datetime_datetime.fromordinal"] = lambda n: self._manager.ref(
            datetime.datetime.fromordinal(n)
        )
        funcs["datetime_datetime.fromtimestamp"] = lambda timestamp: self._manager.ref(
            datetime.datetime.fromtimestamp(timestamp)
        )
        funcs["datetime_datetime.hour"] = lambda ptr: self._deref(ptr).hour
        funcs["datetime_datetime.isocalendar"] = lambda ptr: self._manager.ref(
            self._deref(ptr).isocalendar()
        )
        funcs["datetime_datetime.isoformat"] = lambda ptr, sep="T": self._deref(
            ptr
        ).isoformat(sep)
        funcs["datetime_datetime.isoweekday"] = lambda ptr: self._deref(
            ptr
        ).isoweekday()
        funcs["datetime_datetime.max"] = lambda: self._manager.ref(
            datetime.datetime.max
        )
        funcs["datetime_datetime.microsecond"] = lambda ptr: self._deref(
            ptr
        ).microsecond
        funcs["datetime_datetime.min"] = lambda: self._manager.ref(
            datetime.datetime.min
        )
        funcs["datetime_datetime.minute"] = lambda ptr: self._deref(ptr).minute
        funcs["datetime_datetime.month"] = lambda ptr: self._deref(ptr).month
        funcs["datetime_datetime.replace"] = self.replace
        funcs["datetime_datetime.second"] = lambda ptr: self._deref(ptr).second
        funcs["datetime_datetime.strftime"] = lambda ptr, format: self._deref(
            ptr
        ).strftime(format)
        funcs["datetime_datetime.strptime"] = (
            lambda date_string, format: self._manager.ref(
                datetime.datetime.strptime(date_string, format)
            )
        )
        funcs["datetime_datetime.time"] = lambda ptr: self._manager.ref(
            self._deref(ptr).time()
        )
        funcs["datetime_datetime.timetuple"] = lambda ptr: self._manager.ref(
            self._deref(ptr).timetuple()
        )
        funcs["datetime_datetime.today"] = lambda: self._manager.ref(
            datetime.datetime.today()
        )
        funcs["datetime_datetime.toordinal"] = lambda ptr: self._deref(ptr).toordinal()
        funcs["datetime_datetime.weekday"] = lambda ptr: self._deref(ptr).weekday()
        funcs["datetime_datetime.greater"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) > self._deref(ptr_b)
        funcs["datetime_datetime.less"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) < self._deref(ptr_b)
        funcs["datetime_datetime.greater_equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) >= self._deref(ptr_b)
        funcs["datetime_datetime.less_equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) <= self._deref(ptr_b)
        funcs["datetime_datetime.equal"] = lambda ptr_a, ptr_b: self._deref(
            ptr_a
        ) == self._deref(ptr_b)
        funcs["datetime_datetime.add_delta"] = self.add_delta
        funcs["datetime_datetime.remove_delta"] = self.remove_delta
        funcs["datetime_datetime.remove_datetime"] = (
            lambda ptr_a, ptr_b: self._manager.ref(
                self._deref(ptr_a) - self._deref(ptr_b)
            )
        )

        for key, value in funcs.items():
            origin[key] = value
