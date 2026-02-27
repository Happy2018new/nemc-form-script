# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

import time
from .lib_object import BaseManager


class StructTime:
    """
    StructTime 提供了对 struct_time 的内置操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 StructTime

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def cast(self, ptr):  # type: (int) -> int
        """
        cast 将 ptr 指向的对象强制转换为 StructTime

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int: 强制转换后所得 StructTime 的指针
        """
        return self._manager.ref(time.struct_time(self._manager.deref(ptr)))

    def _deref(self, ptr):  # type: (int) -> time.struct_time
        """
        _deref 解引用 ptr 指针，并检查所得对象是否是 StructTime。
        如果所得对象是 StructTime，则将其返回，否则抛出对应的错误

        Args:
            ptr (int): 目标对象的指针

        Raises:
            Exception:
                如果目标对象不是 StructTime，
                则抛出相应的错误

        Returns:
            time.struct_time: 解引用所得的对象
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, time.struct_time):
            raise Exception("_deref: Target object is not a struct_time")
        return obj

    def length(self, ptr):  # type: (int) -> int
        """length 返回 StructTime 的长度

        Args:
            ptr (int): 目标 StructTime 的指针

        Raises:
            Exception:
                如果目标对象不是 StructTime，
                则抛出相应的错误

        Returns:
            int: 目标 StructTime 的长度
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, time.struct_time):
            raise Exception("struct_time.length: Target object is not a struct_time")
        return len(obj)

    def format(self, ptr):  # type: (int) -> str
        """format 将 StructTime 格式化为其字符串表示

        Args:
            ptr (int): 目标 StructTime 的指针

        Raises:
            Exception:
                如果目标对象不是 StructTime，
                则抛出相应的错误

        Returns:
            str: 目标 StructTime 的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, time.struct_time):
            raise Exception("struct_time.format: Target object is not a struct_time")
        return obj.__repr__()

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 struct_time 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["struct_time.cast"] = self.cast
        funcs["struct_time.length"] = self.length
        funcs["struct_time.format"] = self.format
        funcs["struct_time.tm_year"] = lambda ptr: self._deref(ptr).tm_year
        funcs["struct_time.tm_mon"] = lambda ptr: self._deref(ptr).tm_mon
        funcs["struct_time.tm_mday"] = lambda ptr: self._deref(ptr).tm_mday
        funcs["struct_time.tm_hour"] = lambda ptr: self._deref(ptr).tm_hour
        funcs["struct_time.tm_min"] = lambda ptr: self._deref(ptr).tm_min
        funcs["struct_time.tm_sec"] = lambda ptr: self._deref(ptr).tm_sec
        funcs["struct_time.tm_wday"] = lambda ptr: self._deref(ptr).tm_wday
        funcs["struct_time.tm_yday"] = lambda ptr: self._deref(ptr).tm_yday
        funcs["struct_time.tm_isdst"] = lambda ptr: self._deref(ptr).tm_isdst

        for key, value in funcs.items():
            origin[key] = value


class Time:
    """
    Time 提供了对时间的内置操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Time

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def asctime(self, ptr):  # type: (int) -> str
        """
        asctime converts a time tuple to a string, e.g. 'Sat Jun 06 16:26:11 1998'.
        When the time tuple is not present, current time as returned by localtime()
        is used.

        Args:
            ptr (int): The pointer points to the target StructTime

        Returns:
            str: The formatted time string
        """
        if ptr == 0:
            return time.asctime()
        return time.asctime(self._manager.deref(ptr))

    def strftime(self, format, ptr):  # type: (str, int) -> str
        """
        strftime converts a time tuple to a string according to a format specification.
        See the library reference manual for formatting codes. When the time tuple is
        not present, current time as returned by localtime() is used.

        Commonly used format codes:
            - %Y Year with century as a decimal number.
            - %m Month as a decimal number [01,12].
            - %d Day of the month as a decimal number [01,31].
            - %H Hour (24-hour clock) as a decimal number [00,23].
            - %M Minute as a decimal number [00,59].
            - %S Second as a decimal number [00,61].
            - %z Time zone offset from UTC.
            - %a Locale's abbreviated weekday name.
            - %A Locale's full weekday name.
            - %b Locale's abbreviated month name.
            - %B Locale's full month name.
            - %c Locale's appropriate date and time representation.
            - %I Hour (12-hour clock) as a decimal number [01,12].
            - %p Locale's equivalent of either AM or PM.

        Other codes may be available on your platform.
        See documentation for the C library strftime function.

        Args:
            format (str): The format string
            ptr (int): The pointer points to the target StructTime

        Returns:
            str: The formatted time string
        """
        if ptr == 0:
            return time.strftime(format)
        return time.strftime(format, self._manager.deref(ptr))

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 time 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["time.time"] = lambda: time.time()
        funcs["time.ctime"] = lambda seconds=None: time.ctime(seconds)
        funcs["time.asctime"] = self.asctime
        funcs["time.gmtime"] = lambda seconds=None: self._manager.ref(
            time.gmtime(seconds)
        )
        funcs["time.localtime"] = lambda seconds=None: self._manager.ref(
            time.localtime(seconds)
        )
        funcs["time.mktime"] = lambda ptr: time.mktime(self._manager.deref(ptr))
        funcs["time.strftime"] = self.strftime
        funcs["time.strptime"] = (
            lambda data_string, format="%a %b %d %H:%M:%S %Y": self._manager.ref(
                time.strptime(data_string, format)
            )
        )
        funcs["time.timezone"] = lambda: time.timezone
        funcs["time.tzname"] = lambda: self._manager.ref(time.tzname)

        for key, value in funcs.items():
            origin[key] = value
