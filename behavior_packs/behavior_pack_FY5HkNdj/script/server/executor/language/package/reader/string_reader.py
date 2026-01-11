# -*- coding: utf-8 -*-


class StringReader:
    """StringReader 是字符串流式阅读器"""

    _buffer = ""
    _pointer = 0

    def __init__(self, buffer, pointer=0):  # type: (str, int) -> None
        """初始化并返回一个新的字符串流式阅读器

        Args:
            buffer (str):
                字符串阅读器的底层负载
            pointer (int, optional):
                字符串阅读器的指针位置
                默认值为 0
        """
        self._buffer = buffer
        self._pointer = min(max(0, pointer), len(buffer))

    def buffer(self):  # type: () -> str
        """buffer 返回该阅读器的底层负载

        Returns:
            str: 字符串阅读器的底层负载
        """
        return self._buffer

    def pointer(self):  # type: () -> int
        """pointer 返回该阅读器的指针位置

        Returns:
            int: 字符串阅读器的指针位置
        """
        return self._pointer

    def set_pointer(self, ptr):  # type: (int) -> None
        """
        set_pointer 设置该阅读器的指针位置。
        如果给定的指针超出范围，也不会出现问题

        Args:
            ptr (int): 指针的新位置
        """
        self._pointer = ptr
        if self._pointer < 0:
            self._pointer = 0
        if self._pointer > len(self._buffer):
            self._pointer = len(self._buffer)

    def read(self, n):  # type: (int) -> str
        """read 从当前流中阅读 n 个字符

        Args:
            n (int):
                要阅读的字符串数

        Returns:
            str:
                阅读到的字符串。如果流已被提前耗尽，
                则返回的字符串的长度可能小于 n
        """
        result = self._buffer[self._pointer : self._pointer + n]
        self._pointer = min(self._pointer + n, len(self._buffer))
        return result

    def unread(self, n):  # type: (int) -> StringReader
        """
        unread 撤销 n 个字符的 read 操作。
        在形式它，它是对 read(n) 的逆操作

        Args:
            n (int):
                要撤销的字符数

        Raises:
            Exception:
                如果撤销后的指针位置早于流的起点，
                则抛出相应的错误

        Returns:
            StringReader:
                返回 StringReader 本身
        """
        self._pointer -= n
        if self._pointer < 0:
            self._pointer = 0
            raise Exception(
                "unread: Try unread to the position that beyond the beginning"
            )
        return self

    def jump_space(self):  # type: () -> None
        """
        jump_space 不断地从底层流阅读，
        直到遇到非制表符或非制表符的字符为止。

        如果流已被耗尽，则它将停止阅读。
        确保在这种情况下不会抛出错误。

        在形式上，jump_space 的作用相当于跳过空白字符，
        以便下次阅读时能读取到具有实际意义的字符。
        """
        while True:
            char = self.read(1)
            if char == " " or char == "\t":
                continue
            if char != "":
                _ = self.unread(1)
            break

    def parse_string(self):  # type: () -> str
        """
        parse_string 试图从底层流解析一个由单引号包裹的字符串。
        实际上，它不断的读取字符，直到遇到一个单引号时终止阅读

        单引号包裹的字符串中允许使用转义符，
        这意味着 parse_string 可以正确处理转义符，
        其中也就包括被转义的单引号

        Raises:
            Exception:
                如果底层流提前耗尽，则抛出相应的错误

        Returns:
            str:
                解析所得的，由单引号包裹的字符串。
                确保所有转义符已得到正确处理
        """
        result = ""
        while True:
            char = self.read(1)
            if char == "":
                raise Exception("parse_string: Unexpected EOF")
            if char == "\\":
                sub = char + self.read(1)
                sub = str(sub.encode().decode(encoding="unicode_escape"))
                result += sub
                continue
            if char == "'":
                break
            result += char
        return result
