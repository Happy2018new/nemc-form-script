# -*- coding: utf-8 -*-

from .define import (
    ConditionCodeBlock,
    ForLoopCodeBlock,
    OpcodeBase,
    OpcodeAssign,
    OpcodeCondition,
    OpcodeForLoop,
    OpcodeContinue,
    OpcodeBreak,
    OpcodeExpression,
    OpcodeReturn,
)
from ..expression.combine import ExpressionCombine
from ..expression.define import (
    CONTEXT_PARSE_ASSIGN,
    CONTEXT_PARSE_IF,
    CONTEXT_PARSE_FOR,
)
from ..reader.string_reader import StringReader
from ..token.sentence import Sentence, SentenceReader
from ..token.token import (
    Token,
    TOKEN_ID_WORD,
    TOKEN_ID_ASSIGN,
    TOKEN_ID_COLON,
    TOKEN_ID_COMMA,
    TOKEN_ID_SEPSEPARATE,
    TOKEN_ID_KEY_WORD_RETURN,
    TOKEN_ID_KEY_WORD_IF,
    TOKEN_ID_KEY_WORD_ELSE,
    TOKEN_ID_KEY_WORD_ELIF,
    TOKEN_ID_KEY_WORD_FI,
    TOKEN_ID_KEY_WORD_FOR,
    TOKEN_ID_KEY_WORD_CONTINUE,
    TOKEN_ID_KEY_WORD_BREAK,
    TOKEN_ID_KEY_WORD_ROF,
)

try:
    range = xrange  # type: ignore
except Exception:
    pass

ORD_ZERO, ORD_NINE = ord("0"), ord("9")
DEFAULT_EMPTY_EXCEPTION = Exception()


