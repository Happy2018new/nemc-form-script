# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any


class AnyReader:
    """
    AnyReader 是通用的流式阅读器。
    其底层实现是由列表和指针构成的
    """

    _contents = []  # type: list[Any]
    _pointer = 0  # type: int

    def __init__(self, contents, pointer=0):  # type: (list[Any], int) -> None
        """初始化并返回一个新的 AnyReader

        Args:
            contents (list[Any]):
                阅读器的底层负载
            pointer (int, optional):
                阅读指针的起始位置。
                默认值为 0
        """
        self._contents = contents
        self._pointer = min(max(0, pointer), len(contents) - 1)

    def contents(self):  # type: () -> list[Any]
        """contents 返回阅读器的底层负载

        Returns:
            list[Any]:
                阅读器的底层负载
        """
        return self._contents

    def pointer(self):  # type: () -> int
        """pointer 返回当前阅读指针的位置

        Returns:
            int: 阅读指针当前的位置
        """
        return self._pointer

    def set_pointer(self, ptr):  # type: (int) -> None
        """
        set_pointer 设置阅读指针的位置。
        如果给定的指针超出范围，也不会出现问题

        Args:
            ptr (int): 阅读指针的新位置
        """
        self._pointer = ptr
        if self._pointer < 0:
            self._pointer = 0
        if self._pointer > len(self._contents):
            self._pointer = len(self._contents)

    def read(self):  # type: () -> Any | None
        """read 从当前流中阅读一个元素

        Returns:
            Any | None:
                返回所读的元素。
                如果流已被耗尽，则返回 None
        """
        if self._pointer >= len(self._contents):
            return None
        self._pointer += 1
        return self._contents[self._pointer - 1]

    def unread(self):  # type: () -> AnyReader
        """
        unread 在形式上等于撤销上一次 read 操作。
        其底层实现则是将阅读指针向列表前端移动

        Raises:
            Exception:
                如果阅读指针已在最开头，
                则抛出响应的错误

        Returns:
            AnyReader:
                返回 AnyReader 本身
        """
        self._pointer -= 1
        if self._pointer < 0:
            self._pointer = 0
            raise Exception("unread: Try unread in the beginning")
        return self

    def must_read(self):  # type: () -> Any
        """
        must_read 从流中阅读一个元素。
        如果流已被耗尽，则抛出相应的错误

        must_read 是对 read 的进一步封装。
        它在形式上确保内部进行了边界测试，
        因此外部调用者可以以简单的方式阅读

        Raises:
            Exception:
                如果流已被耗尽，
                则抛出相应的错误

        Returns:
            Any:
                返回所读的元素
        """
        element = self.read()
        if element is None:
            raise Exception("must_read: Unexpected EOF")
        return element
