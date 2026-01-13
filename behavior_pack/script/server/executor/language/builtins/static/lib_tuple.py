# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from .lib_object import BaseManager


class Tuple:
    """
    Tuple 提供了对元组的内置操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Tuple

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def new(self, *elements):  # type: (int) -> int
        """
        new 创建并返回一个新的元组

        Returns:
            int: 新创建的元组的指针
        """
        return self._manager.ref(tuple(elements))

    def cast(self, ptr):  # type: (int) -> int
        """
        cast 将 ptr 指向的对象强制转换为元组

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int: 强制转换后所得元组的指针
        """
        return self._manager.ref(tuple(self._manager.deref(ptr)))

    def length(self, ptr):  # type: (int) -> int
        """length 返回元组的长度

        Args:
            ptr (int): 目标元组的指针

        Raises:
            Exception:
                如果目标对象不是元组，则抛出相应的错误

        Returns:
            int: 目标元组的长度
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, tuple):
            raise Exception("tuple.length: Target object is not a tuple")
        return len(obj)

    def format(self, ptr):  # type: (int) -> str
        """format 将元组格式化为其字符串表示

        Args:
            ptr (int): 目标元组的指针

        Raises:
            Exception:
                如果目标对象不是元组，则抛出相应的错误

        Returns:
            str: 目标元组的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, tuple):
            raise Exception("tuple.format: Target object is not a tuple")
        return obj.__repr__()

    def get(self, ptr, index):  # type: (int, int) -> int
        """get 从元组中获取指定索引的元素

        Args:
            ptr (int): 目标元组的指针
            index (int): 要获取的元素的索引

        Raises:
            Exception:
                如果目标对象不是元组，则抛出相应的错误

        Returns:
            int: 所获元素的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, tuple):
            raise Exception("tuple.get: Target object is not a tuple")
        if index < 0 or index >= len(obj):
            raise Exception(
                "tuple.get: Index out of range [{}] with length {}".format(
                    index, len(obj)
                )
            )
        return self._manager.ref(obj[index])

    def sub(self, ptr, start, end):  # type: (int, int, int) -> int
        """sub 返回元组的子元组

        Args:
            ptr (int): 目标元组的指针
            start (int): 子元组的起始索引
            end (int): 子元组的结束索引

        Raises:
            Exception:
                如果目标对象不是元组，则抛出相应的错误

        Returns:
            int: 子元组的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, tuple):
            raise Exception("tuple.sub: Target object is not a tuple")
        return self._manager.ref(obj[start:end])

    def max(self, ptr):  # type: (int) -> int | bool | float | str
        """max 返回元组中最大的元素

        Args:
            ptr (int): 目标元组的指针

        Raises:
            Exception:
                如果目标对象不是元组，
                或最大值不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                元组中最大的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, tuple):
            raise Exception("tuple.max: Target object is not a tuple")

        result = max(obj)
        if not isinstance(result, (int, bool, float, str)):
            raise Exception(
                "tuple.max: Only support compare between int, bool, float or str"
            )

        return result

    def min(self, ptr):  # type: (int) -> int | bool | float | str
        """min 返回元组中最小的元素

        Args:
            ptr (int): 目标元组的指针

        Raises:
            Exception:
                如果目标对象不是元组，
                或最大值不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                元组中最小的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, tuple):
            raise Exception("tuple.min: Target object is not a tuple")

        result = min(obj)
        if not isinstance(result, (int, bool, float, str)):
            raise Exception(
                "tuple.min: Only support compare between int, bool, float or str"
            )

        return result

    def sum(self, ptr):  # type: (int) -> int | float
        """sum 返回元组中所有元素的和

        Args:
            ptr (int): 目标元组的指针

        Raises:
            Exception:
                如果目标对象不是元组，
                或求和结果不是整数或浮点数，
                则抛出相应的错误

        Returns:
            int | float:
                元组中所有元素的和
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, tuple):
            raise Exception("tuple.sum: Target object is not a tuple")

        result = sum(obj)
        if isinstance(result, bool) or not isinstance(result, (int, float)):
            raise Exception("tuple.sum: Only support tuple that contains int or float")

        return result

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 tuple 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["tuple.new"] = self.new
        funcs["tuple.cast"] = self.cast
        funcs["tuple.length"] = self.length
        funcs["tuple.format"] = self.format
        funcs["tuple.get"] = self.get
        funcs["tuple.sub"] = self.sub
        funcs["tuple.max"] = self.max
        funcs["tuple.min"] = self.min
        funcs["tuple.sum"] = self.sum

        for key, value in funcs.items():
            origin[key] = value
