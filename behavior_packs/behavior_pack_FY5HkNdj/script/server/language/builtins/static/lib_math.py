# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

import math
from .lib_object import BaseManager


class Math:
    """
    Math 提供了数学相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Math

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def _validate_int(self, obj):  # type: (Any) -> int
        """_validate_int 检查给定的对象是否为整数

        Args:
            obj (Any): 待检查的对象

        Raises:
            Exception:
                如果给定的对象不是整数，则抛出相应的错误

        Returns:
            int: 返回给定的对象，当且仅当它是整数时
        """
        if not isinstance(obj, int):
            raise Exception("_validate_int: Result {} is not an integer".format(obj))
        return obj

    def _validate_number(self, obj):  # type: (Any) -> int | float
        """_validate_number 检查给定的对象是否为实数

        Args:
            obj (Any): 待检查的对象

        Raises:
            Exception:
                如果给定的对象不是实数，则抛出相应的错误

        Returns:
            int | float:
                返回给定的对象，当且仅当它是实数时
        """
        if not isinstance(obj, (int, float)):
            raise Exception(
                "_validate_number: Result {} is not a real number".format(obj)
            )
        return obj

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 math 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["math.bit_and"] = lambda a, b: self._validate_int(a & b)
        funcs["math.bit_or"] = lambda a, b: self._validate_int(a | b)
        funcs["math.bit_xor"] = lambda a, b: self._validate_int(a ^ b)
        funcs["math.bit_not"] = lambda a: self._validate_int(~a)
        funcs["math.left_shift"] = lambda a, b: self._validate_int(a << b)
        funcs["math.right_shift"] = lambda a, b: self._validate_int(a >> b)
        funcs["math.acos"] = lambda x: math.acos(x)
        funcs["math.acosh"] = lambda x: math.acosh(x)
        funcs["math.asin"] = lambda x: math.asin(x)
        funcs["math.asinh"] = lambda x: math.asinh(x)
        funcs["math.atan"] = lambda x: math.atan(x)
        funcs["math.atan2"] = lambda y, x: math.atan2(y, x)
        funcs["math.atanh"] = lambda x: math.atanh(x)
        funcs["math.ceil"] = lambda x: math.ceil(x)
        funcs["math.cos"] = lambda x: math.cos(x)
        funcs["math.cosh"] = lambda x: math.cosh(x)
        funcs["math.degrees"] = lambda x: math.degrees(x)
        funcs["math.e"] = lambda: math.e
        funcs["math.erf"] = lambda x: math.erf(x)
        funcs["math.erfc"] = lambda x: math.erfc(x)
        funcs["math.exp"] = lambda x: math.exp(x)
        funcs["math.expm1"] = lambda x: math.expm1(x)
        funcs["math.fabs"] = lambda x: math.fabs(x)
        funcs["math.factorial"] = lambda x: math.factorial(x)
        funcs["math.floor"] = lambda x: math.floor(x)
        funcs["math.fmod"] = lambda x, y: math.fmod(x, y)
        funcs["math.frexp"] = lambda x: self._manager.ref(math.frexp(x))
        funcs["math.fsum"] = lambda ptr: math.fsum(self._manager.deref(ptr))
        funcs["math.gamma"] = lambda x: math.gamma(x)
        funcs["math.hypot"] = lambda x, y: math.hypot(x, y)
        funcs["math.isinf"] = lambda x: math.isinf(x)
        funcs["math.isnan"] = lambda x: math.isnan(x)
        funcs["math.ldexp"] = lambda x, i: math.ldexp(x, i)
        funcs["math.lgamma"] = lambda x: math.lgamma(x)
        funcs["math.log"] = lambda x, base=math.e: math.log(x, base)
        funcs["math.log10"] = lambda x: math.log10(x)
        funcs["math.log1p"] = lambda x: math.log1p(x)
        funcs["math.modf"] = lambda x: self._manager.ref(math.modf(x))
        funcs["math.pi"] = lambda: math.pi
        funcs["math.mod"] = lambda a, b: self._validate_int(a % b)
        funcs["math.pow"] = lambda x, y: math.pow(x, y)
        funcs["math.powmod"] = lambda x, y, mod: self._validate_number(pow(x, y, mod))
        funcs["math.radians"] = lambda x: math.radians(x)
        funcs["math.sin"] = lambda x: math.sin(x)
        funcs["math.sinh"] = lambda x: math.sinh(x)
        funcs["math.sqrt"] = lambda x: math.sqrt(x)
        funcs["math.tan"] = lambda x: math.tan(x)
        funcs["math.tanh"] = lambda x: math.tanh(x)
        funcs["math.trunc"] = lambda x: math.trunc(x)

        for key, value in funcs.items():
            origin[key] = value
