# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from .define import (
    ExpressionElement,
    CONTEXT_PARSE_ASSIGN,
    CONTEXT_PARSE_IF,
    CONTEXT_PARSE_FOR,
    CONTEXT_PARSE_ARGUMENT,
    CONTEXT_PARSE_SUB_EXPR,
    CONTEXT_PARSE_BARRIER,
    ELEMENT_ID_VAR,
    ELEMENT_ID_EXPR,
    ELEMENT_ID_EQUAL,
    ELEMENT_ID_LESS_THAN,
    ELEMENT_ID_GREATER_THAN,
    ELEMENT_ID_LESS_EQUAL,
    ELEMENT_ID_GREATER_EQUAL,
    ELEMENT_ID_ADD,
    ELEMENT_ID_REMOVE,
    ELEMENT_ID_TIMES,
    ELEMENT_ID_DIVIDE,
    ELEMENT_ID_NOT_EQUAL,
    ELEMENT_ID_INT,
    ELEMENT_ID_BOOL,
    ELEMENT_ID_FLOAT,
    ELEMENT_ID_STR,
    ELEMENT_ID_REF,
    ELEMENT_ID_SELECTOR,
    ELEMENT_ID_SCORE,
    ELEMENT_ID_COMMAND,
    ELEMENT_ID_FUNC,
    ELEMENT_ID_AND,
    ELEMENT_ID_OR,
    ELEMENT_ID_IN,
    ELEMENT_ID_INVERSE,
)
from .basic import (
    ExpressionNormal,
    ExpressionLiteral,
    ExpressionReference,
    ExpressionSelector,
    ExpressionScore,
    ExpressionCommand,
    ExpressionFunction,
)
from .compute import (
    ExpressionTimes,
    ExpressionDivide,
    ExpressionAdd,
    ExpressionRemove,
)
from .compare import (
    ExpressionOperator,
    ExpressionGreaterThan,
    ExpressionLessThan,
    ExpressionGreaterEqual,
    ExpressionLessEqual,
    ExpressionEqual,
    ExpressionNotEqual,
    ExpressionAnd,
    ExpressionOr,
    ExpressionIn,
    ExpressionInverse,
)
from ..reader.any_reader import AnyReader
from ..token.sentence import SentenceReader
from ..token.token import (
    Token,
    TOKEN_ID_WORD,
    TOKEN_ID_ASSIGN,
    TOKEN_ID_LEFT_ANGLE_BRACKET,
    TOKEN_ID_RIGHT_ANGLE_BRACKET,
    TOKEN_ID_LEFT_BARRIER,
    TOKEN_ID_RIGHT_BARRIER,
    TOKEN_ID_COLON,
    TOKEN_ID_PLUS,
    TOKEN_ID_MINUS,
    TOKEN_ID_ASTERISK,
    TOKEN_ID_SLASH,
    TOKEN_ID_SINGLE_QUOTE,
    TOKEN_ID_LEFT_BRACKET,
    TOKEN_ID_RIGHT_BRACKET,
    TOKEN_ID_COMMA,
    TOKEN_ID_EXCLAMATION,
    TOKEN_ID_SEPSEPARATE,
    TOKEN_ID_KEY_WORD_INT,
    TOKEN_ID_KEY_WORD_BOOL,
    TOKEN_ID_KEY_WORD_STR,
    TOKEN_ID_KEY_WORD_FLOAT,
    TOKEN_ID_KEY_WORD_REF,
    TOKEN_ID_KEY_WORD_SELECTOR,
    TOKEN_ID_KEY_WORD_SCORE,
    TOKEN_ID_KEY_WORD_COMMAND,
    TOKEN_ID_KEY_WORD_FUNC,
    TOKEN_ID_KEY_WORD_RETURN,
    TOKEN_ID_KEY_WORD_IF,
    TOKEN_ID_KEY_WORD_ELSE,
    TOKEN_ID_KEY_WORD_ELIF,
    TOKEN_ID_KEY_WORD_FI,
    TOKEN_ID_KEY_WORD_FOR,
    TOKEN_ID_KEY_WORD_CONTINUE,
    TOKEN_ID_KEY_WORD_BREAK,
    TOKEN_ID_KEY_WORD_ROF,
    TOKEN_ID_KEY_WORD_AND,
    TOKEN_ID_KEY_WORD_OR,
    TOKEN_ID_KEY_WORD_NOT,
    TOKEN_ID_KEY_WORD_IN,
    TOKEN_ID_KEY_WORD_TRUE,
    TOKEN_ID_KEY_WORD_FALSE,
)

