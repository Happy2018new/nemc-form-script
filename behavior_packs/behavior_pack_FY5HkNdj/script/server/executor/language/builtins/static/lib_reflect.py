# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable, Any

import copy
from .lib_object import BaseManager
from .checker.checker import check_object


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
        """length 返回对象的长度

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回目标对象的长度；
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
        """vars 返回对象的属性字典

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回对应映射的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(vars(self._manager.deref(ptr)))
        except Exception:
            return 0

    def dir(self, ptr):  # type: (int) -> int
        """dir 返回对象的属性列表

        Args:
            ptr (int): 目标对象的指针

        Returns:
            int:
                如果成功，则返回对应切片的指针；
                否则失败，那么返回 0
        """
        try:
            return self._manager.ref(dir(self._manager.deref(ptr)))
        except Exception:
            return 0

    def hasattr(self, ptr, attr):  # type: (int, str) -> bool
        """
        hasattr 检查对象是否拥有 attr 指示的属性

        Args:
            ptr (int): 目标对象的指针
            attr (str): 欲检查的属性的名称

        Returns:
            bool: 目标对象是否拥有该属性
        """
        try:
            return hasattr(self._manager.deref(ptr), attr)
        except Exception:
            return False

    def getattr(self, ptr, attr):  # type: (int, str) -> int
        """
        getattr 获取对象在 attr 上指示的属性。
        如果 attr 或目标属性是受保护的特性，则将返回 0

        Args:
            ptr (int): 目标对象的指针
            attr (str): 欲获取的属性的名称

        Returns:
            int:
                如果成功，则返回该属性对应对象的指针；
                否则失败，那么返回 0
        """
        if attr.startswith("_"):
            return 0

        try:
            result = getattr(self._manager.deref(ptr), attr)
        except Exception:
            return 0
        if attr.startswith("_") or not check_object(result):
            return 0

        return self._manager.ref(result)

    def setattr(self, obj_ptr, obj_attr, value_ptr):  # type: (int, str, int) -> bool
        """
        setattr 设置对象在 obj_attr 上指示的属性。
        如果 obj_attr 是受保护的特性，则将返回 False

        Args:
            obj_ptr (int): 目标对象的指针
            obj_attr (str): 欲设置的属性的名称
            value_ptr (int): 要设置的值的指针

        Returns:
            bool: 操作是否成功
        """
        if obj_attr.startswith("_"):
            return False
        try:
            setattr(
                self._manager.deref(obj_ptr), obj_attr, self._manager.deref(value_ptr)
            )
            return True
        except Exception:
            return False

    def delattr(self, ptr, attr):  # type: (int, str) -> bool
        """
        delattr 删除对象在 attr 上指示的属性。
        如果 attr 是受保护的特性，则将返回 False

        Args:
            ptr (int): 目标对象的指针
            attr (str): 欲删除的属性的名称

        Returns:
            bool: 操作是否成功
        """
        if attr.startswith("_"):
            return False
        try:
            delattr(self._manager.deref(ptr), attr)
            return True
        except Exception:
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
        call 调用 func_ptr 所指向的函数。
        arg_ptrs 是要传入的参数，
        所有这些参数都应须是指针

        Args:
            func_ptr (int):
                欲调用的函数的指针

        Returns:
            int | str:
                如果成功，则返回函数调用后所得对象的指针；
                否则失败，那么返回错误信息的字符串形式
        """
        func = self._manager.deref(func_ptr)
        args = [self._manager.deref(i) for i in arg_ptrs]
        try:
            return self._manager.ref(func(*args))
        except Exception as e:
            return str(e)

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
        """rempove 计算 A-B 的值

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
        funcs["reflect.vars"] = self.vars
        funcs["reflect.dir"] = self.dir
        funcs["reflect.hasattr"] = self.hasattr
        funcs["reflect.getattr"] = self.getattr
        funcs["reflect.setattr"] = self.setattr
        funcs["reflect.delattr"] = self.delattr
        funcs["reflect.callable"] = self.callable
        funcs["reflect.call"] = self.call
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
