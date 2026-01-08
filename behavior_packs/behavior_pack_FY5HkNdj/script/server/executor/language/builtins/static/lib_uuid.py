# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

import uuid
from .lib_object import BaseManager


class UUID:
    """
    UUID 提供了对 UUID 的内置操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 UUID

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def new(self):  # type: () -> int
        """
        new 创建并返回一个新的 UUID

        Returns:
            int: 新创建的 UUID 的指针
        """
        return self._manager.ref(uuid.uuid4())

    def format(self, ptr):  # type: (int) -> str
        """format 返回 UUID 的字符串表示

        Args:
            ptr (int): 目标 UUID 的指针

        Raises:
            Exception:
                如果目标对象不是 UUID，则抛出相应的错误

        Returns:
            str: 目标 UUID 的字符串表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, uuid.UUID):
            raise Exception("uuid.format: Target object is not a UUID")
        return obj.__repr__()

    def to_string(self, ptr):  # type: (int) -> str
        """to_string 将 UUID 转换为字符串

        Args:
            ptr (int): 目标 UUID 的指针

        Raises:
            Exception:
                如果目标对象不是 UUID，则抛出相应的错误

        Returns:
            str: 转换所得的字符串
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, uuid.UUID):
            raise Exception("uuid.string: Target object is not a UUID")
        return str(obj)

    def to_bytes(self, ptr):  # type: (int) -> int | str
        """to_bytes 返回 UUID 的字节表示

        Args:
            ptr (int): 目标 UUID 的指针

        Raises:
            Exception:
                如果目标对象不是 UUID，则抛出相应的错误

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, uuid.UUID):
            raise Exception("uuid.bytes: Target object is not a UUID")
        result = obj.bytes
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def to_bytes_le(self, ptr):  # type: (int) -> int | str
        """
        to_bytes_le 返回 UUID 在小端序上的字节表示

        Args:
            ptr (int): 目标 UUID 的指针

        Raises:
            Exception:
                如果目标对象不是 UUID，则抛出相应的错误

        Returns:
            int | str:
                如果返回了一个整数，则它是一个指向了 bytes 的指针；
                否则，返回了一个字符串，表示其在较低 Python 版本中的结果
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, uuid.UUID):
            raise Exception("uuid.bytes_le: Target object is not a UUID")
        result = obj.bytes_le
        if isinstance(result, str):
            return result
        return self._manager.ref(result)

    def to_hex(self, ptr):  # type: (int) -> str
        """to_hex 返回 UUID 的十六进制表示

        Args:
            ptr (int): 目标 UUID 的指针

        Raises:
            Exception:
                如果目标对象不是 UUID，则抛出相应的错误

        Returns:
            str: 目标 UUID 的十六进制表示
        """
        obj = self._manager.deref(ptr)
        if not isinstance(obj, uuid.UUID):
            raise Exception("uuid.hex: Target object is not a UUID")
        return obj.hex

    def from_string(self, string):  # type: (str) -> int
        """
        from_string 试图从一个字符串解析一个 UUID。
        from_string 与 to_string 是互相对应的

        Args:
            string (str): 给定的字符串

        Returns:
            int: 新创建的 UUID 的指针
        """
        return self._manager.ref(uuid.UUID(string))

    def from_bytes(self, ptr_or_str):  # type: (int | str) -> int
        """from_bytes 从字节表示创建一个 UUID

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象创建 UUID；
                否则，提供的是字符串，则将直接从该字符串表示的字节创建

        Returns:
            int: 新创建的 UUID 的指针
        """
        if isinstance(ptr_or_str, int):
            return self._manager.ref(uuid.UUID(bytes=self._manager.deref(ptr_or_str)))
        else:
            return self._manager.ref(uuid.UUID(bytes=ptr_or_str))  # type: ignore

    def from_bytes_le(self, ptr_or_str):  # type: (int | str) -> int
        """from_bytes_le 从小端序的字节表示创建一个 UUID

        Args:
            ptr_or_str (int | str):
                如果提供的是整数，则将从它指向的 bytes 对象创建 UUID；
                否则，提供的是字符串，则将直接从该字符串表示的字节创建

        Returns:
            int: 新创建的 UUID 的指针
        """
        if isinstance(ptr_or_str, int):
            return self._manager.ref(
                uuid.UUID(bytes_le=self._manager.deref(ptr_or_str))
            )
        else:
            return self._manager.ref(uuid.UUID(bytes_le=ptr_or_str))  # type: ignore

    def from_hex(self, string):  # type: (str) -> int
        """from_hex 从十六进制表示创建一个 UUID

        Args:
            string (str): 目标 UUID 的十六进制表示

        Returns:
            int: 新创建的 UUID 的指针
        """
        return self._manager.ref(uuid.UUID(hex=string))

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 uuid 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["uuid.new"] = self.new
        funcs["uuid.format"] = self.format
        funcs["uuid.string"] = self.to_string
        funcs["uuid.bytes"] = self.to_bytes
        funcs["uuid.bytes_le"] = self.to_bytes_le
        funcs["uuid.hex"] = self.to_hex
        funcs["uuid.from_string"] = self.from_string
        funcs["uuid.from_bytes"] = self.from_bytes
        funcs["uuid.from_bytes_le"] = self.from_bytes_le
        funcs["uuid.from_hex"] = self.from_hex

        for key, value in funcs.items():
            origin[key] = value
