# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

from .lib_object import BaseManager


class Strings:
    """
    Strings 提供了对字符串的扩展操作
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Strings

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def _validate(self, string):  # type: (Any) -> str
        """_validate 验证给定的对象是否为字符串

        Args:
            string (Any): 待验证的对象

        Raises:
            Exception:
                如果给定的对象不是字符串，则抛出相应的错误

        Returns:
            str:
                返回给定的对象，当且仅当它是字符串时
        """
        if not isinstance(string, str):
            raise Exception("strings: Target object is not a string")
        return string

    def cast(self, ptr):  # type: (int) -> str
        """
        cast 将 ptr 指向的对象强制转换为字符串

        Args:
            ptr (int): 目标对象的指针

        Returns:
            str: 强制转换后所得的字符串
        """
        return str(self._manager.deref(ptr))

    def length(self, string):  # type: (str) -> int
        """length 返回字符串的长度

        Args:
            ptr (int): 给定的字符串

        Returns:
            int: 字符串的长度
        """
        return len(self._validate(string))

    def sub(self, string, start, end):  # type: (str, int, int) -> str
        """sub 返回字符串的子字符串

        Args:
            ptr (str): 给定的字符串
            start (int): 子字符串的起始索引
            end (int): 子字符串的结束索引

        Raises:
            Exception:
                如果给出的起始或结束索引超出字符串范围，
                或结束索引小于起始索引，则抛出相应的错误

        Returns:
            int: 产生的子字符串
        """
        _ = self._validate(string)

        if start < 0 or start > len(string):
            raise Exception(
                "strings.sub: Start index out of range [{}] with length {}".format(
                    start, len(string)
                )
            )
        if end < 0 or end > len(string):
            raise Exception(
                "strings.sub: End index out of range [{}] with length {}".format(
                    end, len(string)
                )
            )
        if end < start:
            raise Exception(
                "strings.sub: The end index can't be less than the start index (start={}, end={})".format(
                    start, end
                )
            )

        return string[start:end]

    def join(self, string, slice_ptr):  # type: (str, int) -> str
        """
        join 将切片中的元素以 string 作为分隔符连接形成一个新的字符串。
        join 的调用者有义务确保切片中的所有元素都是字符串，否则会发生错误

        Args:
            string (str): 用作分隔符的字符串
            slice_ptr (int): 目标切片的指针

        Raises:
            Exception:
                如果 slice_ptr 指向的对象不是切片，
                或切片中的某个元素不是字符串，
                则抛出相应的错误

        Returns:
            str: 连接所得的字符串
        """
        obj = self._manager.deref(slice_ptr)
        if not isinstance(obj, list):
            raise Exception("strings.join: Given ptr of slice is not a slice")
        return self._validate(string).join(obj)

    def split(
        self, string, sep=None, maxsplit=-1
    ):  # type: (str, str | None, int) -> int
        """
        split 将字符串按指定分隔符拆分为多个子字符串，
        并将这些子字符串按顺序放入一个新的切片中

        Args:
            string (str):
                要被拆分的字符串
            sep (str | None, optional):
                拆分所使用的分隔符。
                默认值为 None
            maxsplit (int, optional):
                最大拆分次数。
                默认值为 -1

        Returns:
            int: 所产生的切片的指针
        """
        return self._manager.ref(self._validate(string).split(sep, maxsplit))

    def rsplit(
        self, string, sep=None, maxsplit=-1
    ):  # type: (str, str | None, int) -> int
        """
        rsplit 将字符串按指定分隔符从右侧开始拆分为多个子字符串，
        并将这些子字符串按顺序放入一个新的切片中。

        rsplit 与 split 的唯一区别在于，
        rsplit 是从字符串的右侧开始拆分的，
        而 split 则是从左侧开始拆分的

        Args:
            string (str):
                给定的字符串
            sep (str | None, optional):
                分隔符。默认值为 None
            maxsplit (int, optional):
                最大拆分次数。默认值为 -1

        Returns:
            int: 所产生的切片的指针
        """
        return self._manager.ref(self._validate(string).rsplit(sep, maxsplit))

    def equalfold(self, string_a, string_b):  # type: (str, str) -> bool
        """
        equalfold 比较两个字符串在忽略大小写的情况下是否相等

        Args:
            string_a (str): 被比较的第一个字符串
            string_b (str): 被比较的第二个字符串

        Returns:
            bool: 两个字符串在忽略大小写的情况下是否相等
        """
        return self._validate(string_a).lower() == self._validate(string_b).lower()

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 strings 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["strings.cast"] = self.cast
        funcs["strings.length"] = self.length
        funcs["strings.sub"] = self.sub
        funcs["strings.capitalize"] = lambda string: self._validate(string).capitalize()
        funcs["strings.center"] = lambda string, width, fillchar=" ": self._validate(
            string
        ).center(width, fillchar)
        funcs["strings.startswith"] = (
            lambda string, prefix, start=None, end=None: self._validate(
                string
            ).startswith(prefix, start, end)
        )
        funcs["strings.endswith"] = (
            lambda string, prefix, start=None, end=None: self._validate(
                string
            ).endswith(prefix, start, end)
        )
        funcs["strings.find"] = (
            lambda string, prefix, start=None, end=None: self._validate(string).find(
                prefix, start, end
            )
        )
        funcs["strings.rfind"] = (
            lambda string, prefix, start=None, end=None: self._validate(string).rfind(
                prefix, start, end
            )
        )
        funcs["strings.index"] = (
            lambda string, prefix, start=None, end=None: self._validate(string).index(
                prefix, start, end
            )
        )
        funcs["strings.rindex"] = (
            lambda string, prefix, start=None, end=None: self._validate(string).rindex(
                prefix, start, end
            )
        )
        funcs["strings.isalnum"] = lambda string: self._validate(string).isalnum()
        funcs["strings.isalpha"] = lambda string: self._validate(string).isalpha()
        funcs["strings.isdigit"] = lambda string: self._validate(string).isdigit()
        funcs["strings.islower"] = lambda string: self._validate(string).islower()
        funcs["strings.isspace"] = lambda string: self._validate(string).isspace()
        funcs["strings.istitle"] = lambda string: self._validate(string).istitle()
        funcs["strings.isupper"] = lambda string: self._validate(string).isupper()
        funcs["strings.join"] = self.join
        funcs["strings.ljust"] = lambda string, width, fillchar=" ": self._validate(
            string
        ).ljust(width, fillchar)
        funcs["strings.rjust"] = lambda string, width, fillchar=" ": self._validate(
            string
        ).rjust(width, fillchar)
        funcs["strings.lower"] = lambda string: self._validate(string).lower()
        funcs["strings.upper"] = lambda string: self._validate(string).upper()
        funcs["strings.lstrip"] = lambda string, chars=None: self._validate(
            string
        ).lstrip(chars)
        funcs["strings.rstrip"] = lambda string, chars=None: self._validate(
            string
        ).rstrip(chars)
        funcs["strings.strip"] = lambda string, chars=None: self._validate(
            string
        ).strip(chars)
        funcs["strings.replace"] = lambda string, old, new, count=-1: self._validate(
            string
        ).replace(old, new, count)
        funcs["strings.split"] = self.split
        funcs["strings.rsplit"] = self.rsplit
        funcs["strings.swapcase"] = lambda string: self._validate(string).swapcase()
        funcs["strings.title"] = lambda string: self._validate(string).title()
        funcs["strings.zfill"] = lambda string, width: self._validate(string).zfill(
            width
        )
        funcs["strings.equalfold"] = self.equalfold

        for key, value in funcs.items():
            origin[key] = value
