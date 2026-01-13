# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

import bisect
from .lib_object import BaseManager


class Slices:
    """
    Slices 提供了对切片的内置操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Slices

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def make(self, length, value):  # type: (int, int | bool | float | str) -> int
        """
        make 创建一个长度为 length 且元素为 value 的切片

        Args:
            length (int):
                目标切片的长度
            value (int | bool | float | str):
                目标切片中的单个元素

        Returns:
            int:
                新创建的切片的指针
        """
        return self._manager.ref([value] * length)

    def cast(self, ptr):  # type: (int) -> int
        """
        cast 将 ptr 指向的对象强制转换为切片

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int: 强制转换后所得切片的指针
        """
        return self._manager.ref(list(self._manager.deref(ptr)))

    def length(self, ptr):  # type: (int) -> int
        """length 返回切片的长度

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，则抛出相应的错误

        Returns:
            int: 目标切片的长度
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.length: Target object is not a slice")
        return len(obj)

    def copy(self, ptr):  # type: (int) -> int
        """copy 返回切片的浅拷贝

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，则抛出相应的错误

        Returns:
            int: 浅拷贝所得切片的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.copy: Target object is not a slice")
        return self._manager.ref(obj.copy())

    def format(self, ptr):  # type: (int) -> str
        """format 将切片格式化为其字符串表示

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，则抛出相应的错误

        Returns:
            str: 目标切片的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.format: Target object is not a slice")
        return obj.__repr__()

    def append(self, ptr, raw):  # type: (int, int | bool | float | str) -> bool
        """
        append 向一个给定的切片追加指定的新元素

        Args:
            ptr (int):
                要被追加的切片的指针
            raw (int | bool | float | str):
                欲被追加的元素

        Raises:
            Exception:
                如果目标对象不是切片，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        slice_obj = self._manager.deref(ptr)
        if not isinstance(slice_obj, list):
            raise Exception("slices.append: Target object is not a slice")
        slice_obj.append(raw)
        return True

    def ptr_append(self, slice_ptr, value_ptr):  # type: (int, int) -> bool
        """
        ptr_append 向一个给定的切片追加指定的新元素。
        它与 append 的不同之处在于它完全基于指针进行操作

        Args:
            slice_ptr (int):
                要被追加的切片的指针
            value_ptr (int):
                欲被追加的元素的指针

        Raises:
            Exception:
                如果 slice_ptr 指向的对象不是切片，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        slice_obj = self._manager.deref(slice_ptr)
        if not isinstance(slice_obj, list):
            raise Exception("slices.ptr_append: Target object is not a slice")
        slice_obj.append(self._manager.deref(value_ptr))
        return True

    def get(self, ptr, index):  # type: (int, int) -> int | bool | float | str
        """
        get 从给定的切片中获取在指定索引的元素

        Args:
            ptr (int): 目标切片的指针
            index (int): 要获取的元素的索引

        Raises:
            Exception:
                如果目标对象不是切片，
                或目标元素不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                所获的目标元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.get: Target object is not a slice")

        if index < 0 or index >= len(obj):
            raise Exception(
                "slices.get: Index out of range [{}] with length {}".format(
                    index, len(obj)
                )
            )
        val = obj[index]
        if not isinstance(val, (int, bool, float, str)):
            raise Exception(
                "slices.get: Can only get a value that data type is int, bool, float or str"
            )

        return val

    def ptr_get(self, ptr, index):  # type: (int, int) -> int
        """
        ptr_get 从给定的切片中获取在指定索引的元素。
        它与 get 的不同之处在于它完全基于指针进行操作

        Args:
            ptr (int): 目标切片的指针
            index (int): 要获取的元素的索引

        Raises:
            Exception:
                如果目标对象不是切片，
                则抛出相应的错误

        Returns:
            int: 所获元素的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.ptr_get: Target object is not a slice")
        if index < 0 or index >= len(obj):
            raise Exception(
                "slices.ptr_get: Index out of range [{}] with length {}".format(
                    index, len(obj)
                )
            )
        return self._manager.ref(obj[index])

    def set(self, ptr, ind, raw):  # type: (int, int, int | bool | float | str) -> bool
        """set 设置给定的切片中，在指定索引处的元素

        Args:
            ptr (int):
                被修改的切片的指针
            ind (int):
                被修改的元素的索引
            raw (int | bool | float | str):
                该索引处应设置的新元素

        Raises:
            Exception:
                如果目标对象不是切片，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        slice_obj = self._manager.deref(ptr)
        if not isinstance(slice_obj, list):
            raise Exception("slices.set: Target object is not a slice")
        if ind < 0 or ind >= len(slice_obj):
            raise Exception(
                "slices.set: Index out of range [{}] with length {}".format(
                    ind, len(slice_obj)
                )
            )
        slice_obj[ind] = raw
        return True

    def ptr_set(self, slice_ptr, index, value_ptr):  # type: (int, int, int) -> bool
        """
        ptr_set 设置给定的切片中，在指定索引处的元素。
        它与 set 的不同之处在于它完全基于指针进行操作

        Args:
            slice_ptr (int):
                被修改的切片的指针
            index (int):
                被修改的元素的索引
            value_ptr (int):
                该索引处应设置的新元素（的指针）

        Raises:
            Exception:
                如果 slice_ptr 指向的对象不是切片，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        slice_obj = self._manager.deref(slice_ptr)
        if not isinstance(slice_obj, list):
            raise Exception("slices.ptr_set: Target object is not a slice")
        if index < 0 or index >= len(slice_obj):
            raise Exception(
                "slices.ptr_set: Index out of range [{}] with length {}".format(
                    index, len(slice_obj)
                )
            )
        slice_obj[index] = self._manager.deref(value_ptr)
        return True

    def max(self, ptr):  # type: (int) -> int | bool | float | str
        """max 返回切片中最大的元素

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，
                或最大值不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                切片中最大的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.max: Target object is not a slice")

        result = max(obj)
        if not isinstance(result, (int, bool, float, str)):
            raise Exception(
                "slices.max: Only support compare between int, bool, float or str"
            )

        return result

    def min(self, ptr):  # type: (int) -> int | bool | float | str
        """min 返回切片中最小的元素

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，
                或最大值不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                切片中最小的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.min: Target object is not a slice")

        result = min(obj)
        if not isinstance(result, (int, bool, float, str)):
            raise Exception(
                "slices.min: Only support compare between int, bool, float or str"
            )

        return result

    def sum(self, ptr):  # type: (int) -> int | float
        """sum 返回切片中所有元素的和

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，
                或求和结果不是整数或浮点数，
                则抛出相应的错误

        Returns:
            int | float:
                切片中所有元素的和
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.sum: Target object is not a slice")

        result = sum(obj)
        if isinstance(result, bool) or not isinstance(result, (int, float)):
            raise Exception("slices.sum: Only support slice that contains int or float")

        return result

    def sub(self, ptr, start, end):  # type: (int, int, int) -> int
        """sub 返回切片的子切片

        Args:
            ptr (int): 目标切片的指针
            start (int): 子切片的起始索引
            end (int): 子切片的结束索引

        Raises:
            Exception:
                如果目标对象不是切片，
                或给出的起始或结束索引超出切片的范围，
                或结束索引小于起始索引，
                则抛出相应的错误

        Returns:
            int: 子切片的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.sub: Target object is not a slice")

        if start < 0 or start > len(obj):
            raise Exception(
                "slices.sub: Start index out of range [{}] with length {}".format(
                    start, len(obj)
                )
            )
        if end < 0 or end > len(obj):
            raise Exception(
                "slices.sub: End index out of range [{}] with length {}".format(
                    end, len(obj)
                )
            )
        if end < start:
            raise Exception(
                "slices.sub: The end index can't be less than the start index (start={}, end={})".format(
                    start, end
                )
            )

        return self._manager.ref(obj[start:end])

    def insert(
        self, ptr, ind, raw
    ):  # type: (int, int, int | bool | float | str) -> bool
        """
        insert 向给定的切片在指定的位置处插入一个新的元素

        Args:
            ptr (int):
                目标切片的指针
            ind (int):
                要插入的位置（索引）
            raw (int | bool | float | str):
                要插入的元素

        Raises:
            Exception:
                如果目标对象不是切片，
                或给出的索引超出范围，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        slice_obj = self._manager.deref(ptr)
        if not isinstance(slice_obj, list):
            raise Exception("slices.insert: Target object is not a slice")
        if ind < 0 or ind > len(slice_obj):
            raise Exception(
                "slices.insert: Index out of range [{}] with length {}".format(
                    ind, len(slice_obj)
                )
            )
        slice_obj.insert(ind, raw)
        return True

    def ptr_insert(self, slice_ptr, index, value_ptr):  # type: (int, int, int) -> bool
        """
        ptr_insert 向给定的切片在指定的位置处插入一个新的元素。
        它与 insert 的不同之处在于它完全基于指针进行操作

        Args:
            slice_ptr (int): 目标切片的指针
            index (int): 要插入的位置（索引）
            value_ptr (int): 要插入的元素的指针

        Raises:
            Exception:
                如果 slice_ptr 指向的对象不是切片，
                或给出的索引超出范围，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        slice_obj = self._manager.deref(slice_ptr)
        if not isinstance(slice_obj, list):
            raise Exception("slices.ptr_insert: Target object is not a slice")
        if index < 0 or index > len(slice_obj):
            raise Exception(
                "slices.ptr_insert: Index out of range [{}] with length {}".format(
                    index, len(slice_obj)
                )
            )
        slice_obj.insert(index, self._manager.deref(value_ptr))
        return True

    def pop(self, ptr):  # type: (int) -> int | bool | float | str
        """pop 从给定的切片中弹出其最后一个元素

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，
                或被弹出的元素不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                被弹出的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.pop: Target object is not a slice")
        val = obj.pop()
        if not isinstance(val, (int, bool, float, str)):
            raise Exception(
                "slices.pop: Can only pop a value that data type is int, bool, float or str"
            )
        return val

    def ptr_pop(self, ptr):  # type: (int) -> int
        """
        ptr_pop 从给定的切片中弹出其最后一个元素。
        它与 pop 的不同之处在于它完全基于指针进行操作

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，
                则抛出相应的错误

        Returns:
            int: 被弹出的元素的指针
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.ptr_pop: Target object is not a slice")
        return self._manager.ref(obj.pop())

    def reverse(self, ptr):  # type: (int) -> bool
        """
        reverse 将切片按切片中元素的原有顺序反转。
        最终将得到一个元素排列顺序与原切片相反的切片

        Args:
            ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果目标对象不是切片，则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.reverse: Target object is not a slice")
        obj.reverse()
        return True

    def sort(self, ptr, reverse=False):  # type: (int, bool) -> bool
        """sort 对切片中的元素进行排序

        Args:
            ptr (int):
                目标切片的指针
            reverse (bool, optional):
                是否反向排序。
                默认值为 False

        Raises:
            Exception:
                如果目标对象不是切片，则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.sort: Target object is not a slice")
        obj.sort(reverse=reverse)
        return True

    def concat(self, *ptrs):  # type: (...) -> int
        """
        concat 将多个切片连接成一个新的切片

        Raises:
            Exception:
                如果有任意一个指针指向的对象不是切片，
                则抛出相应的错误

        Returns:
            int: 新切片的指针
        """
        result = []
        for index, value in enumerate(ptrs):
            obj = self._manager.deref(value)
            if not isinstance(obj, list):
                raise Exception(
                    "slices.concat: Argument in index {} is not a slice (ptr={})".format(
                        index, value
                    )
                )
            result.extend(obj)
        return self._manager.ref(result)

    def binsearch(self, ptr, raw):  # type: (int, int | bool | float | str) -> int
        """
        binsearch 在有序切片中二分查找指定元素。请务必确保传递的切片已经按升序排序。
        如果传递的切片未被按正确的顺序进行排序，则最终返回的结果将是不确定的

        Args:
            ptr (int):
                目标切片的指针
            raw (int | bool | float | str):
                欲查找的元素

        Raises:
            Exception:
                如果目标对象不是切片，
                则抛出相应的错误

        Returns:
            int:
                返回一个只有两个元素的元组的指针。
                如果目标元素被找到，则元组的第二个元素为 True，并且第一个元素指示该元素在切片中的索引；
                否则，元组的第二个元素为 False，并且第一个元素指示该元素应被插入的位置的索引
        """
        slice_obj = self._manager.deref(ptr)
        if not isinstance(slice_obj, list):
            raise Exception("slices.binsearch: Target object is not a slice")

        index = bisect.bisect_left(slice_obj, raw)
        if index != len(slice_obj) and slice_obj[index] == raw:
            return self._manager.ref((index, True))

        return self._manager.ref((index, False))

    def ptr_binsearch(self, slice_ptr, value_ptr):  # type: (int, int) -> int
        """
        ptr_binsearch 在有序切片中二分查找指定元素。
        它的调用者有义务确保传递的切片已经按升序排序。

        如果传递的切片未被按正确的顺序进行排序，
        则最终返回的结果将是不确定的。

        ptr_binsearch 与 binsearch 的不同之处在于
        ptr_binsearch 完全基于指针进行操作

        Args:
            slice_ptr (int): 目标切片的指针
            value_ptr (int): 要查找的元素的指针

        Raises:
            Exception:
                如果 slice_ptr 指向的对象不是切片，
                则抛出相应的错误

        Returns:
            int:
                返回一个只有两个元素的元组的指针。
                如果目标元素被找到，则元组的第二个元素为 True，并且第一个元素指示该元素在切片中的索引；
                否则，元组的第二个元素为 False，并且第一个元素指示该元素应被插入的位置的索引
        """
        slice_obj = self._manager.deref(slice_ptr)
        if not isinstance(slice_obj, list):
            raise Exception("slices.ptr_binsearch: Target object is not a slice")

        value_obj = self._manager.deref(value_ptr)
        index = bisect.bisect_left(slice_obj, value_obj)

        if index != len(slice_obj) and slice_obj[index] == value_obj:
            return self._manager.ref((index, True))
        return self._manager.ref((index, False))

    def compare_in(self, ptr, raw):  # type: (int, int | bool | float | str) -> bool
        """compare_in 检查给定的切片是否包含指定的元素

        Args:
            ptr (int):
                目标切片的指针
            raw (int | bool | float | str):
                欲被检查的元素

        Raises:
            Exception:
                如果目标对象不是切片，
                则抛出相应的错误

        Returns:
            bool: 目标切片是否包含给定的元素
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, list):
            raise Exception("slices.in: Target object is not a slice")
        return raw in obj

    def ptr_compare_in(self, slice_ptr, value_ptr):  # type: (int, int) -> bool
        """
        ptr_compare_in 检查给定的切片是否包含指定的元素。
        它与 compare_in 的不同之处在于它完全基于指针进行操作

        Args:
            slice_ptr (int):
                目标切片的指针
            value_ptr (int):
                欲被检查的元素（的指针）

        Raises:
            Exception:
                如果目标对象不是切片，
                则抛出相应的错误

        Returns:
            bool: 目标切片是否包含给定的元素
        """
        obj = self._manager.deref(slice_ptr)
        if not isinstance(obj, list):
            raise Exception("slices.ptr_in: Target object is not a slice")
        return self._manager.deref(value_ptr) in obj

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 slices 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["slices.make"] = self.make
        funcs["slices.cast"] = self.cast
        funcs["slices.length"] = self.length
        funcs["slices.copy"] = self.copy
        funcs["slices.format"] = self.format
        funcs["slices.append"] = self.append
        funcs["slices.ptr_append"] = self.ptr_append
        funcs["slices.get"] = self.get
        funcs["slices.ptr_get"] = self.ptr_get
        funcs["slices.set"] = self.set
        funcs["slices.ptr_set"] = self.ptr_set
        funcs["slices.max"] = self.max
        funcs["slices.min"] = self.min
        funcs["slices.sum"] = self.sum
        funcs["slices.sub"] = self.sub
        funcs["slices.insert"] = self.insert
        funcs["slices.ptr_insert"] = self.ptr_insert
        funcs["slices.pop"] = self.pop
        funcs["slices.ptr_pop"] = self.ptr_pop
        funcs["slices.reverse"] = self.reverse
        funcs["slices.sort"] = self.sort
        funcs["slices.concat"] = self.concat
        funcs["slices.binsearch"] = self.binsearch
        funcs["slices.ptr_binsearch"] = self.ptr_binsearch
        funcs["slices.in"] = self.compare_in
        funcs["slices.ptr_in"] = self.ptr_compare_in

        for key, value in funcs.items():
            origin[key] = value
