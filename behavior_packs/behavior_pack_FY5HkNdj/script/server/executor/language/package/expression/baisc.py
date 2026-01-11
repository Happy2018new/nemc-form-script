# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from .combine import ExpressionCombine

from .define import (
    ExpressionElement,
    CONTEXT_PARSE_ARGUMENT,
    CONTEXT_PARSE_SUB_EXPR,
    CONTEXT_PARSE_BARRIER,
    TYPE_ENUM_INT,
    TYPE_ENUM_BOOL,
    TYPE_ENUM_FLOAT,
    TYPE_ENUM_STR,
    ELEMENT_ID_REF,
    ELEMENT_ID_SELECTOR,
    ELEMENT_ID_SCORE,
    ELEMENT_ID_COMMAND,
    ELEMENT_ID_FUNC,
)
from ..token.sentence import SentenceReader
from ..token.token import (
    TOKEN_ID_WORD,
    TOKEN_ID_LEFT_BRACKET,
    TOKEN_ID_RIGHT_BRACKET,
    TOKEN_ID_COMMA,
    TOKEN_ID_KEY_WORD_INT,
    TOKEN_ID_KEY_WORD_BOOL,
    TOKEN_ID_KEY_WORD_STR,
    TOKEN_ID_KEY_WORD_FLOAT,
)

try:
    range = xrange  # type: ignore
except Exception:
    pass


class ExpressionNormal(ExpressionElement):
    """
    ExpressionNormal
    是普通的表达式元素，
    它没有任何负载。

    就目前而言，它仅作为
    复杂表达式在解析时所
    使用的中间媒介。

    应确保最终所得的复杂
    表达式中不会出现当前
    类的任何实例
    """

    element_id = 0
    element_payload = None

    def __init__(self, element_id):  # type: (int) -> None
        """初始化并返回一个新的 ExpressionNormal

        Args:
            element_id (int): 该普通表达式元素的元素 ID
        """
        self.element_id = element_id
        self.element_payload = None


class ExpressionLiteral(ExpressionElement):
    """
    ExpressionLiteral 在狭义上指示字面量表达式元素。
    这意味着它可以直接储存字面量，例如整数、布尔值、浮点数和字符串。

    但广义上，它亦可以指示一个变量，或者针对复杂表达式的强制类型转换。
    对于复杂表达式，将由其他实现在运行时求值，然后再进行强制类型转换
    """

    element_id = 0  # type: int
    element_payload = 0  # type: int | bool | float | str | ExpressionCombine

    def __init__(
        self, element_id, element_payload
    ):  # type: (int, int | bool | float | str | ExpressionCombine) -> None
        """初始化并返回一个新的 ExpressionLiteral

        Args:
            element_id (int):
                该字面量表达式元素的元素 ID。
                应只可能是以下几种之一。
                    - ELEMENT_ID_VAR
                    - ELEMENT_ID_INT
                    - ELEMENT_ID_BOOL
                    - ELEMENT_ID_FLOAT
                    - ELEMENT_ID_STR
            element_payload (int | bool | float | str | ExpressionCombine):
                该字面量表达式元素的负载。如果它只承载一个字面量，则应是整数、布尔值、浮点数或字符串。
                否则，它指示变量，或对复杂表达式的强制类型转换，所以它需要是复杂表达式或变量。
                对于变量，我们通过字符串来表示变量的名字，因此 element_payload 在此时应是字符串
        """
        self.element_id = element_id
        self.element_payload = element_payload

    def parse(
        self, reader, layer=0
    ):  # type: (SentenceReader, int) -> ExpressionLiteral
        """
        parse 从底层流解析一个复杂表达式到当前字面量表达式元素的负载中。
        这不会改变本字面量表达式元素的元素 ID。

        parse 的调用通常意味着被解析的源代码中出现了强制类型转换，
        而调用 parse 便是解析强制类型转换所包含的复杂表达式。
        换句话说，parse 被用于解析强制类型转换中，被括号所包围的表达式。

        因此，parse 只是将解析所得到的复杂表达式置于该字面量表达式元素
        的负载中，而并不会改变它的元素 ID。表达式元素 ID 在此上下文中，
        用于告知运行时，应该将复杂表达式的求值结果强制转换为哪个类型

        Args:
            reader (SentenceReader): 底层 Token 流
            layer (int, optional):
                当前解析的层数。
                应只在处理括号时自增。
                默认值为 0

        Raises:
            Exception: 当解析出现错误时抛出

        Returns:
            ExpressionLiteral: 返回 ExpressionLiteral 本身
        """
        from .combine import ExpressionCombine

        token = reader.must_read()
        if token.token_id != TOKEN_ID_LEFT_BRACKET:
            raise Exception('parse: Syntax error; expected="(", token={}'.format(token))

        val = ExpressionCombine().parse(reader, layer + 1, CONTEXT_PARSE_SUB_EXPR)
        sub = reader.unread().must_read()
        if sub.token_id != TOKEN_ID_RIGHT_BRACKET:
            raise Exception('parse: Syntax error; expected=")", token={}'.format(token))

        self.element_payload = val
        return self


