# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

import base64
from .lib_object import BaseManager


class Base64:
    """
    Base64 提供了 base64 相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Base64

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def b16decode(self, string, casefold=False):  # type: (str, bool) -> int | str
        """b16decode 解码一个 Base16 编码的字符串

        Args:
            string (str):
                待解码的字符串
            casefold (bool, optional):
                是否忽略大小写。
                默认值为 False

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        result = base64.b16decode(string, casefold)
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def b16encode(self, ptr_or_str):  # type: (int | str) -> str
        """b16encode 将给定的对象按 Base16 编码

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象解码；
                否则，提供的是字符串，则将直接对其进行解码

        Returns:
            str: 编码所得的 Base16 字符串
        """
        if isinstance(ptr_or_str, int):
            obj_a = self._manager.deref(ptr_or_str)  # type: bytes
            return base64.b16encode(obj_a).decode(encoding="utf-8")
        else:
            temp = ptr_or_str  # type: Any
            obj_b = temp  # type: bytes
            return base64.b16encode(obj_b).decode(encoding="utf-8")

    def b32decode(self, string, casefold=False):  # type: (str, bool) -> int | str
        """b32decode 解码一个 Base32 编码的字符串

        Args:
            string (str):
                待解码的字符串
            casefold (bool, optional):
                是否忽略大小写。
                默认值为 False

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        result = base64.b32decode(string, casefold)
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def b32encode(self, ptr_or_str):  # type: (int | str) -> str
        """b32encode 将给定的对象按 Base32 编码

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象解码；
                否则，提供的是字符串，则将直接对其进行解码

        Returns:
            str: 编码所得的 Base32 字符串
        """
        if isinstance(ptr_or_str, int):
            obj_a = self._manager.deref(ptr_or_str)  # type: bytes
            return base64.b32encode(obj_a).decode(encoding="utf-8")
        else:
            temp = ptr_or_str  # type: Any
            obj_b = temp  # type: bytes
            return base64.b32encode(obj_b).decode(encoding="utf-8")

    def b64decode(self, string, altchars=None):  # type: (str, str | None) -> int | str
        """b64decode 解码一个 Base64 编码的字符串

        Args:
            string (str): 待解码的字符串
            altchars (str | None, optional):
                可选的替代字符，用于替换标准 Base64 字符集中的 '+' 和 '/'。
                默认值为 None

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        result = base64.b64decode(string, altchars)
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def b64encode(self, ptr_or_str):  # type: (int | str) -> str
        """b64encode 将给定的对象按 Base64 编码

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象解码；
                否则，提供的是字符串，则将直接对其进行解码

        Returns:
            str: 编码所得的 Base64 字符串
        """
        if isinstance(ptr_or_str, int):
            obj_a = self._manager.deref(ptr_or_str)  # type: bytes
            return base64.b64encode(obj_a).decode(encoding="utf-8")
        else:
            temp = ptr_or_str  # type: Any
            obj_b = temp  # type: bytes
            return base64.b64encode(obj_b).decode(encoding="utf-8")

    def standard_b64decode(self, string):  # type: (str) -> int | str
        """standard_b64decode 按 Base64 标准解码一个字符串

        Args:
            string (str): 待解码的字符串

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        result = base64.standard_b64decode(string)
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def standard_b64encode(self, ptr_or_str):  # type: (int | str) -> str
        """standard_b64encode 按 Base64 标准进行编码

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象解码；
                否则，提供的是字符串，则将直接对其进行解码

        Returns:
            str: 编码所得的 Base64 字符串
        """
        if isinstance(ptr_or_str, int):
            obj_a = self._manager.deref(ptr_or_str)  # type: bytes
            return base64.standard_b64encode(obj_a).decode(encoding="utf-8")
        else:
            temp = ptr_or_str  # type: Any
            obj_b = temp  # type: bytes
            return base64.standard_b64encode(obj_b).decode(encoding="utf-8")

    def urlsafe_b64decode(self, string):  # type: (str) -> int | str
        """urlsafe_b64decode 解码一个 URL 安全的 Base64 编码字符串

        Args:
            string (str): 待解码的字符串

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        result = base64.urlsafe_b64decode(string)
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def urlsafe_b64encode(self, ptr_or_str):  # type: (int | str) -> str
        """
        urlsafe_b64encode 编码一个 Base64 字符串，
        并确保其对于 URL 是安全的

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象解码；
                否则，提供的是字符串，则将直接对其进行解码

        Returns:
            str: 编码所得的 Base64 字符串
        """
        if isinstance(ptr_or_str, int):
            obj_a = self._manager.deref(ptr_or_str)  # type: bytes
            return base64.urlsafe_b64encode(obj_a).decode(encoding="utf-8")
        else:
            temp = ptr_or_str  # type: Any
            obj_b = temp  # type: bytes
            return base64.urlsafe_b64encode(obj_b).decode(encoding="utf-8")

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 base64 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["base64.b16decode"] = self.b16decode
        funcs["base64.b16encode"] = self.b16encode
        funcs["base64.b32decode"] = self.b32decode
        funcs["base64.b32encode"] = self.b32encode
        funcs["base64.b64decode"] = self.b64decode
        funcs["base64.b64encode"] = self.b64encode
        funcs["base64.standard_b64decode"] = self.standard_b64decode
        funcs["base64.standard_b64encode"] = self.standard_b64encode
        funcs["base64.urlsafe_b64decode"] = self.urlsafe_b64decode
        funcs["base64.urlsafe_b64encode"] = self.urlsafe_b64encode

        for key, value in funcs.items():
            origin[key] = value
