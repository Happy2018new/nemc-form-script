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

    def format(self, number, accuracy=6):  # type: (int | float, int) -> str
        """
        format 将给定的数字格式化为其字符串表示

        Args:
            number (float | int):
                欲被格式化的数字
            accuracy (int):
                在格式化小数时所使用的精度。
                那些超出精度的部分将会丢失。
                默认值为 6

        Returns:
            str:
                给定数字的字符串表示
        """
        if isinstance(number, bool) or not isinstance(number, (int, float)):
            raise Exception("math.format: Target object is not a number")
        if isinstance(accuracy, bool) or not isinstance(accuracy, int):
            raise Exception("math.format: The given accuracy must be int")

        result = format(number, ".{}f".format(accuracy))
        if "." not in result:
            return result

        result = result.rstrip("0")
        if result.endswith("."):
            return result + "0"
        return result

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

        funcs["math.format"] = self.format
        funcs["math.round"] = lambda number, ndigits=None: (
            round(number) if ndigits is None else round(number, ndigits)
        )
        funcs["math.floordiv"] = lambda x, y: x // y
        funcs["math.mod"] = lambda a, b: a % b
        funcs["math.abs"] = lambda x: abs(x)
        funcs["math.max"] = lambda a, b: max(a, b)
        funcs["math.min"] = lambda a, b: min(a, b)
        funcs["math.bit_and"] = lambda a, b: a & b
        funcs["math.bit_or"] = lambda a, b: a | b
        funcs["math.bit_xor"] = lambda a, b: a ^ b
        funcs["math.bit_not"] = lambda a: ~a
        funcs["math.left_shift"] = lambda a, b: a << b
        funcs["math.right_shift"] = lambda a, b: a >> b
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
        funcs["math.pow"] = lambda x, y: math.pow(x, y)
        funcs["math.powmod"] = lambda x, y, mod: pow(x, y, mod)
        funcs["math.radians"] = lambda x: math.radians(x)
        funcs["math.sin"] = lambda x: math.sin(x)
        funcs["math.sinh"] = lambda x: math.sinh(x)
        funcs["math.sqrt"] = lambda x: math.sqrt(x)
        funcs["math.tan"] = lambda x: math.tan(x)
        funcs["math.tanh"] = lambda x: math.tanh(x)
        funcs["math.trunc"] = lambda x: math.trunc(x)

        for key, value in funcs.items():
            origin[key] = value