class ExpressionReference(ExpressionElement):
    """
    ExpressionReference 指示引用表达式元素。
    它的主要目的是引用表单响应中某个元素的结果。

    对于模态表单，它指示引用第 i 个索引上的响应；
    对于长表单，查询用户所点击的按钮的索引；
    对于信息表单，查询用户选择了“确定”还是“取消”。

    作为一种特殊情况，代码可能被用作处理表单被关闭的情况。
    在这种情况下，该表达式元素用于获取表单被关闭的原因

    在最初设计时只考虑了模态表单中，
    针对用户响应的引用，
    所以“引用”因而得名
    """

    element_id = ELEMENT_ID_REF  # type: int
    element_payload = []  # type: list[Any]

    def __init__(self, payload=[]):  # type: (list[Any]) -> None
        """初始化并返回一个新的 ExpressionReference

        Args:
            payload (list[Any], optional):
                该引用表达式元素的负载。
                默认值为空列表
        """
        self.element_id = ELEMENT_ID_REF
        self.element_payload = payload if len(payload) > 0 else []

    def parse(self, reader):  # type: (SentenceReader) -> ExpressionReference
        """
        parse 从底层流解析该引用表达式元素的负载。

        在设计上，我们要求用户断言被引用对象的类型，
        它目前只出于确保用户代码正确性的目的而存在。

        因此，parse 首先读取类型关键字，
        然后再解析一个复杂表达式，
        然后最后再分别追加到底层的负载中。

        复杂表达式的求值结果应只可能是一个整数。
        它可能指示一个索引，或其他具有意义的值，
        这取决于用户代码所处的上下文环境

        Args:
            reader (SentenceReader): 底层 Token 流

        Raises:
            Exception: 当解析出现错误时抛出

        Returns:
            ExpressionReference: 返回 ExpressionReference 本身
        """
        from .combine import ExpressionCombine

        token = reader.must_read()
        if token.token_id != TOKEN_ID_COMMA:
            raise Exception('parse: Syntax error; expected=",", token={}'.format(token))

        token = reader.must_read()
        if token.token_id == TOKEN_ID_KEY_WORD_INT:
            self.element_payload = [TYPE_ENUM_INT]
        elif token.token_id == TOKEN_ID_KEY_WORD_BOOL:
            self.element_payload = [TYPE_ENUM_BOOL]
        elif token.token_id == TOKEN_ID_KEY_WORD_FLOAT:
            self.element_payload = [TYPE_ENUM_FLOAT]
        elif token.token_id == TOKEN_ID_KEY_WORD_STR:
            self.element_payload = [TYPE_ENUM_STR]
        else:
            raise Exception(
                "parse: Syntax error: Type of reference must be int/bool/float/str; token={}".format(
                    token
                )
            )

        token = reader.must_read()
        if token.token_id != TOKEN_ID_COMMA:
            raise Exception('parse: Syntax error; expected=",", token={}'.format(token))
        self.element_payload.append(
            ExpressionCombine().parse(reader, 1, CONTEXT_PARSE_BARRIER)
        )
        _ = reader.unread()

        return self