class CodeParser:
    """
    CodeParser 是源代码解析器。
    它用于解析并编译给定的源代码，
    将源代码处理为抽象语法树表示
    """

    code = ""  # type: str
    reader = SentenceReader()  # type: SentenceReader
    code_block = []  # type: list[OpcodeBase]

    def __init__(self, code=""):  # type: (str) -> None
        """初始化并返回一个新的 CodeParser

        Args:
            code (str, optional):
                给定的源代码。
                默认值为空字符串

        Raises:
            Exception:
                如果源代码在初始化阶段（分词阶段）出现错误，
                则抛出相应的错误
        """
        self.code = code + "\n"
        sentence = Sentence(StringReader(self.code))

        ptr1, ptr2, err = sentence.parse_all()
        if err is not None:
            self._fast_normal_panic(ptr1, ptr2, str(err))
            raise Exception("unreachable")

        self.reader = SentenceReader(sentence.tokens)
        self.code_block = []

    def _format_problem_normal(self, ptr1, ptr2):  # type: (int, int) -> str
        """
        _format_problem_normal 突出 self.code[ptr1:ptr2] 处的源代码，
        并同时展示其附近的源代码，以便于调试和定位问题

        Args:
            ptr1 (int): 源代码被突出的起始位置
            ptr2 (int): 源代码被突出的结束位置

        Returns:
            str:
                返回 self.code[ptr1:ptr2] 及其附近的源代码，
                其中特别突出了 ptr1 到 ptr2 中的部分，用于调试和定位问题
        """
        code = ""
        left_overflow = False
        right_overflow = False
        if True:
            # Part that before the problem
            if ptr1 - 30 > 0:
                code += "...\n"
                code += self.code[ptr1 - 30 : ptr1]
                left_overflow = True
            else:
                code += self.code[:ptr1]
            # Problem part
            code += ">>"
            code += self.code[ptr1:ptr2]
            code += "<<"
            # Part that after the problem
            if ptr2 + 30 < len(self.code):
                code += self.code[ptr2 : ptr2 + 30]
                code += "\n..."
                right_overflow = True
            else:
                code += self.code[ptr2:]

        blocks = code.split("\n")
        states = [True] * len(blocks)
        start, end = 0, len(blocks) - 1
        if left_overflow and blocks[0] == "...":
            start += 1
        if right_overflow and blocks[-1] == "...":
            end -= 1
        for i in range(start, end + 1):
            if blocks[i].strip() == "":
                states[i] = False
            else:
                break
        for i in range(end, start - 1, -1):
            if blocks[i].strip() == "":
                states[i] = False
            else:
                break

        prefix = ["  " + value for index, value in enumerate(blocks) if states[index]]
        return "\n".join(prefix).rstrip()

    def _format_problem_sentence(self, ptr1, ptr2):  # type: (int, int) -> str
        """
        _format_problem_sentence 突出下方范围内的源代码，并同时展示其附近的源代码。
        ```
            part_a = self.contents[ptr1].ori_start_ptr
            part_b = self.contents[ptr2-1].ori_end_ptr
            return self.code[part_a:part_b]
        ```

        确保 ptr1 和 ptr2 取何值，此函数都可以正常工作。
        这意味着即便 ptr1 或 ptr2 超出范围，或它们相等，此函数都不会抛出错误
        Args:
            ptr1 (int): 需要被突出的 self.contents 的起始位置
            ptr2 (int): 需要被突出的 self.contents 的结束位置

        Returns:
            str:
                返回被突出的源代码段及其附近的源代码，
                用于调试和定位问题
        """
        contents = self.reader.contents()

        ptr1 = min(max(0, ptr1), len(contents) - 1)
        ptr2 = min(max(0, ptr2), len(contents) - 1)
        if ptr1 == ptr2:
            ptr2 += 1

        return self._format_problem_normal(
            contents[ptr1].ori_start_ptr, contents[ptr2 - 1].ori_end_ptr
        )

    def _fast_normal_panic(self, ptr1, ptr2, err):  # type: (int, int, str) -> None
        """
        _fast_normal_panic 抛出 err 所指示的语法错误，
        并在抛出的错误中展示 self.code[ptr1:ptr2] 及其附近的源代码

        Args:
            ptr1 (int): 出现问题的源代码的起始位置
            ptr2 (int): 出现问题的源代码的结束位置
            err (str): 这段源代码出现的问题

        Raises:
            Exception: err 所指示的错误
        """
        raise Exception(
            "Syntax Error.\n\n- Error -\n  {}\n\n- Code -\n{}".format(
                err, self._format_problem_normal(ptr1, ptr2)
            )
        )

    def _fast_sentence_panic(self, ptr1, ptr2, err):  # type: (int, int, str) -> None
        """
        _fast_sentence_panic 抛出 err 所指示的语法错误，
        并在抛出的错误中展示对应源代码段及其附近的源代码。

        具体来说，它会突出显示下方的源代码，并同时展示其附近的源代码。
        这么做的目的是为了便于调试和定位问题。
        ```
            part_a = self.contents[ptr1].ori_start_ptr
            part_b = self.contents[ptr2-1].ori_end_ptr
            return self.code[part_a:part_b]
        ```

        Args:
            ptr1 (int): 需要被突出的 self.contents 的起始位置
            ptr2 (int): 需要被突出的 self.contents 的结束位置
            err (str): 相应源代码段出现的问题

        Raises:
            Exception: err 所指示的错误
        """
        raise Exception(
            "Syntax Error.\n\n- Error -\n  {}\n\n- Code -\n{}".format(
                err, self._format_problem_sentence(ptr1, ptr2)
            )
        )

    def _get_line_code(self, ptr1, ptr2):  # type: (int, int) -> str
        """
        _get_line_code 截取下方范围内的源代码段，
        并同时去除尾随的行分隔符“|”以及多余的空白字符
        ```
            part_a = self.contents[ptr1].ori_start_ptr
            part_b = self.contents[ptr2-1].ori_end_ptr
            return self.code[part_a:part_b]
        ```

        Args:
            ptr1 (int): 被截取的 self.contents 的起始位置
            ptr2 (int): 被截取的 self.contents 的结束位置

        Returns:
            str: 截取到的源代码段
        """
        contents = self.reader.contents()
        ptr1 = min(max(0, ptr1), len(contents) - 1)
        ptr2 = min(max(0, ptr2), len(contents) - 1)
        if ptr1 == ptr2:
            ptr2 += 1

        ptr1 = contents[ptr1].ori_start_ptr
        ptr2 = contents[ptr2 - 1].ori_end_ptr
        code = self.code[ptr1:ptr2]

        while code.endswith("|"):
            code = code[:-1]
        return code.strip()

    def _validate_next_token(self, ptr, token_id, err):  # type: (int, int, str) -> None
        """
        _validate_next_token 从底层流阅读一个 Token，
        并检查它的 ID 是否是 token_id

        Args:
            ptr (int):
                在检查失败时，也即需要抛出错误时，
                用于突出问题源代码的起始位置
            token_id (int):
                预期的 Token 的 ID
            err (str):
                如果阅读到的 Token 的 ID 不是 token_id，
                则应该抛出的错误信息

        Raises:
            Exception:
                如果 _validate_next_token 失败，
                则抛出 err 所指示的错误
        """
        token = self.reader.read()
        if token is None or token.token_id != token_id:
            self._fast_sentence_panic(ptr, self.reader.pointer(), err)
            raise Exception("unreachable")

    def _validate_var_name(self, token, ptr1, ptr2):  # type: (Token, int, int) -> None
        """
        _validate_var_name 检查给定的 Token 的负载是否可以作为合法的变量名

        Args:
            token (Token):
                欲被检查的 Token
            ptr1 (int):
                在检查失败时，也即需要抛出错误时，
                用于突出问题源代码的起始位置
            ptr2 (int):
                在检查失败时，也即需要抛出错误时，
                用于突出问题源代码的终止位置

        Raises:
            Exception:
                当检查失时应抛出的错误
        """
        if "'" in token.token_payload or '"' in token.token_payload:
            self._fast_sentence_panic(
                ptr1, ptr2, "Variable name should not contain quotes"
            )
            raise Exception("unreachable")
        if "." in token.token_payload:
            self._fast_sentence_panic(
                ptr1, ptr2, "Variable name should not contain dots"
            )
            raise Exception("unreachable")
        if ORD_ZERO <= ord(token.token_payload[0]) <= ORD_NINE:
            self._fast_sentence_panic(
                ptr1,
                ptr2,
                "Variable name should not start with number ({})".format(
                    token.token_payload[0]
                ),
            )
            raise Exception("unreachable")

    def _validate_next_line(self, ptr, unread=False):  # type: (int, bool) -> None
        """
        _validate_next_line 从底层流阅读一个 Token，并检查它是否是行分隔符。
        _validate_next_line 的目的是为了确保每条语句都写单独的行上

        Args:
            ptr (int):
                在检查失败时，也即需要抛出错误时，
                用于突出问题源代码的起始位置
            unread (bool, optional):
                如果检查通过，
                那么是否需要撤销对该行分隔符的阅读

        Raises:
            Exception:
                当检查失时应抛出的错误
        """
        token = self.reader.read()
        if token is None:
            return
        if token.token_id != TOKEN_ID_SEPSEPARATE:
            self._fast_sentence_panic(
                ptr,
                self.reader.pointer(),
                'You must write statements line by line or use "|" to represent a new line',
            )
            raise Exception("unreachable")
        if unread:
            self.reader.unread()

    def _parse_variable(self, ptr):  # type: (int) -> str
        """
        _parse_variable 从底层流阅读一个 Token，
        并检查该 Token 是否可以作为合法的变量名。
        如果它可以作为合法的变量名，则返回该变量名

        Args:
            ptr (int):
                当需要抛出错误时，
                用于突出问题源代码的起始位置

        Raises:
            Exception:
                当目标 Token 不能作为合法的变量名时，
                应抛出的错误

        Returns:
            str:
                返回读取到的变量名
        """
        token = self.reader.read()
        if token is None:
            self._fast_sentence_panic(
                ptr, self.reader.pointer(), "Unexpected EOF when reading variable name"
            )
            raise Exception("unreachable")
        if token.token_id != TOKEN_ID_WORD:
            self._fast_sentence_panic(
                ptr,
                self.reader.pointer(),
                "Expected a variable name but got {}".format(token),
            )
            raise Exception("unreachable")
        self._validate_var_name(token, ptr, self.reader.pointer())
        return token.token_payload

    def _parse_expression(
        self, context=CONTEXT_PARSE_ASSIGN, panic=True, unread=False
    ):  # type: (int, bool, bool) -> ExpressionCombine
        """_parse_expression 从底层流解析一个复杂表达式

        Args:
            context (int, optional):
                指示解析该复杂表达式所用的上下文，是一个比特掩码。
                在不同的上下文环境中，复杂表达式中允许出现的字符是不同的。
                默认值为 CONTEXT_PARSE_ASSIGN
            panic (bool, optional):
                是否在解析失败时格式化错误。
                如果不格式化，则按原样抛出错误。
                默认值为 True
            unread (bool, optional):
                是否在解析成功后，
                撤销对复杂表达式最后一个字符（终止符）的读取。
                默认值为 False

        Raises:
            Exception:
                当解析复杂表达式出现错误时抛出

        Returns:
            ExpressionCombine:
                解析所得的复杂表达式
        """
        ptr = self.reader.pointer()
        try:
            expression = ExpressionCombine().parse(self.reader, 0, context)
            if unread:
                self.reader.unread()
        except Exception as e:
            if panic:
                self._fast_sentence_panic(ptr, self.reader.pointer(), str(e))
                raise Exception("unreachable")
            else:
                raise e
        return expression

    def _parse_assign(self, ptr, token):  # type: (int, Token) -> OpcodeAssign
        """_parse_assign 从底层流解析一个赋值操作

        Args:
            ptr (int):
                当需要抛出错误时，
                用于突出问题源代码的起始位置
            token (Token):
                该赋值操作的左侧 Token。
                该 Token 应指向一个变量名

        Returns:
            OpcodeAssign:
                解析所得的赋值操作
        """
        self._validate_var_name(token, ptr, self.reader.pointer())
        self._validate_next_token(
            self.reader.pointer(),
            TOKEN_ID_ASSIGN,
            'Assign statement should use "=" after variable name',
        )
        return OpcodeAssign(
            (
                token.token_payload,
                self._parse_expression(CONTEXT_PARSE_ASSIGN, True, True),
            ),
            self._get_line_code(ptr, self.reader.pointer()),
        )

    def _parse_return(self, ptr):  # type: (int) -> OpcodeReturn
        """_parse_return 从底层流解析一个返回语句

        Args:
            ptr (int):
                当需要抛出错误时，
                用于突出问题源代码的起始位置

        Returns:
            OpcodeReturn:
                解析所得的返回语句
        """
        return OpcodeReturn(
            self._parse_expression(CONTEXT_PARSE_ASSIGN, True, True),
            self._get_line_code(ptr, self.reader.pointer()),
        )

    def _parse_code(
        self, ptr
    ):  # type: (int) -> tuple[OpcodeBase | None, tuple[Token, int, int, Exception] | None]
        """
        _parse_code 从底层流阅读一个单行代码，
        并试图返回该行代码对应的操作语句。

        _parse_code 将返回一个元组。
        通常情况下，元组的第一个元素即为解析所得的操作语句。
        并且，在这一情况下，元组的第二个元素为 None。

        如果底层流已经被耗尽，
        则返回的元组的第一个元素和第二个元素均为 None。

        否则，若仍未出现错误，则元组的第一个元素应是 None，
        且返回的元组的第二个元素的第一个元素 T 应具有值。

        T 是一个 Token，它用于 _parse_code 的调用者
        在后续处理特定于上下文的语句，例如下方列出的特殊关键字。
        ```
            elif, else, fi, rof, ...
        ```

        如果 _parse_code 的调用者处理失败，
        则 _parse_code 返回的元组可另用作下面的用途。
        ```
            self._fast_sentence_panic(S1, S2, S3)
        ```
        其中，S1、S2 和 S3 是元组第二个元素的后三个元素

        Args:
            ptr (int):
                当需要抛出错误时，
                用于突出问题源代码的起始位置

        Returns:
            tuple[OpcodeBase | None, tuple[Token, int, int, Exception] | None]:
                相应的元组
        """
        expr_start_ptr = self.reader.pointer()
        expr_end_ptr = expr_start_ptr
        expr_parse_err = DEFAULT_EMPTY_EXCEPTION
        try:
            return (
                OpcodeExpression(
                    self._parse_expression(CONTEXT_PARSE_ASSIGN, False, True),
                    self._get_line_code(expr_start_ptr, self.reader.pointer()),
                ),
                None,
            )
        except Exception as e:
            expr_end_ptr, expr_parse_err = self.reader.pointer(), e
            self.reader.set_pointer(expr_start_ptr)

        ptr = self.reader.pointer()
        token = self.reader.read()
        if token is None:
            return None, None

        if token.token_id == TOKEN_ID_WORD:
            return self._parse_assign(ptr, token), None
        if token.token_id == TOKEN_ID_KEY_WORD_IF:
            return self._parse_condition(ptr), None
        if token.token_id == TOKEN_ID_KEY_WORD_FOR:
            return self._parse_for_loop(ptr), None
        if token.token_id == TOKEN_ID_KEY_WORD_RETURN:
            return self._parse_return(ptr), None
        if token.token_id == TOKEN_ID_KEY_WORD_CONTINUE:
            code = self._get_line_code(ptr, self.reader.pointer())
            return OpcodeContinue(code), None
        if token.token_id == TOKEN_ID_KEY_WORD_BREAK:
            code = self._get_line_code(ptr, self.reader.pointer())
            return OpcodeBreak(code), None

        return None, (token, expr_start_ptr, expr_end_ptr, expr_parse_err)

    def _parse_condition(self, ptr):  # type: (int) -> OpcodeCondition
        """
        _parse_condition 从底层流解析一个条件代码块。

        下面是一个条件代码块的示例。
        ```
            if x > 0:
                ...
            elif x < 0:
                ...
            else:
                ...
            fi
        ```

        Args:
            ptr (int):
                当需要抛出错误时，
                用于突出问题源代码的起始位置

        Raises:
            Exception:
                当解析出现错误时抛出

        Returns:
            OpcodeCondition:
                解析所得的条件代码块
        """
        conditions = [
            ConditionCodeBlock(
                self._parse_expression(CONTEXT_PARSE_IF, True, False),
                self._get_line_code(ptr, self.reader.pointer()),
                [],
            )
        ]
        self._validate_next_line(ptr, False)

        while True:
            sub_ptr = self.reader.pointer()
            opcode, further = self._parse_code(sub_ptr)

            if opcode is not None:
                conditions[-1].code_block.append(opcode)
                self._validate_next_line(sub_ptr, False)
                continue
            if further is None:
                self._fast_sentence_panic(
                    sub_ptr, self.reader.pointer(), 'If statement not closed with "fi"'
                )
                raise Exception("unreachable")

            if further[0].token_id == TOKEN_ID_KEY_WORD_ELIF:
                conditions.append(
                    ConditionCodeBlock(
                        self._parse_expression(CONTEXT_PARSE_IF, True, False),
                        self._get_line_code(sub_ptr, self.reader.pointer()),
                        [],
                    )
                )
            elif further[0].token_id == TOKEN_ID_KEY_WORD_ELSE:
                self._validate_next_token(
                    self.reader.pointer(),
                    TOKEN_ID_COLON,
                    'Else statement should use ":" after the expression',
                )
                conditions.append(
                    ConditionCodeBlock(
                        None, self._get_line_code(sub_ptr, self.reader.pointer()), []
                    )
                )
            elif further[0].token_id == TOKEN_ID_KEY_WORD_FI:
                self._validate_next_line(sub_ptr, True)
                break
            elif further[0].token_id == TOKEN_ID_SEPSEPARATE:
                continue
            else:
                self._fast_sentence_panic(further[1], further[2], str(further[3]))
                raise Exception("unreachable")

            self._validate_next_line(sub_ptr, False)

        return OpcodeCondition(conditions)

    def _parse_for_loop(self, ptr):  # type: (int) -> OpcodeForLoop
        """
        _parse_for_loop 从底层流解析一个循环代码块。

        下面是一个循环代码块的示例。
        ```
            for i, 2*4+2:
                ...
                continue
                ...
                break
                ...
            rof
        ```

        Args:
            ptr (int):
                当需要抛出错误时，
                用于突出问题源代码的起始位置

        Raises:
            Exception:
                当解析出现错误时抛出

        Returns:
            OpcodeForLoop:
                解析所得的循环代码块
        """
        variable = self._parse_variable(ptr)
        self._validate_next_token(
            self.reader.pointer(),
            TOKEN_ID_COMMA,
            'For loop should use "," before the expression',
        )

        repeat_times = self._parse_expression(CONTEXT_PARSE_FOR, True, False)
        end_expr_ptr = self.reader.pointer()
        self._validate_next_line(ptr, False)

        code_block = []  # type: list[OpcodeBase]
        while True:
            sub_ptr = self.reader.pointer()
            opcode, further = self._parse_code(sub_ptr)

            if opcode is not None:
                code_block.append(opcode)
                self._validate_next_line(sub_ptr, False)
                continue
            if further is None:
                self._fast_sentence_panic(
                    sub_ptr, self.reader.pointer(), 'For loop not closed with "rof"'
                )
                raise Exception("unreachable")

            if further[0].token_id == TOKEN_ID_KEY_WORD_ROF:
                self._validate_next_line(sub_ptr, True)
                break
            elif further[0].token_id == TOKEN_ID_SEPSEPARATE:
                continue
            else:
                self._fast_sentence_panic(further[1], further[2], str(further[3]))
                raise Exception("unreachable")

        return OpcodeForLoop(
            ForLoopCodeBlock(
                variable,
                repeat_times,
                self._get_line_code(ptr, end_expr_ptr),
                code_block,
            )
        )

    def parse(self):  # type: () -> CodeParser
        """
        parse 解析底层流中的所有字符，
        并将其编译为抽象语法树表示。

        如果解析没有出现错误，则底层流最终应会被耗尽。
        并且，解析结果将被置于本实例的 code_block 中

        Raises:
            Exception:
                当解析出现错误时抛出

        Returns:
            CodeParser:
                返回 CodeParser 本身
        """
        while True:
            ptr = self.reader.pointer()
            opcode, further = self._parse_code(ptr)

            if opcode is not None:
                self.code_block.append(opcode)
                self._validate_next_line(ptr, False)
                continue
            if further is None:
                break
            if further[0].token_id == TOKEN_ID_SEPSEPARATE:
                continue

            self._fast_sentence_panic(further[1], further[2], str(further[3]))
            raise Exception("unreachable")

        return self
