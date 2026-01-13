# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

import json
from .lib_object import BaseManager


class JSON:
    """
    JSON 提供了 JSON 相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 JSON

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def dumps(
        self,
        ptr,  # type: int
        skipkeys=False,  # type: bool
        ensure_ascii=True,  # type: bool
        check_circular=True,  # type: bool
        allow_nan=True,  # type: bool
        indent=None,  # type: int | str | None
        separators_ptr=None,  # type: int | None
        sort_keys=False,  # type: bool
    ):  # type: (...) -> str
        """
        Serialize ``obj`` to a JSON formatted ``str``.

        If ``skipkeys`` is true then ``dict`` keys that are not basic types
        (``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped
        instead of raising a ``TypeError``.

        If ``ensure_ascii`` is false, then the return value can contain non-ASCII
        characters if they appear in strings contained in ``obj``. Otherwise, all
        such characters are escaped in JSON strings.

        If ``check_circular`` is false, then the circular reference check
        for container types will be skipped and a circular reference will
        result in an ``RecursionError`` (or worse).

        If ``allow_nan`` is false, then it will be a ``ValueError`` to
        serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
        strict compliance of the JSON specification, instead of using the
        JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

        If ``indent`` is a non-negative integer, then JSON array elements and
        object members will be pretty-printed with that indent level. An indent
        level of 0 will only insert newlines. ``None`` is the most compact
        representation.

        If specified, ``separators`` should be an ``(item_separator, key_separator)``
        tuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and
        ``(',', ': ')`` otherwise.  To get the most compact JSON representation,
        you should specify ``(',', ':')`` to eliminate whitespace.

        If *sort_keys* is true (default: ``False``), then the output of
        dictionaries will be sorted by key.

        Returns:
            str: The JSON formatted string
        """
        obj = self._manager.deref(ptr)

        separators = None  # type: tuple[str, str] | None
        if separators_ptr is not None and separators_ptr != 0:
            separators = self._manager.deref(separators_ptr)

        return json.dumps(
            obj,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            indent=indent,
            separators=separators,
            sort_keys=sort_keys,
        )

    def loads(self, string):  # type: (str) -> int
        """
        loads 将字符串以 JSON 的格式解析。
        所得结果可能是一个映射，或其他类型

        Args:
            string (str): 待解析的字符串

        Returns:
            int: 解析后所得映射的指针
        """
        return self._manager.ref(json.loads(string))

    def fast_loads(self, string):  # type: (str) -> int | bool | float | str
        """
        fast_loads 将字符串以 JSON 的格式解析。
        它与 loads 的区别在于，它的解析结果应只
        可能是整数、布尔值、浮点数或字符串

        Args:
            string (str): 待解析的字符串

        Raises:
            Exception:
                如果解析失败，
                或解析结果不是整数、布尔值、浮点数或字符串，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                解析后所得的结果
        """
        result = json.loads(string)
        if not isinstance(result, (int, bool, float, str)):
            raise Exception(
                "json.fast_loads: The loaded result must be int, bool, float or str"
            )
        return result

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 json 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["json.dumps"] = self.dumps
        funcs["json.fast_dumps"] = lambda obj: self.dumps(obj, ensure_ascii=False)
        funcs["json.loads"] = self.loads
        funcs["json.fast_loads"] = self.fast_loads

        for key, value in funcs.items():
            origin[key] = value