class ExpressionSelector(ExpressionElement):
    """
    ExpressionSelector 指示目标选择器表达式元素。
    它保存了一个复杂表达式，对该表达式求值可以得到选择器字符串。
    然后，对选择器字符串进行求值，将可以得到相应的实体名
    """

    element_id = ELEMENT_ID_SELECTOR  # type: int
    element_payload = None  # type: ExpressionCombine | None

    def __init__(self, payload=None):  # type: (ExpressionCombine | None) -> None
        """初始化并返回一个新的 ExpressionSelector

        Args:
            payload (ExpressionCombine | None, optional):
                该目标选择器表达式元素的负载。应指向一个复杂表达式，
                并且它的求值结果将作为目标选择器的字符串。
                使用 None 作为参数后，应尽快调用 parse 函数，
                以使得本表达式元素的负载指向切实的复杂表达式。
                默认值为 None
        """
        self.element_id = ELEMENT_ID_SELECTOR
        self.element_payload = payload

    def parse(self, reader):  # type: (SentenceReader) -> ExpressionSelector
        """
        parse 从底层流解析一个复杂表达式。
        该复杂表达式的求值结果将作为目标选择器的字符串。
        对该字符串进行求值后，将可以得到相应的实体名

        Args:
            reader (SentenceReader): 底层 Token 流

        Raises:
            Exception: 当解析出现错误时抛出

        Returns:
            ExpressionSelector: 返回 ExpressionSelector 本身
        """
        from .combine import ExpressionCombine

        token = reader.must_read()
        if token.token_id != TOKEN_ID_COMMA:
            raise Exception('parse: Syntax error; expected=",", token={}'.format(token))

        self.element_payload = ExpressionCombine().parse(
            reader, 1, CONTEXT_PARSE_BARRIER
        )
        _ = reader.unread()

        return self


class ExpressionScore(ExpressionElement):
    """
    ExpressionScore 指示记分板分数表达式元素。
    它保存了两个复杂表达式，求值后可以得到两个字符串，
    分别是指向玩家的目标选择器（或通配符）和记分板名
    """

    element_id = ELEMENT_ID_SCORE  # type: int
    element_payload = []  # type: list[ExpressionCombine]

    def __init__(self, payload=[]):  # type: (list[ExpressionCombine]) -> None
        """初始化并返回一个新的 ExpressionScore

        Args:
            payload (list[ExpressionCombine], optional):
                该记分板分数表达式元素的负载。
                默认值为空列表
        """
        self.element_id = ELEMENT_ID_SCORE
        self.element_payload = payload if len(payload) > 0 else []

    def parse(self, reader):  # type: (SentenceReader) -> ExpressionScore
        """
        parse 从底层流解析该记分板分数表达式元素的负载。

        具体来说，它将依次解析两个复杂表达式，
        并且这两个复杂表达式的求值结果将分别作为
        指向玩家的目标选择器（或通配符）和记分板名

        Args:
            reader (SentenceReader): 底层 Token 流

        Raises:
            Exception: 当解析出现错误时抛出

        Returns:
            ExpressionScore: 返回 ExpressionScore 本身
        """
        from .combine import ExpressionCombine

        self.element_payload = []
        for index in range(2):
            token = reader.must_read()
            if token.token_id != TOKEN_ID_COMMA:
                raise Exception(
                    'parse: Syntax error; expected=",", index={}, token={}'.format(
                        index, token
                    )
                )
            self.element_payload.append(
                ExpressionCombine().parse(reader, 1, CONTEXT_PARSE_BARRIER)
            )
            _ = reader.unread()
        return self