ORD_ZERO = ord("0")
ORD_NINE = ord("9")


class ExpressionCombine(ExpressionElement):
    """
    ExpressionCombine 指示复杂表达式。

    如果解析无误，element_payload 的长度为 1，
    但其内部可能嵌套多个表达式元素，这其中也可能
    包含 ExpressionCombine 类。

    无论内部结构如何，对 ExpressionCombine 的求值
    将得到单一值，并且从形式上，多个值是不被允许的
    """

    element_id = ELEMENT_ID_EXPR  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, payload=[]):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionCombine

        Args:
            payload (list[ExpressionElement], optional):
                多个表达式元素组成的列表。
                默认值为空列表
        """
        self.element_id = ELEMENT_ID_EXPR
        self.element_payload = payload if len(payload) > 0 else []

    def try_parse_float(self, token):  # type: (Token) -> bool
        """
        try_parse_float 试图将 token 解析为浮点数，
        然后将解析结果追加到底层的 element_payload

        Args:
            token (Token): 欲被解析的 Token

        Returns:
            bool: 如果解析成功，则返回真；
                  否则解析失败，那么返回假
        """
        if token.token_id != TOKEN_ID_WORD:
            return False
        if "." not in token.token_payload:
            return False
        number = float(token.token_payload)
        self.element_payload.append(ExpressionLiteral(ELEMENT_ID_FLOAT, number))
        return True

    def try_parse_int(self, token):  # type: (Token) -> bool
        """
        try_parse_int 试图将 token 解析为整数，
        然后将解析结果追加到底层的 element_payload

        Args:
            token (Token): 欲被解析的 Token

        Returns:
            bool: 如果解析成功，则返回真；
                  否则解析失败，那么返回假
        """
        if token.token_id != TOKEN_ID_WORD:
            return False
        try:
            number = int(token.token_payload)
            self.element_payload.append(ExpressionLiteral(ELEMENT_ID_INT, number))
            return True
        except Exception:
            return False

    def try_parse_var(self, token):  # type: (Token) -> bool
        """
        try_parse_var 试图从 token 解析一个变量名，
        然后将解析结果追加到底层的 element_payload

        Args:
            token (Token): 欲被解析的 Token

        Raises:
            Exception:
                如果变量名包含引号，
                或变量名以数字开头，
                则抛出变量名不符合规范的错误

        Returns:
            bool: 如果解析成功，则返回真；
                  否则解析失败，那么返回假
        """
        if token.token_id != TOKEN_ID_WORD:
            return False

        if "'" in token.token_payload or '"' in token.token_payload:
            raise Exception(
                "try_parse_var: Syntax error: Variable name should not contain quotes; token.token_payload={}".format(
                    json.dumps(token.token_payload, ensure_ascii=False)
                )
            )
        if ORD_ZERO <= ord(token.token_payload[0]) <= ORD_NINE:
            raise Exception(
                "try_parse_var: Syntax error: Variable name should not start with number ({}); token.token_payload={}".format(
                    token.token_payload[0],
                    json.dumps(token.token_payload, ensure_ascii=False),
                )
            )

        self.element_payload.append(
            ExpressionLiteral(ELEMENT_ID_VAR, token.token_payload)
        )
        return True

    def try_parse_equal(self, token, sub):  # type: (Token, Token) -> None
        """
        try_parse_equal 检查 token 和 sub 是否构成相等运算符。
        如果构成，则向底层的 element_payload 追加一个相等运算符

        Args:
            token (Token):
                相等运算符的第一个字符。
                应只可能是等号
            sub (Token):
                相等运算符的第二个字符。
                应只可能是等号

        Raises:
            Exception:
                如果 token 和 sub 不构成有效的相等运算符，
                则抛出对应的错误
        """
        if token.token_id != TOKEN_ID_ASSIGN:
            raise Exception(
                'try_parse_equal: Syntax error; expected="=", token={}'.format(token)
            )
        if sub.token_id != TOKEN_ID_ASSIGN:
            raise Exception(
                'try_parse_equal: Syntax error; expected="=", sub={}'.format(sub)
            )
        self.element_payload.append(ExpressionNormal(ELEMENT_ID_EQUAL))

    def try_parse_compare(
        self, reader, token, sub
    ):  # type: (SentenceReader, Token, Token) -> None
        """
        try_parse_compare 试图从 token 和 sub 解析比较操作符。
        如果成功，则向底层的 element_payload 追加解析的操作符

        Args:
            reader (SentenceReader):
                底层 Token 的阅读器
            token (Token):
                比较运算中的第一个字符。
                应只可能是 > 或 <
            sub (Token):
                比较运算中的第二个字符。
                它可以是任意符号

        Raises:
            Exception:
                如果 token 和 sub 不构成有效的比较运算符，
                则抛出对应的错误
        """
        if token.token_id == TOKEN_ID_LEFT_ANGLE_BRACKET:
            if sub.token_id == TOKEN_ID_ASSIGN:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_LESS_EQUAL))
            else:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_LESS_THAN))
                _ = reader.unread()
            return

        if token.token_id == TOKEN_ID_RIGHT_ANGLE_BRACKET:
            if sub.token_id == TOKEN_ID_ASSIGN:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_GREATER_EQUAL))
            else:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_GREATER_THAN))
                _ = reader.unread()
            return

        raise Exception(
            "try_parse_compare: Syntax error; token={}, sub={}".format(token, sub)
        )

    def try_parse_barrier(self, reader, token):  # type: (SentenceReader, Token) -> None
        """
        try_parse_barrier 试图根据 reader
        和 token 来解析一个 `{...}` 表达式。

        下面列出了被允许的 `{...}` 表达式。
        ```
            {ref, ... (type), ... (expression)}
            {selector, ... (str)}
            {score, ... (str), ... (str)}
            {command, ... (str)}
            {func, ... (function call)}
        ```

        Args:
            reader (SentenceReader): 底层 Token 的阅读器
            token (Token): 左大括号符号所对应的 Token

        Raises:
            Exception:
                如果 token 及其后续构成的串不是有效的 `{...}` 表达式，
                则抛出对应的错误
        """
        if token.token_id != TOKEN_ID_LEFT_BARRIER:
            raise Exception(
                'try_parse_barrier: Syntax error; expected="{", token={}'.format(token)
            )

        sub = reader.must_read()
        if sub.token_id == TOKEN_ID_KEY_WORD_REF:
            self.element_payload.append(ExpressionReference().parse(reader))
        elif sub.token_id == TOKEN_ID_KEY_WORD_SELECTOR:
            self.element_payload.append(ExpressionSelector().parse(reader))
        elif sub.token_id == TOKEN_ID_KEY_WORD_SCORE:
            self.element_payload.append(ExpressionScore().parse(reader))
        elif sub.token_id == TOKEN_ID_KEY_WORD_COMMAND:
            self.element_payload.append(ExpressionCommand().parse(reader))
        elif sub.token_id == TOKEN_ID_KEY_WORD_FUNC:
            self.element_payload.append(ExpressionFunction().parse(reader))
        else:
            raise Exception(
                "try_parse_barrier: Syntax error: Barrier only accept ref/selector/score/command/func; sub={}".format(
                    sub
                )
            )

        end = reader.must_read()
        if end.token_id != TOKEN_ID_RIGHT_BARRIER:
            raise Exception("try_parse_barrier: Barrier not closed")

    def try_parse_not_equal(self, token, sub):  # type: (Token, Token) -> None
        """
        try_parse_not_equal 检查 token 和 sub 是否构成不等运算符。
        如果构成，则向底层的 element_payload 追加一个不等运算符

        Args:
            token (Token):
                不等运算符的第一个字符。
                应只可能是不等号
            sub (Token):
                不等运算符的第二个字符。
                应只可能是等号

        Raises:
            Exception:
                如果 token 和 sub 不构成有效的不等运算符，
                则抛出对应的错误
        """
        if token.token_id != TOKEN_ID_EXCLAMATION:
            raise Exception(
                'try_parse_equal: Syntax error; expected="!", token={}'.format(token)
            )
        if sub.token_id != TOKEN_ID_ASSIGN:
            raise Exception(
                'try_parse_equal: Syntax error; expected="=", sub={}'.format(sub)
            )
        self.element_payload.append(ExpressionNormal(ELEMENT_ID_NOT_EQUAL))

    def parse_to_elements(
        self, reader, layer=0, context=CONTEXT_PARSE_ASSIGN
    ):  # type: (SentenceReader, int, int) -> None
        """
        parse_to_elements 从 reader 指示的底层流中不断地读取字符，
        直到底层流被耗尽，或读取到相应的终止符。

        如果没有发生错误，从 reader 读取到的所有 Token 将被置入底
        层的 element_payload 中，作为多个表达式元素。

        这意味着 parse_to_elements 的实际作用是将相应的 Token 流
        转换为 ExpressionElement 列表。

        下面列出了所有的终止符。应注意的是，终止符仅终止表达式的读取，
        这意味着 reader 所指示的底层流仍可以被继续使用。
        ```
            '}', ':', ')', ',',
            '\\n', '|'
        ```

        Args:
            reader (SentenceReader):
                底层 Token 流
            layer (int, optional):
                当前解析的层数。
                应只在处理括号时自增。
                默认值为 0
            context (int, optional):
                指示当前解析的上下文，是一个比特掩码。
                在不同的上下文中，所不允许出现的字符是不同的。
                并且，并非任意的终止符都可以在任何情况下使用。
                默认值为 CONTEXT_PARSE_ASSIGN

        Raises:
            Exception:
                如果在解析过程中遭遇错误，
                例如底层流提前耗尽，
                或读取到不符合上下文的符号，
                则抛出相应的错误
        """
        while True:
            token = reader.must_read()
            if token.token_id == TOKEN_ID_WORD:
                if self.try_parse_float(token):
                    continue
                if self.try_parse_int(token):
                    continue
                if self.try_parse_var(token):
                    continue
            if token.token_id == TOKEN_ID_ASSIGN:
                self.try_parse_equal(token, reader.must_read())
                continue
            if token.token_id == TOKEN_ID_LEFT_ANGLE_BRACKET:
                self.try_parse_compare(reader, token, reader.must_read())
                continue
            if token.token_id == TOKEN_ID_RIGHT_ANGLE_BRACKET:
                self.try_parse_compare(reader, token, reader.must_read())
                continue
            if token.token_id == TOKEN_ID_LEFT_BARRIER:
                self.try_parse_barrier(reader, token)
                continue
            if token.token_id == TOKEN_ID_RIGHT_BARRIER:
                if context & CONTEXT_PARSE_BARRIER == 0:
                    raise Exception(
                        'parse_to_elements: Syntax error: "}" can only been used under barrier expression'
                    )
                break
            if token.token_id == TOKEN_ID_COLON:
                if context & CONTEXT_PARSE_IF == 0 and context & CONTEXT_PARSE_FOR == 0:
                    raise Exception(
                        'parse_to_elements: Syntax error: ":" can only been used under if condition or for loop'
                    )
                break
            if token.token_id == TOKEN_ID_PLUS:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_ADD))
                continue
            if token.token_id == TOKEN_ID_MINUS:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_REMOVE))
                continue
            if token.token_id == TOKEN_ID_ASTERISK:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_TIMES))
                continue
            if token.token_id == TOKEN_ID_SLASH:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_DIVIDE))
                continue
            if token.token_id == TOKEN_ID_SINGLE_QUOTE:
                self.element_payload.append(
                    ExpressionLiteral(ELEMENT_ID_STR, token.token_payload)
                )
                continue
            if token.token_id == TOKEN_ID_LEFT_BRACKET:
                self.element_payload.append(
                    ExpressionCombine().parse(reader, layer + 1, CONTEXT_PARSE_SUB_EXPR)
                )
                continue
            if token.token_id == TOKEN_ID_RIGHT_BRACKET:
                if (
                    context & CONTEXT_PARSE_SUB_EXPR == 0
                    and context & CONTEXT_PARSE_ARGUMENT == 0
                ):
                    raise Exception(
                        'parse_to_elements: Syntax error: ")" only accepted under sub-expression or function argument'
                    )
                if layer == 0:
                    raise Exception(
                        "parse_to_elements: Syntax error: Bracket closed incorrectly"
                    )
                break
            if token.token_id == TOKEN_ID_COMMA:
                if (
                    context & CONTEXT_PARSE_ARGUMENT == 0
                    and context & CONTEXT_PARSE_BARRIER == 0
                ):
                    raise Exception(
                        'parse_to_elements: Syntax error: "," only accepted under function argument or barrier expression'
                    )
                break
            if token.token_id == TOKEN_ID_EXCLAMATION:
                self.try_parse_not_equal(token, reader.must_read())
                continue
            if token.token_id == TOKEN_ID_SEPSEPARATE:
                if context & CONTEXT_PARSE_ASSIGN == 0:
                    raise Exception(
                        "parse_to_elements: Syntax error: Incomplete expression in the end of a line"
                    )
                break
            if token.token_id == TOKEN_ID_KEY_WORD_INT:
                self.element_payload.append(
                    ExpressionLiteral(ELEMENT_ID_INT, 0).parse(reader, layer + 1)
                )
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_BOOL:
                self.element_payload.append(
                    ExpressionLiteral(ELEMENT_ID_BOOL, False).parse(reader, layer + 1)
                )
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_STR:
                self.element_payload.append(
                    ExpressionLiteral(ELEMENT_ID_STR, "").parse(reader, layer + 1)
                )
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_FLOAT:
                self.element_payload.append(
                    ExpressionLiteral(ELEMENT_ID_FLOAT, 0.0).parse(reader, layer + 1)
                )
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_REF:
                raise Exception(
                    'parse_to_elements: Syntax error: "ref" should inside in a barrier'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_SELECTOR:
                raise Exception(
                    'parse_to_elements: Syntax error: "selector" should inside in a barrier'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_SCORE:
                raise Exception(
                    'parse_to_elements: Syntax error: "score" should inside in a barrier'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_COMMAND:
                raise Exception(
                    'parse_to_elements: Syntax error: "command" should inside in a barrier'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_FUNC:
                raise Exception(
                    'parse_to_elements: Syntax error: "func" should inside in a barrier'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_RETURN:
                raise Exception(
                    'parse_to_elements: Syntax error: "return" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_IF:
                raise Exception(
                    'parse_to_elements: Syntax error: "if" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_ELSE:
                raise Exception(
                    'parse_to_elements: Syntax error: "else" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_ELIF:
                raise Exception(
                    'parse_to_elements: Syntax error: "elif" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_FI:
                raise Exception(
                    'parse_to_elements: Syntax error: "fi" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_FOR:
                raise Exception(
                    'parse_to_elements: Syntax error: "for" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_CONTINUE:
                raise Exception(
                    'parse_to_elements: Syntax error: "continue" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_BREAK:
                raise Exception(
                    'parse_to_elements: Syntax error: "break" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_ROF:
                raise Exception(
                    'parse_to_elements: Syntax error: "rof" cannot be used in expression'
                )
            if token.token_id == TOKEN_ID_KEY_WORD_AND:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_AND))
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_OR:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_OR))
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_NOT:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_INVERSE))
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_IN:
                self.element_payload.append(ExpressionNormal(ELEMENT_ID_IN))
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_TRUE:
                self.element_payload.append(ExpressionLiteral(ELEMENT_ID_BOOL, True))
                continue
            if token.token_id == TOKEN_ID_KEY_WORD_FALSE:
                self.element_payload.append(ExpressionLiteral(ELEMENT_ID_BOOL, False))
                continue

    def is_variable(self, element):  # type: (ExpressionElement) -> bool
        """
        is_variable 检查 element 是否可以视作变量。
        或者说，element 的求值结果是否是单个值

        Args:
            element (ExpressionElement): 欲被检查的表达式元素

        Returns:
            bool: 被检查的表达式元素是否可以视作变量
        """
        if element.element_id in [
            ELEMENT_ID_VAR,
            ELEMENT_ID_EXPR,
            ELEMENT_ID_INT,
            ELEMENT_ID_BOOL,
            ELEMENT_ID_FLOAT,
            ELEMENT_ID_STR,
            ELEMENT_ID_REF,
            ELEMENT_ID_SELECTOR,
            ELEMENT_ID_SCORE,
            ELEMENT_ID_COMMAND,
            ELEMENT_ID_FUNC,
        ]:
            return True
        if isinstance(element, ExpressionOperator):
            return True
        return False

    def compact_operator(
        self, element_id, element_cls
    ):  # type: (int, type[ExpressionOperator]) -> None
        """
        compact_operator 紧缩 ID 为 element_id 的表达式元素。
        应确保 element_id 所指示的表达式元素是一个运算符。

        记 element_id 指示的运算符为 T。那么具体来说，
        compact_operator 将连续的 T 及其中涉及的变量
        紧缩到 element_cls 所指示的单个表达式元素中。

        下面给出了一些紧缩示例。
        ```
            6*8/2/4*2*3: [6, *, 8, /, 2, /, 4, *, 2, *, 3] => [6, *, Divide(8, 2, 4), *, 2, *, 3]
            4+10-7-3+2+1: [4, +, 10, -, 7, -, 3, +, 2, +, 1] => [4, +, Remove(10, 7, 3), +, 2, +, 1]
        ```

        大多数运算符都可以通过该方式完成紧缩。
        例如上面给出的两个例子的完成形式如下。
        ```
            6*8/2/4*2*3: [Times(6, Divide(8, 2, 4), 2, 3)]
            4+10-7-3+2+1: [Add(4, Remove(10, 7, 3), 2, 1)]
        ```

        Args:
            element_id (int):
                欲被紧缩的运算符所对应的表达式元素 ID
            element_cls (type[ExpressionOperator]):
                在紧缩时所使用的，对应 element_id 的表达式元素类

        Raises:
            Exception: 当紧缩发生错误时抛出
        """
        reader = AnyReader(self.element_payload)  # type: AnyReader
        self.element_payload = []  # type: list[ExpressionElement]

        while True:
            sub_elements = []  # type: list[ExpressionElement]

            element = reader.read()  # type: ExpressionElement | None
            if element is None:
                break
            if element.element_id != element_id:
                self.element_payload.append(element)
                continue
            self.element_payload = self.element_payload[:-1]

            if element_id == ELEMENT_ID_ADD or element_id == ELEMENT_ID_REMOVE:
                if reader.pointer() > 1:
                    operator = (
                        reader.unread().unread().must_read()
                    )  # type: ExpressionElement
                    if not self.is_variable(operator):
                        reader.contents().insert(
                            reader.pointer(), ExpressionLiteral(ELEMENT_ID_INT, 0)
                        )
                        _ = reader.must_read()
                        _ = reader.must_read()
                        self.element_payload.append(operator)
                    else:
                        _ = reader.must_read()
                else:
                    reader.contents().insert(0, ExpressionLiteral(ELEMENT_ID_INT, 0))
                    _ = reader.must_read()

            while True:
                _ = reader.unread().unread()  # type: Any
                var_a = reader.must_read()  # type: ExpressionElement
                _ = reader.must_read()  # type: Any
                var_b = reader.must_read()  # type: ExpressionElement

                if not self.is_variable(var_a):
                    raise Exception(
                        "compact_operator: Syntax error; unexpected={}".format(var_a)
                    )
                if not self.is_variable(var_b):
                    raise Exception(
                        "compact_operator: Syntax error; unexpected={}".format(var_b)
                    )
                if len(sub_elements) == 0:
                    sub_elements.append(var_a)
                sub_elements.append(var_b)

                next_op = reader.read()  # type: ExpressionElement | None
                if next_op is None or next_op.element_id != element_id:
                    if len(sub_elements) > 0:
                        self.element_payload.append(element_cls(sub_elements))
                    if next_op is not None:
                        reader.unread()
                    break

    def compact_inverse(self):  # type: () -> None
        """
        compact_inverse 紧缩取反运算符。

        它将 element_payload 中所有的取反运算符，
        以及其后紧跟的表达式元素紧缩到单个对象中。

        下面给出了一些示例。
        ```
            not a and not b: [not, a, and, not, b] => [Inverse(a), and, Inverse(b)]
            not a * b: [not, a, *, b] => [Inverse(a), *, b]
            a + not b: [a, +, not, b] => [a, +, Inverse(b)]
        ```
        """
        reader = AnyReader(self.element_payload)  # type: AnyReader
        self.element_payload = []  # type: list[ExpressionElement]

        while True:
            element = reader.read()  # type: ExpressionElement | None
            if element is None:
                break
            if element.element_id == ELEMENT_ID_INVERSE:
                self.element_payload.append(ExpressionInverse([reader.must_read()]))
            else:
                self.element_payload.append(element)

    def parse(
        self, reader, layer=0, context=CONTEXT_PARSE_ASSIGN
    ):  # type: (SentenceReader, int, int) -> ExpressionCombine
        """
        parse 从 reader 指示的底层流中解析一个复杂表达式。
        在 parse 返回后，reader 仍可被继续使用，即使耗尽

        Args:
            reader (SentenceReader):
                底层 Token 流
            layer (int, optional):
                当前解析的层数。
                应只在处理括号时自增。
                默认值为 0
            context (int, optional):
                指示当前解析的上下文，是一个比特掩码。
                在不同的上下文中，所不允许出现的字符是不同的。
                并且，并非任意的终止符都可以在任何情况下使用。
                默认值为 CONTEXT_PARSE_ASSIGN

        Raises:
            Exception: 当解析发生错误时抛出

        Returns:
            ExpressionCombine: 对应的复杂表达式
        """
        self.parse_to_elements(reader, layer, context)

        self.compact_operator(ELEMENT_ID_DIVIDE, ExpressionDivide)
        self.compact_operator(ELEMENT_ID_TIMES, ExpressionTimes)
        self.compact_operator(ELEMENT_ID_REMOVE, ExpressionRemove)
        self.compact_operator(ELEMENT_ID_ADD, ExpressionAdd)

        self.compact_operator(ELEMENT_ID_GREATER_THAN, ExpressionGreaterThan)
        self.compact_operator(ELEMENT_ID_LESS_THAN, ExpressionLessThan)
        self.compact_operator(ELEMENT_ID_GREATER_EQUAL, ExpressionGreaterEqual)
        self.compact_operator(ELEMENT_ID_LESS_EQUAL, ExpressionLessEqual)
        self.compact_operator(ELEMENT_ID_EQUAL, ExpressionEqual)
        self.compact_operator(ELEMENT_ID_NOT_EQUAL, ExpressionNotEqual)

        self.compact_operator(ELEMENT_ID_IN, ExpressionIn)
        self.compact_inverse()
        self.compact_operator(ELEMENT_ID_AND, ExpressionAnd)
        self.compact_operator(ELEMENT_ID_OR, ExpressionOr)

        if len(self.element_payload) != 1:
            self.element_payload = []
            raise Exception(
                "parse: Syntax error: Invalid compression (failed to compact the compression)"
            )
        return self
