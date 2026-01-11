# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

import binascii
from .lib_object import BaseManager


class Binascii:
    """
    Binascii 提供了二进制与 ASCII 码相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Binascii

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def a2b_base64(self, string):  # type: (str) -> int | str
        """
        a2b_base64 将给定的 Base64 编码字符串解码为二进制数据

        Args:
            string (str):
                待解码的字符串

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        result = binascii.a2b_base64(string)
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def a2b_hex(self, string):  # type: (str) -> int | str
        """
        a2b_hex 将给定的十六进制编码字符串解码为二进制数据

        Args:
            string (str): 待解码的字符串

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        result = binascii.a2b_hex(string)
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def b2a_base64(self, ptr_or_str):  # type: (int | str) -> str
        """
        b2a_base64 将给定的二进制数据编码为 Base64 字符串

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象编码；
                否则，提供的是字符串，则将直接对其进行编码

        Returns:
            str: 编码后的 Base64 字符串
        """
        if isinstance(ptr_or_str, int):
            obj_a = self._manager.deref(ptr_or_str)  # type: bytes
            return binascii.b2a_base64(obj_a).decode(encoding="utf-8")
        else:
            temp = ptr_or_str  # type: Any
            obj_b = temp  # type: bytes
            return str(binascii.b2a_base64(obj_b))

    def b2a_hex(self, ptr_or_str):  # type: (int | str) -> str
        """
        b2a_hex 将给定的二进制数据编码为十六进制字符串

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象编码；
                否则，提供的是字符串，则将直接对其进行编码

        Returns:
            str: 编码后的十六进制字符串
        """
        if isinstance(ptr_or_str, int):
            obj_a = self._manager.deref(ptr_or_str)  # type: bytes
            return binascii.b2a_hex(obj_a).decode(encoding="utf-8")
        else:
            temp = ptr_or_str  # type: Any
            obj_b = temp  # type: bytes
            return str(binascii.b2a_hex(obj_b))

    def hexlify(self, ptr_or_str):  # type: (int | str) -> str
        """
        hexlify 将给定的二进制数据编码为十六进制字符串。
        应当说明的是，该函数与 b2a_hex 具有相同的效果

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象编码；
                否则，提供的是字符串，则将直接对其进行编码

        Returns:
            str: 编码后的十六进制字符串
        """
        if isinstance(ptr_or_str, int):
            obj_a = self._manager.deref(ptr_or_str)  # type: bytes
            return binascii.hexlify(obj_a).decode(encoding="utf-8")
        else:
            temp = ptr_or_str  # type: Any
            obj_b = temp  # type: bytes
            return str(binascii.hexlify(obj_b))

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 binascii 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["binascii.a2b_base64"] = self.a2b_base64
        funcs["binascii.a2b_hex"] = self.a2b_hex
        funcs["binascii.b2a_base64"] = self.b2a_base64
        funcs["binascii.b2a_hex"] = self.b2a_hex
        funcs["binascii.hexlify"] = self.hexlify

        for key, value in funcs.items():
            origin[key] = value