class ExpressionCommand(ExpressionElement):
    """
    ExpressionCommand 指示命令表达式元素。
    它保存了一个复杂表达式，并且它的求值结果将作为命令
    """

    element_id = ELEMENT_ID_COMMAND  # type: int
    element_payload = None  # type: ExpressionCombine | None

    def __init__(self, payload=None):  # type: (ExpressionCombine | None) -> None
        """初始化并返回一个新的 ExpressionCommand

        Args:
            payload (ExpressionCombine | None, optional):
                该命令表达式元素的负载。应指向一个复杂表达式，
                并且它的求值结果将作为命令。
                使用 None 作为参数后，应尽快调用 parse 函数，
                以使得本表达式元素的负载指向切实的复杂表达式。
                默认值为 None
        """
        self.element_id = ELEMENT_ID_COMMAND
        self.element_payload = payload

    def parse(self, reader):  # type: (SentenceReader) -> ExpressionCommand
        """
        parse 从底层流解析一个复杂表达式。
        该复杂表达式的求值结果将作为命令

        Args:
            reader (SentenceReader): 底层 Token 流

        Raises:
            Exception: 当解析出现错误时抛出

        Returns:
            ExpressionCommand: 返回 ExpressionCommand 本身
        """
        from .combine import ExpressionCombine

        token = reader.must_read()
        if token.token_id != TOKEN_ID_COMMA:
            raise Exception('parse: Syntax error; expected=",", token={}'.format(token))

        self.element_payload = ExpressionCombine().parse(
            reader, 1, CONTEXT_PARSE_BARRIER
        )
        _ = reader.unread()

        return self


class ExpressionFunction(ExpressionElement):
    """
    ExpressionFunction 指示函数表达式元素。
    它保存了函数名和参数列表，用于函数调用
    """

    element_id = ELEMENT_ID_FUNC  # type: int
    element_payload = []  # type: list[Any]

    def __init__(self, element_payload=[]):  # type: (list[Any]) -> None
        """初始化并返回一个新的 ExpressionFunction

        Args:
            element_payload (list[Any], optional):
                该函数表达式元素的负载。
                默认值为空列表
        """
        self.element_id = ELEMENT_ID_FUNC
        self.element_payload = element_payload if len(element_payload) > 0 else []

    def parse(self, reader):  # type: (SentenceReader) -> ExpressionFunction
        """
        parse 从底层流解析被调用函数的函数名，
        以及所有需要传入给该函数的参数。

        实际上，解析得到的参数列表是由多个复杂表达式组成的列表。
        因此，该函数表达式元素的负载具有两个元素，
        而第一个元素即为函数名，第二个元素便是参数列表

        Args:
            reader (SentenceReader): 底层 Token 流

        Raises:
            Exception: 当解析出现错误时抛出

        Returns:
            ExpressionFunction: 返回 ExpressionFunction 本身
        """
        from .combine import ExpressionCombine

        self.element_payload = []  # type: list[Any]
        arguments = []  # type: list[ExpressionCombine]

        token = reader.must_read()
        if token.token_id != TOKEN_ID_COMMA:
            raise Exception('parse: Syntax error; expected=",", token={}'.format(token))

        token = reader.must_read()
        if token.token_id == TOKEN_ID_KEY_WORD_INT:
            self.element_payload.append("int")
        elif token.token_id == TOKEN_ID_KEY_WORD_BOOL:
            self.element_payload.append("bool")
        elif token.token_id == TOKEN_ID_KEY_WORD_FLOAT:
            self.element_payload.append("float")
        elif token.token_id == TOKEN_ID_KEY_WORD_STR:
            self.element_payload.append("str")
        elif token.token_id == TOKEN_ID_WORD:
            self.element_payload.append(token.token_payload)
        else:
            raise Exception(
                "parse: Syntax error: Invalid function name; token={}".format(token)
            )

        token = reader.must_read()
        if token.token_id != TOKEN_ID_LEFT_BRACKET:
            raise Exception('parse: Syntax error; expected="(", token={}'.format(token))

        token = reader.must_read()
        if token.token_id != TOKEN_ID_RIGHT_BRACKET:
            _ = reader.unread()
            while True:
                arguments.append(
                    ExpressionCombine().parse(reader, 1, CONTEXT_PARSE_ARGUMENT)
                )
                if reader.unread().must_read().token_id == TOKEN_ID_RIGHT_BRACKET:
                    break

        self.element_payload.append(arguments)
        return self
