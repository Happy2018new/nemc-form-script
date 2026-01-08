# -*- coding: utf-8 -*-

from ..reader.any_reader import AnyReader
from ..reader.string_reader import StringReader
from .token import (
    Token,
    CHAR_TO_TOKEN_ID,
    KEY_WORD_TO_TOKEN_ID,
    TOKEN_ID_WORD,
    TOKEN_ID_SINGLE_QUOTE,
)


class Sentence:
    """
    Sentence 是词法分词实现。
    它通过多个 Token 构成了句子
    """

    reader = StringReader("")  # type: StringReader
    tokens = []  # type: list[Token]

    def __init__(self, reader):  # type: (StringReader) -> None
        """初始化并返回一个新的词法分词器

        Args:
            reader (StringReader):
                用于读取源代码的底层流
        """
        self.reader = reader
        self.tokens = []

    def parse_all(self):  # type: () -> tuple[int, int, Exception | None]
        """
        parse_all 通过不断地调用 parse_next 直到底层流被耗尽。
        最终，parse_next 读取到了所有的 Token，分词工作被完成。
        应注意的是，分词结果被保存到当前实例的 tokens 列表中

        Returns:
            tuple[int, int, Exception | None]:
                元组的第一个元素表示分词开始时底层流的指针位置，
                元组的第二个元素表示分词结束（或发生错误时）时底层流的指针位置。
                另外，如果分词过程中发生错误，则该元组的第三个元素将有值
        """
        ptr = self.reader.pointer()

        while True:
            ptr = self.reader.pointer()
            try:
                if not self.parse_next():
                    break
            except Exception as e:
                return ptr, self.reader.pointer(), e

        return ptr, self.reader.pointer(), None

    def parse_next(self):  # type: () -> bool
        """
        parse_next 从底层流解析一个 Token，
        并将其追加到当前实例的 tokens 列表中

        Returns:
            bool:
                指示解析是否成功。
                如果返回假，则说明底层流已被耗尽
        """
        self.reader.jump_space()
        ptr = self.reader.pointer()
        word = self.reader.read(1)

        if word == "":
            return False
        if word == "'":
            self.tokens.append(
                Token(
                    TOKEN_ID_SINGLE_QUOTE,
                    self.reader.parse_string(),
                    ptr,
                    self.reader.pointer(),
                )
            )
            return True
        if word in CHAR_TO_TOKEN_ID:
            self.tokens.append(
                Token(
                    CHAR_TO_TOKEN_ID[word],
                    "",
                    ptr,
                    self.reader.pointer(),
                )
            )
            return True

        while True:
            char = self.reader.read(1)
            if char == "":
                break
            if char == " " or char == "\t" or char in CHAR_TO_TOKEN_ID:
                _ = self.reader.unread(1)
                break
            word += char

        if word in KEY_WORD_TO_TOKEN_ID:
            self.tokens.append(
                Token(
                    KEY_WORD_TO_TOKEN_ID[word],
                    "",
                    ptr,
                    self.reader.pointer(),
                )
            )
        else:
            self.tokens.append(
                Token(
                    TOKEN_ID_WORD,
                    word,
                    ptr,
                    self.reader.pointer(),
                )
            )
        return True


class SentenceReader(AnyReader):
    """
    SentenceReader 是多个 Token 组成的流式阅读器。
    它应当通过 Sentence 的分词结果来进行初始化
    """

    _contents = []  # type: list[Token]
    _pointer = 0  # type: int

    def __init__(self, tokens=[], pointer=0):  # type: (list[Token], int) -> None
        """初始化并返回一个新的 SentenceReader

        Args:
            tokens (list[Token], optional):
                词法分词器的分词结果列表。
                默认值为空列表
            pointer (int, optional):
                该阅读器的指针初始位置。
                默认值为 0
        """
        self._contents = tokens if len(tokens) > 0 else []
        self._pointer = min(max(0, pointer), len(tokens) - 1)

    def contents(self):  # type: () -> list[Token]
        """contents 返回阅读器的底层负载

        Returns:
            list[Token]:
                阅读器的底层负载
        """
        return self._contents

    def read(self):  # type: () -> Token | None
        """read 从当前流中阅读一个 Token

        Returns:
            Token | None:
                返回读到的 Token。
                如果流已被耗尽，则返回 None
        """
        return AnyReader.read(self)

    def unread(self):  # type: () -> SentenceReader
        """
        unread 在形式上等于撤销上一次 read 操作。
        其底层实现则是将阅读指针向列表前端移动

        Raises:
            Exception:
                如果阅读指针已在最开头，
                则抛出响应的错误

        Returns:
            SentenceReader:
                返回 SentenceReader 本身
        """
        AnyReader.unread(self)
        return self

    def must_read(self):  # type: () -> Token
        """
        must_read 从流中阅读一个 Token。
        如果流已被耗尽，则抛出相应的错误

        must_read 是对 read 的进一步封装。
        它在形式上确保内部进行了边界测试，
        因此外部调用者可以以简单的方式阅读

        Raises:
            Exception:
                如果流已被耗尽，
                则抛出相应的错误

        Returns:
            Token:
                返回读到的 Token
        """
        return AnyReader.must_read(self)
