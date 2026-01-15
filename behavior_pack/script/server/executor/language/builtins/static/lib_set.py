# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from .lib_object import BaseManager


class Set:
    """
    Set 提供了对集合的内置操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Set

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def new(self):  # type: () -> int
        """
        new 创建并返回一个新的集合

        Returns:
            int: 新创建的集合的指针
        """
        return self._manager.ref(set())

    def cast(self, ptr):  # type: (int) -> int
        """
        cast 将 ptr 指向的对象强制转换为集合

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int: 强制转换后所得集合的指针
        """
        return self._manager.ref(set(self._manager.deref(ptr)))

    def length(self, ptr):  # type: (int) -> int
        """length 返回集合的长度

        Args:
            ptr (int): 目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，则抛出相应的错误

        Returns:
            int: 目标集合的长度
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.length: Target object is not a set")
        return len(obj)

    def copy(self, ptr):  # type: (int) -> int
        """copy 返回集合的浅拷贝

        Args:
            ptr (int): 目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，则抛出相应的错误

        Returns:
            int: 浅拷贝所得集合的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.copy: Target object is not a set")
        return self._manager.ref(obj.copy())

    def format(self, ptr):  # type: (int) -> str
        """format 将集合格式化为其字符串表示

        Args:
            ptr (int): 目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，则抛出相应的错误

        Returns:
            str: 目标集合的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.format: Target object is not a set")
        return obj.__repr__()

    def exist(self, ptr, raw):  # type: (int, int | bool | float | str) -> bool
        """
        exist 检查给定的元素是否存在于指定的集合中

        Args:
            ptr (int):
                目标集合的指针
            raw (int | bool | float | str):
                欲被检查的元素

        Raises:
            Exception:
                如果目标对象不是集合，
                则抛出相应的错误

        Returns:
            bool: 给定的元素是否存在于集合中
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.exist: Target object is not a set")
        return raw in obj

    def ptr_exist(self, set_ptr, element_ptr):  # type: (int, int) -> bool
        """
        ptr_exist 检查给定的元素是否存在于指定的集合中。
        它与 exist 的不同之处在于它完全基于指针进行操作

        Args:
            set_ptr (int): 目标集合的指针
            element_ptr (int): 目标元素的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                则抛出相应的错误

        Returns:
            bool: 给定的元素是否存在于集合中
        """
        obj = self._manager.deref(set_ptr)
        if not isinstance(obj, set):
            raise Exception("set.ptr_exist: Target object is not a set")
        return self._manager.deref(element_ptr) in obj

    def add(self, ptr, raw):  # type: (int, int | bool | float | str) -> bool
        """add 向给定的集合中添加一个指定的元素

        Args:
            ptr (int):
                目标集合的指针
            raw (int | bool | float | str):
                欲被添加的元素

        Raises:
            Exception:
                如果目标对象不是集合，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.add: Target object is not a set")
        obj.add(raw)
        return True

    def ptr_add(self, set_ptr, element_ptr):  # type: (int, int) -> bool
        """
        ptr_add 向给定的集合中添加一个指定的元素。
        它与 add 的不同之处在于它完全基于指针进行操作

        Args:
            set_ptr (int): 目标集合的指针
            element_ptr (int): 目标元素的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(set_ptr)
        if not isinstance(obj, set):
            raise Exception("set.ptr_add: Target object is not a set")
        obj.add(self._manager.deref(element_ptr))
        return True

    def remove(self, ptr, raw):  # type: (int, int | bool | float | str) -> bool
        """
        remove 从给定的集合中移除一个指定的元素

        Args:
            ptr (int):
                目标集合的指针
            raw (int | bool | float | str):
                欲被移除的元素

        Raises:
            Exception:
                如果目标对象不是集合，
                或元素不存在于集合中，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.remove: Target object is not a set")
        obj.remove(raw)
        return True

    def ptr_remove(self, set_ptr, element_ptr):  # type: (int, int) -> bool
        """
        ptr_remove 从给定的集合中移除一个指定的元素。
        它与 remove 的不同之处在于它完全基于指针进行操作

        Args:
            set_ptr (int): 目标集合的指针
            element_ptr (int): 目标元素的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                或元素不存在于集合中，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(set_ptr)
        if not isinstance(obj, set):
            raise Exception("set.ptr_remove: Target object is not a set")
        obj.remove(self._manager.deref(element_ptr))
        return True

    def discard(self, ptr, raw):  # type: (int, int | bool | float | str) -> bool
        """
        discard 从给定的集合中移除一个指定的元素。
        这意味着即便目标元素不存在，也不会抛出错误

        Args:
            ptr (int):
                目标集合的指针
            raw (int | bool | float | str):
                欲被移除的元素

        Raises:
            Exception:
                如果目标对象不是集合，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.discard: Target object is not a set")
        obj.discard(raw)
        return True

    def ptr_discard(self, set_ptr, element_ptr):  # type: (int, int) -> bool
        """
        ptr_discard 从给定的集合中移除一个指定的元素。
        它与 discard 的不同之处在于它完全基于指针进行操作。
        这意味着即便目标元素不存在，也不会抛出错误

        Args:
            set_ptr (int): 目标集合的指针
            element_ptr (int): 目标元素的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(set_ptr)
        if not isinstance(obj, set):
            raise Exception("set.ptr_discard: Target object is not a set")
        obj.discard(self._manager.deref(element_ptr))
        return True

    def pop(self, ptr):  # type: (int) -> int | bool | float | str
        """
        pop 从集合中移除一个任意的元素，
        并返回所移除的这个元素

        Args:
            ptr (int):
                目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                或目标集合没有任何元素，
                或被移除的元素不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                被移除的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.pop: Target object is not a set")

        val = obj.pop()
        if isinstance(val, (int, bool, float, str)):
            return val
        try:
            if isinstance(val, unicode):  # type: ignore
                return val
        except Exception:
            pass

        raise Exception(
            "set.pop: Can only pop data that data type is int, bool, float or str"
        )

    def ptr_pop(self, ptr):  # type: (int) -> int
        """
        ptr_pop 从集合中移除一个任意的元素，并返回所移除的这个元素。
        它与 pop 的不同之处在于它完全基于指针进行操作

        Args:
            ptr (int): 目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                或目标集合没有任何元素，
                则抛出相应的错误

        Returns:
            int: 被移除元素的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.ptr_pop: Target object is not a set")
        return self._manager.ref(obj.pop())

    def clear(self, ptr):  # type: (int) -> bool
        """clear 清空集合中的所有元素

        Args:
            ptr (int): 目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.clear: Target object is not a set")
        obj.clear()
        return True

    def max(self, ptr):  # type: (int) -> int | bool | float | str
        """max 返回集合中最大的元素

        Args:
            ptr (int): 目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                或最大值不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                集合中最大的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.max: Target object is not a set")

        result = max(obj)
        if isinstance(result, (int, bool, float, str)):
            return result
        try:
            if isinstance(result, unicode):  # type: ignore
                return result
        except Exception:
            pass

        raise Exception("set.max: Only support compare between int, bool, float or str")

    def min(self, ptr):  # type: (int) -> int | bool | float | str
        """min 返回集合中最小的元素

        Args:
            ptr (int): 目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                或最大值不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                集合中最小的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.min: Target object is not a set")

        result = min(obj)
        if isinstance(result, (int, bool, float, str)):
            return result
        try:
            if isinstance(result, unicode):  # type: ignore
                return result
        except Exception:
            pass

        raise Exception("set.min: Only support compare between int, bool, float or str")

    def sum(self, ptr):  # type: (int) -> int | float
        """sum 返回集合中所有元素的和

        Args:
            ptr (int): 目标集合的指针

        Raises:
            Exception:
                如果目标对象不是集合，
                或求和结果不是整数或浮点数，
                则抛出相应的错误

        Returns:
            int | float:
                集合中所有元素的和
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, set):
            raise Exception("set.sum: Target object is not a set")

        result = sum(obj)
        if isinstance(result, bool) or not isinstance(result, (int, float)):
            raise Exception("set.sum: Only support set that contains int or float")

        return result

    def difference(self, set_ptr_a, set_ptr_b):  # type: (int, int) -> int
        """difference 返回集合 A 对集合 B 的差集

        Args:
            set_ptr_a (int): 集合 A 的指针
            set_ptr_b (int): 集合 B 的指针

        Raises:
            Exception:
                如果给出的对象有至少一个指向的不是集合，
                则抛出相应的错误

        Returns:
            int: 差集运算所得集合的指针
        """
        obj_a = self._manager.deref(set_ptr_a)
        obj_b = self._manager.deref(set_ptr_b)
        if not isinstance(obj_a, set) or not isinstance(obj_b, set):
            raise Exception(
                "set.difference: At least one of the given object is not a set"
            )
        return self._manager.ref(obj_a.difference(obj_b))

    def symmetric_difference(self, set_ptr_a, set_ptr_b):  # type: (int, int) -> int
        """
        symmetric_difference 返回集合 A 与集合 B 的对称差集

        Args:
            set_ptr_a (int): 集合 A 的指针
            set_ptr_b (int): 集合 B 的指针

        Raises:
            Exception:
                如果给出的对象有至少一个指向的不是集合，
                则抛出相应的错误

        Returns:
            int: 对称差集运算所得集合的指针
        """
        obj_a = self._manager.deref(set_ptr_a)
        obj_b = self._manager.deref(set_ptr_b)
        if not isinstance(obj_a, set) or not isinstance(obj_b, set):
            raise Exception(
                "set.symmetric_difference: At least one of the given object is not a set"
            )
        return self._manager.ref(obj_a.symmetric_difference(obj_b))

    def intersection(self, set_ptr_a, set_ptr_b):  # type: (int, int) -> int
        """
        intersection 返回集合 A 与集合 B 的交集

        Args:
            set_ptr_a (int): 集合 A 的指针
            set_ptr_b (int): 集合 B 的指针

        Raises:
            Exception:
                如果给出的对象有至少一个指向的不是集合，
                则抛出相应的错误

        Returns:
            int: 交集运算所得集合的指针
        """
        obj_a = self._manager.deref(set_ptr_a)
        obj_b = self._manager.deref(set_ptr_b)
        if not isinstance(obj_a, set) or not isinstance(obj_b, set):
            raise Exception(
                "set.intersection: At least one of the given object is not a set"
            )
        return self._manager.ref(obj_a.intersection(obj_b))

    def union(self, set_ptr_a, set_ptr_b):  # type: (int, int) -> int
        """union 返回集合 A 与集合 B 的并集

        Args:
            set_ptr_a (int): 集合 A 的指针
            set_ptr_b (int): 集合 B 的指针

        Raises:
            Exception:
                如果给出的对象有至少一个指向的不是集合，
                则抛出相应的错误

        Returns:
            int: 并集运算所得集合的指针
        """
        obj_a = self._manager.deref(set_ptr_a)
        obj_b = self._manager.deref(set_ptr_b)
        if not isinstance(obj_a, set) or not isinstance(obj_b, set):
            raise Exception("set.union: At least one of the given object is not a set")
        return self._manager.ref(obj_a.union(obj_b))

    def isdisjoint(self, set_ptr_a, set_ptr_b):  # type: (int, int) -> bool
        """isdisjoint 检查集合 A 与集合 B 是否不相交

        Args:
            set_ptr_a (int): 集合 A 的指针
            set_ptr_b (int): 集合 B 的指针

        Raises:
            Exception:
                如果给出的对象有至少一个指向的不是集合，
                则抛出相应的错误

        Returns:
            bool: 集合 A 与集合 B 是否不相交
        """
        obj_a = self._manager.deref(set_ptr_a)
        obj_b = self._manager.deref(set_ptr_b)
        if not isinstance(obj_a, set) or not isinstance(obj_b, set):
            raise Exception(
                "set.isdisjoint: At least one of the given object is not a set"
            )
        return obj_a.isdisjoint(obj_b)

    def issubset(self, set_ptr_a, set_ptr_b):  # type: (int, int) -> bool
        """issubset 检查集合 A 是否是集合 B 的子集

        Args:
            set_ptr_a (int): 集合 A 的指针
            set_ptr_b (int): 集合 B 的指针

        Raises:
            Exception:
                如果给出的对象有至少一个指向的不是集合，
                则抛出相应的错误

        Returns:
            bool: 集合 A 是否是集合 B 的子集
        """
        obj_a = self._manager.deref(set_ptr_a)
        obj_b = self._manager.deref(set_ptr_b)
        if not isinstance(obj_a, set) or not isinstance(obj_b, set):
            raise Exception(
                "set.issubset: At least one of the given object is not a set"
            )
        return obj_a.issubset(obj_b)

    def issuperset(self, set_ptr_a, set_ptr_b):  # type: (int, int) -> bool
        """issuperset 检查集合 A 是否是集合 B 的超集

        Args:
            set_ptr_a (int): 集合 A 的指针
            set_ptr_b (int): 集合 B 的指针

        Raises:
            Exception:
                如果给出的对象有至少一个指向的不是集合，
                则抛出相应的错误

        Returns:
            bool: 集合 A 是否是集合 B 的超集
        """
        obj_a = self._manager.deref(set_ptr_a)
        obj_b = self._manager.deref(set_ptr_b)
        if not isinstance(obj_a, set) or not isinstance(obj_b, set):
            raise Exception(
                "set.issuperset: At least one of the given object is not a set"
            )
        return obj_a.issuperset(obj_b)

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 set 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["set.new"] = self.new
        funcs["set.cast"] = self.cast
        funcs["set.length"] = self.length
        funcs["set.copy"] = self.copy
        funcs["set.format"] = self.format
        funcs["set.exist"] = self.exist
        funcs["set.ptr_exist"] = self.ptr_exist
        funcs["set.add"] = self.add
        funcs["set.ptr_add"] = self.ptr_add
        funcs["set.remove"] = self.remove
        funcs["set.ptr_remove"] = self.ptr_remove
        funcs["set.discard"] = self.discard
        funcs["set.ptr_discard"] = self.ptr_discard
        funcs["set.pop"] = self.pop
        funcs["set.ptr_pop"] = self.ptr_pop
        funcs["set.clear"] = self.clear
        funcs["set.max"] = self.max
        funcs["set.min"] = self.min
        funcs["set.sum"] = self.sum
        funcs["set.difference"] = self.difference
        funcs["set.symmetric_difference"] = self.symmetric_difference
        funcs["set.intersection"] = self.intersection
        funcs["set.union"] = self.union
        funcs["set.isdisjoint"] = self.isdisjoint
        funcs["set.issubset"] = self.issubset
        funcs["set.issuperset"] = self.issuperset

        for key, value in funcs.items():
            origin[key] = value
