# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

import random
import uuid
import time
import datetime

MIN_INT32 = -(2**31)
MAX_INT32 = 2**31 - 1

RAW_TYPE_INT = 0
RAW_TYPE_BOOL = 1
RAW_TYPE_FLOAT = 2
RAW_TYPE_STR = 3

REF_TYPE_INT = 0
REF_TYPE_BOOL = 1
REF_TYPE_FLOAT = 2
REF_TYPE_STR = 3
REF_TYPE_NONE = 4
REF_TYPE_SLICE = 5
REF_TYPE_MAP = 6
REF_TYPE_TUPLE = 7
REF_TYPE_SET = 8
REF_TYPE_UUID = 9
REF_TYPE_STRUCT_TIME = 10
REF_TYPE_DATETIME_TIMEDELTA = 11
REF_TYPE_DATETIME_TIME = 12
REF_TYPE_DATETIME_DATE = 13
REF_TYPE_DATETIME_DATETIME = 14
REF_TYPE_UNKNOWN = 0xFFFF


class BaseManager:
    """
    BaseManager 是一个基本管理器，
    它管理了所有依赖共用的随机数生成器和引用对象
    """

    _random = random.Random()  # type: random.Random
    _mapping = {}  # type: dict[int, Any]
    _pinned = set()  # type: set[int]

    def __init__(self):  # type: () -> None
        """初始化并返回一个新的基本管理器"""
        self._random = random.Random()
        self._mapping = {}
        self._pinned = set()

    def _make_ptr(self):  # type: () -> int
        """
        _make_ptr 试图生成一个新的指针。
        确保指针在有符号 32 位整形范围内，
        并且该指针不为 0 且也没有被使用

        Returns:
            int: 分配到的指针
        """
        while True:
            ptr = self._random.randint(MIN_INT32, MAX_INT32)
            if ptr != 0 and ptr not in self._mapping:
                return ptr

    def rand(self):  # type: () -> random.Random
        """
        rand 返回用于生成随机数的随机数生成器。

        Returns:
            random.Random:
                用于生成随机数的随机数生成器
        """
        return self._random

    def ref(self, obj):  # type: (Any) -> int
        """
        ref 注册 obj 到引用中，并返回此引用所得的指针。

        如果 obj 不是引用类型，则后续对 obj 的进一步
        修改将不会影响该指针所指向的对象

        Args:
            obj (Any): 欲注册的对象

        Returns:
            int: 被注册对象分配得到的指针
        """
        ptr = self._make_ptr()
        self._mapping[ptr] = obj
        return ptr

    def can_deref(self, ptr):  # type: (int) -> bool
        """
        can_deref 检查 ptr 指向的对象是否可以被玩家解引用。
        只有整数、布尔值、浮点数和字符串才可以被玩家解引用

        Args:
            ptr (int): 目标对象的指针

        Raises:
            Exception: 如果 ptr 无效，则抛出相应的错误

        Returns:
            bool: 目标对象是否可以被玩家解引用
        """
        if ptr not in self._mapping:
            raise Exception("can_deref: Invalid address or nil pointer dereference")

        obj = self._mapping[ptr]
        if isinstance(obj, (int, bool, float, str)):
            return True
        try:
            if isinstance(obj, unicode):  # type: ignore
                return True
        except Exception:
            pass

        return False

    def deref(self, ptr, internal=True):  # type: (int, bool) -> Any
        """deref 将 ptr 指向的对象解引用

        Args:
            ptr (int):
                目标对象的指针
            internal (bool, optional):
                deref 的调用者是否是内部实现。
                如果是内部实现，则允许解引用任何类型的对象。
                默认值为 True

        Raises:
            Exception:
                如果 ptr 无效，
                或目标对象不可被解引用，
                则抛出相应的错误

        Returns:
            Any:
                返回 ptr 所指向的对象。
                如果 internal 为假，则只可能返回整数、布尔值、浮点数或字符串；
                否则，可能返回任何类型的对象
        """
        if ptr not in self._mapping:
            raise Exception("deref: Invalid address or nil pointer dereference")

        obj = self._mapping[ptr]
        if internal or isinstance(obj, (int, bool, float, str)):
            return obj
        try:
            if isinstance(obj, unicode):  # type: ignore
                return obj
        except Exception:
            pass

        raise Exception("deref: Target object cannot be dereferenced")

    def current(self):  # type: () -> set[int]
        """
        current 返回当前所有对象的指针。它主要用于递归时保留调用者的上下文。
        有责任确保 current 的调用者总是来自于内部实现（如代码执行器）

        Returns:
            dict[int, Any]:
                当前所有对象的指针
        """
        return set(self._mapping)

    def release(self, ptr):  # type: (int) -> bool
        """
        release 释放 ptr 指向的对象的引用。

        Args:
            ptr (int):
                目标对象的指针

        Raises:
            Exception:
                如果 ptr 无效，
                或其指向的对象已被固定，
                则抛出相应的错误

        Returns:
            bool:
                总是返回 True
        """
        if ptr not in self._mapping:
            raise Exception("release: Invalid address or nil pointer dereference")
        if ptr in self._pinned:
            raise Exception("release: Target object is pinned and cannot be released")
        del self._mapping[ptr]
        return True

    def release_internal(self, last):  # type: (set[int]) -> None
        """
        release_internal 释放除 last 以外的，对所有未被固定的对象的引用。
        release_internal 主要用于在递归的上下文调用之间释放不再需要的对象。
        有责任确保 release_internal 的调用者总是来自于内部实现（如代码执行器）

        Args:
            last (set[int]):
                释放过程中要特别排除的指针
        """
        if len(last) == 0 and len(self._pinned) == 0:
            self._mapping.clear()
        else:
            self._mapping = {
                ptr: self._mapping[ptr]
                for ptr in last | self._pinned
                if ptr in self._mapping
            }

    def pin(self, ptr):  # type: (int) -> bool
        """
        pin 固定 ptr 所指向的对象，这意味着即便它在代码运行结束后也不会被释放。
        多次对相同的对象调用 pin 不会出现错误

        Args:
            ptr (int): 目标对象的指针

        Raises:
            Exception: 如果 ptr 无效，则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        if ptr not in self._mapping:
            raise Exception("pin: Invalid address or nil pointer dereference")
        self._pinned.add(ptr)
        return True

    def finalise(self, ptr):  # type: (int) -> bool
        """
        finalise 终结了 ptr 所指向对象的固定态。
        这意味着 ptr 所指向的对象将可以被释放。
        另，如果目标对象未被固定，也不会出现错误

        Args:
            ptr (int):
                目标对象的指针

        Raises:
            Exception:
                如果 ptr 无效，则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        if ptr not in self._mapping:
            raise Exception("finalise: Invalid address or nil pointer dereference")
        self._pinned.discard(ptr)
        return True

    def make_none(self):  # type: () -> int
        """
        make_none 创建一个 None 对象，
        并返回指向该对象的指针

        Returns:
            int: 新创建的对象的指针
        """
        return self.ref(None)

    def is_ptr(self, ptr):  # type: (int) -> bool
        """
        is_ptr 检查 ptr 是否为是一个指针

        Args:
            ptr (int): 欲被检查的整数

        Returns:
            bool:
                如果 ptr 是一个有效的指针，则返回 True；
                否则 ptr 尚且未指向任何对象，那么返回 False
        """
        return ptr in self._mapping

    def is_none(self, ptr):  # type: (int) -> bool
        """is_none 检查 ptr 指向的对象是否为 None

        Args:
            ptr (int): 欲被检查的整数

        Returns:
            bool:
                如果 ptr 不是有效的指针，或指向的对象不是 None，则返回 False；
                否则 ptr 指向了一个 None 对象，那么返回 True
        """
        return ptr in self._mapping and self._mapping[ptr] is None

    def raw_type(self, obj):  # type: (int | bool | float | str) -> int
        """raw_type 返回 obj 的类型

        Args:
            obj (int | bool | float | str):
                要获取类型的对象

        Returns:
            int:
                用于标识 obj 类型的整数。只可能为下列之一。
                    - RAW_TYPE_INT: 整数
                    - RAW_TYPE_BOOL: 布尔值
                    - RAW_TYPE_FLOAT: 浮点数
                    - RAW_TYPE_STR: 字符串
        """
        if isinstance(obj, bool):
            return RAW_TYPE_BOOL
        if isinstance(obj, int):
            return RAW_TYPE_INT
        if isinstance(obj, float):
            return RAW_TYPE_FLOAT
        if isinstance(obj, str):
            return RAW_TYPE_STR

    def ref_type(self, ptr):  # type: (int) -> int
        """ref_type 返回 ptr 指向对象的类型

        Args:
            obj (int): 目标对象的指针

        Raises:
            Exception:
                如果 ptr 无效，则抛出相应的错误

        Returns:
            int:
                用于标识目标对象的类型的整数。只可能为下列之一。
                    - REF_TYPE_INT: 整数
                    - REF_TYPE_BOOL: 布尔值
                    - REF_TYPE_FLOAT: 浮点数
                    - REF_TYPE_STR: 字符串
                    - REF_TYPE_NONE: None
                    - REF_TYPE_SLICE: 切片
                    - REF_TYPE_MAP: 映射
                    - REF_TYPE_TUPLE: 元组
                    - REF_TYPE_SET: 集合
                    - REF_TYPE_UUID: UUID
                    - REF_TYPE_STRUCT_TIME: 结构化时间
                    - REF_TYPE_DATETIME_TIMEDELTA: 时间差
                    - REF_TYPE_DATETIME_TIME: 时间
                    - REF_TYPE_DATETIME_DATE: 日期
                    - REF_TYPE_DATETIME_DATETIME: DateTime
                    - REF_TYPE_UNKNOWN: 其他类型
        """
        if ptr not in self._mapping:
            raise Exception("ref_type: Invalid address or nil pointer dereference")
        obj = self._mapping[ptr]
        if obj is None:
            return REF_TYPE_NONE

        if isinstance(obj, uuid.UUID):
            return REF_TYPE_UUID
        if isinstance(obj, time.struct_time):
            return REF_TYPE_STRUCT_TIME
        if isinstance(obj, datetime.timedelta):
            return REF_TYPE_DATETIME_TIMEDELTA
        if isinstance(obj, datetime.time):
            return REF_TYPE_DATETIME_TIME
        if isinstance(obj, datetime.date):
            return REF_TYPE_DATETIME_DATE
        if isinstance(obj, datetime.datetime):
            return REF_TYPE_DATETIME_DATETIME

        if isinstance(obj, bool):
            return REF_TYPE_BOOL
        if isinstance(obj, int):
            return REF_TYPE_INT
        if isinstance(obj, float):
            return REF_TYPE_FLOAT
        if isinstance(obj, str):
            return REF_TYPE_STR
        if isinstance(obj, list):
            return REF_TYPE_SLICE
        if isinstance(obj, dict):
            return REF_TYPE_MAP
        if isinstance(obj, tuple):
            return REF_TYPE_TUPLE
        if isinstance(obj, set):
            return REF_TYPE_SET

        try:
            if isinstance(obj, unicode):  # type: ignore
                return REF_TYPE_STR
        except Exception:
            pass

        return REF_TYPE_UNKNOWN

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 object 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["object.ref"] = self.ref
        funcs["object.can_deref"] = self.can_deref
        funcs["object.deref"] = lambda ptr: self.deref(ptr, False)
        funcs["object.release"] = self.release
        funcs["object.pin"] = self.pin
        funcs["object.finalise"] = self.finalise
        funcs["object.make_none"] = self.make_none
        funcs["object.is_ptr"] = self.is_ptr
        funcs["object.is_none"] = self.is_none
        funcs["object.raw_type"] = self.raw_type
        funcs["object.ref_type"] = self.ref_type

        for key, value in funcs.items():
            origin[key] = value
