# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from collections import OrderedDict
from .lib_object import BaseManager


class Maps:
    """
    Maps 提供了对映射的内置操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Maps

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def make(self, ordered=False):  # type: (bool) -> int
        """make 初始化并返回一个新的映射

        Args:
            ordered (bool, optional):
                要创建的映射是否是有序的。
                默认值为 False

        Returns:
            int: 新创建的映射的指针
        """
        if ordered:
            return self._manager.ref(OrderedDict())
        return self._manager.ref({})

    def cast(self, ptr):  # type: (int) -> int
        """
        cast 将 ptr 指向的对象强制转换为映射

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int: 强制转换后所得映射的指针
        """
        return self._manager.ref(dict(self._manager.deref(ptr)))

    def length(self, ptr):  # type: (int) -> int
        """length 返回映射的长度

        Args:
            ptr (int): 目标映射的指针

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            int: 目标映射的长度
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.length: Target object is not a map")
        return len(obj)

    def copy(self, ptr):  # type: (int) -> int
        """copy 返回映射的浅拷贝

        Args:
            ptr (int): 目标映射的指针

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            int: 浅拷贝所得映射的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.copy: Target object is not a map")
        return self._manager.ref(obj.copy())

    def format(self, ptr):  # type: (int) -> str
        """format 将映射格式化为其字符串表示

        Args:
            ptr (int): 目标映射的指针

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            str: 目标映射的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.format: Target object is not a map")
        return obj.__repr__()

    def exist(self, map_ptr, key_ptr):  # type: (int, int) -> bool
        """exist 检查映射中是否存在指定的键

        Args:
            map_ptr (int): 目标映射的指针
            key_ptr (int): 欲被检查的键（的指针）

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            bool: 目标映射中是否存在给定的键
        """
        obj = self._manager.deref(map_ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.exist: Target object is not a map")
        return self._manager.deref(key_ptr) in obj

    def get(self, map_ptr, key_ptr):  # type: (int, int) -> int
        """get 从映射中获取指定键对应的值

        Args:
            map_ptr (int): 目标映射的指针
            key_ptr (int): 欲获取值的键（的指针）

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            int: 给定键对应的值（的指针）
        """
        obj = self._manager.deref(map_ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.get: Target object is not a map")
        return self._manager.ref(obj[self._manager.deref(key_ptr)])

    def pop(self, map_ptr, key_ptr):  # type: (int, int) -> int
        """
        pop 获取并移除映射中指定键对应的值

        Args:
            map_ptr (int): 目标映射的指针
            key_ptr (int): 涉及的键的指针

        Raises:
            Exception:
                如果目标对象不是映射，
                或给定的键不存在，
                则抛出相应的错误

        Returns:
            int: 被移除的值的指针
        """
        obj = self._manager.deref(map_ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.pop: Target object is not a map")
        return self._manager.ref(obj.pop(self._manager.deref(key_ptr)))

    def set(self, map_ptr, key_ptr, value_ptr):  # type: (int, int, int) -> bool
        """set 在映射中设置指定键对应的值

        Args:
            map_ptr (int): 目标映射的指针
            key_ptr (int): 给定的键的指针
            value_ptr (int): 欲设置的值的指针

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(map_ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.set: Target object is not a map")
        obj[self._manager.deref(key_ptr)] = self._manager.deref(value_ptr)
        return True

    def delete(self, map_ptr, key_ptr):  # type: (int, int) -> bool
        """
        delete 从映射中移除给定的键以及该键的值

        Args:
            map_ptr (int): 目标映射的指针
            key_ptr (int): 给定的键的指针

        Raises:
            Exception:
                如果目标对象不是映射，
                或给定的键不存在，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(map_ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.delete: Target object is not a map")
        del obj[self._manager.deref(key_ptr)]
        return True

    def clear(self, ptr):  # type: (int) -> bool
        """clear 清空映射中的所有键值对

        Args:
            ptr (int): 目标映射的指针

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.clear: Target object is not a map")
        obj.clear()
        return True

    def keys(self, ptr):  # type: (int) -> int
        """keys 返回映射中所有键构成的切片

        Args:
            ptr (int): 目标映射的指针

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            int: 返回的切片的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.keys: Target object is not a map")
        return self._manager.ref(list(obj.keys()))

    def values(self, ptr):  # type: (int) -> int
        """values 返回映射中所有值构成的切片

        Args:
            ptr (int): 目标映射的指针

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            int: 返回的切片的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.values: Target object is not a map")
        return self._manager.ref(list(obj.values()))

    def items(self, ptr):  # type: (int) -> int
        """
        items 返回映射中的所有键值对构成的切片。
        切片中的每个元素都是一个二元组，表示一个键值对

        Args:
            ptr (int): 目标映射的指针

        Raises:
            Exception:
                如果目标对象不是映射，则抛出相应的错误

        Returns:
            int: 返回的切片的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, dict):
            raise Exception("maps.items: Target object is not a map")
        return self._manager.ref(list(obj.items()))

    def equal(self, ptr_a, ptr_b):  # type: (int, int) -> bool
        """
        equal 检查两个映射是否相等。
        如果两个映射都是有序映射，则还会检查它们的顺序是否相同

        Args:
            ptr_a (int): 第一个映射的指针
            ptr_b (int): 第二个映射的指针

        Raises:
            Exception:
                如果给出的对象有至少一个指向的不是映射，
                则抛出相应的错误

        Returns:
            bool: 给定的两个映射是否相等
        """
        obj_a = self._manager.deref(ptr_a)
        obj_b = self._manager.deref(ptr_b)
        if not isinstance(obj_a, dict) or not isinstance(obj_b, dict):
            raise Exception("maps.equal: At least one of the given object is not a map")
        return obj_a == obj_b

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 maps 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["maps.make"] = self.make
        funcs["maps.cast"] = self.cast
        funcs["maps.length"] = self.length
        funcs["maps.copy"] = self.copy
        funcs["maps.format"] = self.format
        funcs["maps.exist"] = self.exist
        funcs["maps.get"] = self.get
        funcs["maps.pop"] = self.pop
        funcs["maps.set"] = self.set
        funcs["maps.delete"] = self.delete
        funcs["maps.clear"] = self.clear
        funcs["maps.keys"] = self.keys
        funcs["maps.values"] = self.values
        funcs["maps.items"] = self.items
        funcs["maps.equal"] = self.equal

        for key, value in funcs.items():
            origin[key] = value
