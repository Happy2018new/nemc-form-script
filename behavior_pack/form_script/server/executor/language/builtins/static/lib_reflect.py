# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

import copy
from .lib_object import BaseManager


class Reflect:
    """
    Reflect 提供了对反射的内置操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Reflect

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def cast(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """
        cast 将对象 A 强制转换为对象 B 的类型

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回强制转换所得对象的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                type(self._manager.deref(ptr_b))(self._manager.deref(ptr_a))
            )
        except Exception:
            return 0

    def length(self, ptr):  # type: (int) -> int
        """length 返回给定对象的长度

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向长度的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(len(self._manager.deref(ptr)))
        except Exception:
            return 0

    def copy(self, ptr):  # type: (int) -> int
        """copy 返回对象的浅拷贝

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回目标对象在浅拷贝后所得对象的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(copy.copy(self._manager.deref(ptr)))
        except Exception:
            return 0

    def deepcopy(self, ptr):  # type: (int) -> int
        """deepcopy 返回对象的深拷贝

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回目标对象在深拷贝后所得对象的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(copy.deepcopy(self._manager.deref(ptr)))
        except Exception:
            return 0

    def format(self, ptr):  # type: (int) -> int
        """format 返回对象的格式化表示

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向格式化表示的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(self._manager.deref(ptr).__repr__())
        except Exception:
            return 0

    def vars(self, ptr):  # type: (int) -> int
        """vars 是已被弃用的特性

        Args:
            ptr (int): 任意整数

        Returns:
            int: 总是返回 0
        """
        _ = ptr
        return 0

    def dir(self, ptr):  # type: (int) -> int
        """dir 是已被弃用的特性

        Args:
            ptr (int): 任意整数

        Returns:
            int: 总是返回 0
        """
        _ = ptr
        return 0

    def hasattr(self, ptr, attr):  # type: (int, str) -> bool
        """hasattr 是已被弃用的特性

        Args:
            ptr (int): 任意整数
            attr (str): 任意字符串

        Returns:
            bool: 总是返回 False
        """
        _, _ = ptr, attr
        return False

    def getattr(self, ptr, attr):  # type: (int, str) -> int
        """getattr 是已被弃用的特性

        Args:
            ptr (int): 任意整数
            attr (str): 任意字符串

        Returns:
            int: 总是返回 0
        """
        _, _ = ptr, attr
        return 0

    def setattr(self, obj_ptr, obj_attr, value_ptr):  # type: (int, str, int) -> bool
        """setattr 是已被弃用的特性

        Args:
            obj_ptr (int): 任意整数
            obj_attr (str): 任意字符串
            value_ptr (int): 任意整数

        Returns:
            bool: 总是返回 False
        """
        _, _, _ = obj_ptr, obj_attr, value_ptr
        return False

    def delattr(self, ptr, attr):  # type: (int, str) -> bool
        """delattr 是已被弃用的特性

        Args:
            ptr (int): 任意整数
            attr (str): 任意字符串

        Returns:
            bool: 总是返回 False
        """
        _, _ = ptr, attr
        return False

    def callable(self, ptr):  # type: (int) -> bool
        """callable 检查对象是否是可以调用的

        Args:
            ptr (int): 目标对象的指针

        Returns:
            bool: 对象是否是可以调用的
        """
        try:
            return callable(self._manager.deref(ptr))
        except Exception:
            return False

    def call(self, func_ptr, *arg_ptrs):  # type: (int, Any) -> int | str
        """
        call 是已被弃用的特性

        Args:
            func_ptr (int): 任意整数

        Returns:
            int | str:
                总是返回一个字符串式的错误信息，
                以指示关于该函数已被弃用的错误
        """
        _, _ = func_ptr, arg_ptrs
        return "call: Try to call a deprecated function"

    def compare_and(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """compare_and 对两个对象进行 and 运算

        Args:
            ptr_a (int): 第一个对象的指针
            ptr_b (int): 第二个对象的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) and self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def compare_or(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """compare_or 对两个对象进行 or 运算

        Args:
            ptr_a (int): 第一个对象的指针
            ptr_b (int): 第二个对象的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) or self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def compare_inverse(self, ptr):  # type: (int) -> int
        """compare_inverse 对对象进行 not 运算

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(not self._manager.deref(ptr))
        except Exception:
            return 0

    def compare_in(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """compare_in 计算 A in B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) in self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def add(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """add 对两个对象进行加法运算

        Args:
            ptr_a (int): 第一个对象的指针
            ptr_b (int): 第二个对象的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) + self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def remove(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """remove 计算 A-B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) - self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def times(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """times 对两个对象进行乘法运算

        Args:
            ptr_a (int): 第一个对象的指针
            ptr_b (int): 第二个对象的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) * self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def divide(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """divide 计算 A/B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) / self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def floordiv(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """floordiv 计算 A//B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) // self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def negative(self, ptr):  # type: (int) -> int
        """negative 对对象进行取负运算

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(-self._manager.deref(ptr))
        except Exception:
            return 0

    def abs(self, ptr):  # type: (int) -> int
        """abs 返回对象的绝对值

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(abs(self._manager.deref(ptr)))
        except Exception:
            return 0

    def round(self, ptr, ndigits=None):  # type: (int, int | None) -> int
        """
        round 将 ptr 指向的对象进行舍入运算

        Args:
            ptr (int):
                目标对象的指针
            ndigits (int | None, optional):
                舍入时所用的精度。
                默认值为 None

        Returns:
            int: 指向舍入结果的指针
        """
        if ndigits is None:
            return self._manager.ref(round(self._manager.deref(ptr)))
        else:
            return self._manager.ref(round(self._manager.deref(ptr), ndigits))

    def mod(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """mod 计算 A%B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) % self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def pow(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """pow 计算 pow(A, B) 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                pow(self._manager.deref(ptr_a), self._manager.deref(ptr_b))
            )
        except Exception:
            return 0

    def powmod(self, ptr_a, ptr_b, ptr_c):  # type: (int, int, int) -> int
        """powmod 计算 pow(A, B) % C 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针
            ptr_c (int): 对象 C 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                pow(
                    self._manager.deref(ptr_a),
                    self._manager.deref(ptr_b),
                    self._manager.deref(ptr_c),
                )
            )
        except Exception:
            return 0

    def greater(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """greater 计算 A > B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) > self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def less(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """less 计算 A < B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) < self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def greater_equal(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """greater_equal 计算 A >= B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) >= self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def less_equal(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """less_equal 计算 A <= B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) <= self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def equal(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """equal 计算 A == B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) == self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def not_equal(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """not_equal 计算 A != B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) != self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def bit_and(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """bit_and 计算 A & B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) & self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def bit_or(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """bit_or 计算 A | B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) | self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def bit_xor(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """bit_xor 计算 A⊕B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) ^ self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def bit_not(self, ptr):  # type: (int) -> int
        """bit_not 对对象进行按位取反运算

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(~self._manager.deref(ptr))
        except Exception:
            return 0

    def left_shift(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """left_shift 计算 A<<B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) << self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def right_shift(self, ptr_a, ptr_b):  # type: (int, int) -> int
        """right_shift 计算 A>>B 的值

        Args:
            ptr_a (int): 对象 A 的指针
            ptr_b (int): 对象 B 的指针

        Returns:
            int:
                如果成功，则返回指向运算结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(
                self._manager.deref(ptr_a) >> self._manager.deref(ptr_b)
            )
        except Exception:
            return 0

    def max(self, ptr):  # type: (int) -> int
        """max 返回对象中的最大值

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向最大值的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(max(self._manager.deref(ptr)))
        except Exception:
            return 0

    def min(self, ptr):  # type: (int) -> int
        """min 返回对象中的最小值

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向最小值的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(min(self._manager.deref(ptr)))
        except Exception:
            return 0

    def sum(self, ptr):  # type: (int) -> int
        """sum 返回对象中所有元素的和

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回指向求和结果的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(sum(self._manager.deref(ptr)))
        except Exception:
            return 0

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 reflect 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["reflect.cast"] = self.cast
        funcs["reflect.length"] = self.length
        funcs["reflect.copy"] = self.copy
        funcs["reflect.deepcopy"] = self.deepcopy
        funcs["reflect.format"] = self.format
        funcs["reflect.vars"] = self.vars  # Deprecated
        funcs["reflect.dir"] = self.dir  # Deprecated
        funcs["reflect.hasattr"] = self.hasattr  # Deprecated
        funcs["reflect.getattr"] = self.getattr  # Deprecated
        funcs["reflect.setattr"] = self.setattr  # Deprecated
        funcs["reflect.delattr"] = self.delattr  # Deprecated
        funcs["reflect.callable"] = self.callable
        funcs["reflect.call"] = self.call  # Deprecated
        funcs["reflect.and"] = self.compare_and
        funcs["reflect.or"] = self.compare_or
        funcs["reflect.inverse"] = self.compare_inverse
        funcs["reflect.in"] = self.compare_in
        funcs["reflect.add"] = self.add
        funcs["reflect.remove"] = self.remove
        funcs["reflect.times"] = self.times
        funcs["reflect.divide"] = self.divide
        funcs["reflect.floordiv"] = self.floordiv
        funcs["reflect.negative"] = self.negative
        funcs["reflect.abs"] = self.abs
        funcs["reflect.round"] = self.round
        funcs["reflect.mod"] = self.mod
        funcs["reflect.pow"] = self.pow
        funcs["reflect.powmod"] = self.powmod
        funcs["reflect.greater"] = self.greater
        funcs["reflect.less"] = self.less
        funcs["reflect.greater_equal"] = self.greater_equal
        funcs["reflect.less_equal"] = self.less_equal
        funcs["reflect.equal"] = self.equal
        funcs["reflect.not_equal"] = self.not_equal
        funcs["reflect.bit_and"] = self.bit_and
        funcs["reflect.bit_or"] = self.bit_or
        funcs["reflect.bit_xor"] = self.bit_xor
        funcs["reflect.bit_not"] = self.bit_not
        funcs["reflect.left_shift"] = self.left_shift
        funcs["reflect.right_shift"] = self.right_shift
        funcs["reflect.max"] = self.max
        funcs["reflect.min"] = self.min
        funcs["reflect.sum"] = self.sum

        for key, value in funcs.items():
            origin[key] = value
