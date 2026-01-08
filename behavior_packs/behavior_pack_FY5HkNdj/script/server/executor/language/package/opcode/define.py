# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from ..expression.combine import ExpressionCombine

OPCODE_ASSIGN = 0
OPCODE_CONDITION = 1
OPCODE_FOR_LOOP = 2
OPCODE_CONTINUE = 3
OPCODE_BREAK = 4
OPCODE_EXPRESSION = 5
OPCODE_RETURN = 6

OPCODE_ID_TO_NAME = {
    OPCODE_ASSIGN: "assign",
    OPCODE_CONDITION: "if-condition",
    OPCODE_FOR_LOOP: "for-loop",
    OPCODE_CONTINUE: "continue",
    OPCODE_BREAK: "break",
    OPCODE_EXPRESSION: "expression",
    OPCODE_RETURN: "return",
}

DEFAULT_EMPTY_EXPRESSION = ExpressionCombine()


class ConditionCodeBlock:
    """
    ConditionCodeBlock 指示条件代码块。

    它包含了一个条件判断和一个代码块。
    一个代码块中可以包含多个待执行的操作。

    通常来说，只要条件判断为真，
    那么它旗下的代码块就会被执行。

    我们将条件判断和它旗下的代
    码块的组合称为“条件代码块”
    """

    condition = None  # type: ExpressionCombine | None
    state_line = ""  # type: str
    code_block = []  # type: list[OpcodeBase]

    def __init__(
        self, condition, state_line, code_block=[]
    ):  # type: (ExpressionCombine | None, str, list[OpcodeBase]) -> None
        """初始化并返回一个新的条件代码块

        Args:
            condition (ExpressionCombine | None):
                要执行该条件代码块所需要的条件。
                如果为 None，则表示无条件执行
            state_line (str):
                表示条件的源代码行，
                目前只用于调试和错误提示
            code_block (list[OpcodeBase], optional):
                该条件代码块中所含的实际代码，
                不包括条件本身。默认值为空列表
        """
        self.condition = condition
        self.state_line = state_line
        self.code_block = code_block if len(code_block) > 0 else []

    def __repr__(self):  # type: () -> str
        """返回该条件代码块的字符串表示

        Returns:
            str: 该条件代码块的字符串表示
        """
        return "ConditionCodeBlock(condition={}, line={}, code_block={})".format(
            self.condition,
            json.dumps(self.state_line, ensure_ascii=False),
            self.code_block,
        )


class ForLoopCodeBlock:
    """
    ForLoopCodeBlock 指示循环代码块。
    它包含了循环次数及每次循环所执行的代码块。
    它也同时保存了用于标识循环变量的变量名
    """

    variable = ""  # type: str
    repeat_times = DEFAULT_EMPTY_EXPRESSION  # type: ExpressionCombine
    state_line = ""  # type: str
    code_block = []  # type: list[OpcodeBase]

    def __init__(
        self, variable, repeat_times, state_line, code_block=[]
    ):  # type: (str, ExpressionCombine, str, list[OpcodeBase]) -> None
        """初始化并返回一个新的循环代码块

        Args:
            variable (str):
                用于标识循环变量的变量名
            repeat_times (ExpressionCombine):
                这个循环需要执行的次数。
                表达式的求值结果应是整数
            state_line (str):
                定义循环变量和循环次数的源代码行，
                目前只用于调试和错误提示
            code_block (list[OpcodeBase], optional):
                该循环所包含的所有代码。
                默认值为空列表
        """
        self.variable = variable
        self.repeat_times = repeat_times
        self.state_line = state_line
        self.code_block = code_block if len(code_block) > 0 else []

    def __repr__(self):  # type: () -> str
        """返回该循环代码块的字符串表示

        Returns:
            str: 该循环代码块的字符串表示
        """
        return "ForLoopCodeBlock(variable={}, repeat_times={}, state_line={}, code_block={})".format(
            json.dumps(self.variable, ensure_ascii=False),
            self.repeat_times,
            json.dumps(self.state_line, ensure_ascii=False),
            self.code_block,
        )


class OpcodeBase:
    """OpcodeBase 是所有操作码的基本实现"""

    opcode_id = 0  # type: int
    opcode_payload = None  # type: Any
    origin_line = ""  # type: str

    def __init__(
        self, opcode_id, opcode_payload, origin_line=""
    ):  # type: (int, Any, str) -> None
        """初始化并返回一个新的 基本操作码 实例

        Args:
            opcode_id (int):
                该操作码的 ID
            opcode_payload (Any):
                该操作码的负载
            origin_line (str, optional):
                该操作码对应的源代码行，
                目前只用于调试和错误提示。
                默认值为空字符串
        """
        self.opcode_id = opcode_id
        self.opcode_payload = opcode_payload
        self.origin_line = origin_line

    def __repr__(self):  # type: () -> str
        """返回该操作码的字符串表示

        Returns:
            str: 该操作码的字符串表示
        """
        prefix = "OpcodeBase(id={}, name={}".format(
            self.opcode_id, OPCODE_ID_TO_NAME[self.opcode_id]
        )
        if self.opcode_payload is not None:
            prefix += ", payload={}".format(self.opcode_payload)
        return prefix + ", line={})".format(
            json.dumps(self.origin_line, ensure_ascii=False)
        )


class OpcodeAssign(OpcodeBase):
    """OpcodeAssign 指示赋值操作"""

    opcode_id = OPCODE_ASSIGN  # type: int
    opcode_payload = ("", ExpressionCombine())  # type: tuple[str, ExpressionCombine]
    origin_line = ""  # type: str

    def __init__(
        self, payload, line
    ):  # type: (tuple[str, ExpressionCombine], str) -> None
        """初始化并返回一个新的 OpcodeAssign

        Args:
            payload (tuple[str, ExpressionCombine]):
                该赋值操作的负载。元组的第一个元素指示被赋值的变量名，
                元组的第二个元素则指示需要求解的复杂表达式。
                最终，该复杂表达式的求值结果将被赋值给相应的变量
            line (str):
                该赋值操作对应的源代码行。
                目前只用于调试和错误提示
        """
        OpcodeBase.__init__(self, OPCODE_ASSIGN, payload, line)


class OpcodeCondition(OpcodeBase):
    """
    OpcodeCondition 指示条件语句，
    它包含了一系列条件代码块。

    每个条件代码块都包含一个条件判断，
    以及满足该条件时应执行的代码块。

    在实际运行时，按顺序依次判断每个条件代码块的条件是否满足。
    只要有一个条件满足，则它旗下的代码块将被执行，
    然后剩余未被处理的条件代码块将被跳过
    """

    opcode_id = OPCODE_CONDITION  # type: int
    opcode_payload = []  # type: list[ConditionCodeBlock]
    origin_line = "fi"  # type: str

    def __init__(self, payload):  # type: (list[ConditionCodeBlock]) -> None
        """初始化并返回一个新的 OpcodeCondition

        Args:
            payload (list[ConditionCodeBlock]):
                该条件语句所包含的一系列条件代码块。
        """
        OpcodeBase.__init__(self, OPCODE_CONDITION, payload, "fi")


class OpcodeForLoop(OpcodeBase):
    """OpcodeForLoop 指示循环语句"""

    opcode_id = OPCODE_FOR_LOOP  # type: int
    opcode_payload = None  # type: ForLoopCodeBlock | None
    origin_line = "for"  # type: str

    def __init__(self, payload):  # type: (ForLoopCodeBlock) -> None
        """初始化并返回一个新的 OpcodeForLoop

        Args:
            payload (ForLoopCodeBlock): 该循环语句的负载
        """
        OpcodeBase.__init__(self, OPCODE_FOR_LOOP, payload, "for")


class OpcodeContinue(OpcodeBase):
    """
    OpcodeContinue 指示循环语句中的 continue 语句，
    它被用于跳过当前循环的剩余代码，并进入下一次循环
    """

    opcode_id = OPCODE_CONTINUE  # type: int
    opcode_payload = None  # type: None
    origin_line = ""  # type: str

    def __init__(self, line):  # type: (str) -> None
        """初始化并返回一个新的 OpcodeContinue

        Args:
            line (str):
                该 continue 语句对应的源代码行，
                目前只用于调试和错误提示
        """
        OpcodeBase.__init__(self, OPCODE_CONTINUE, None, line)


class OpcodeBreak(OpcodeBase):
    """
    OpcodeBreak 指示循环语句中的 break 语句，
    它被用于中止当前循环的执行，并跳出循环体
    """

    opcode_id = OPCODE_BREAK  # type: int
    opcode_payload = None  # type: None
    origin_line = ""  # type: str

    def __init__(self, line):  # type: (str) -> None
        """初始化并返回一个新的 OpcodeBreak

        Args:
            line (str):
                该 break 语句对应的源代码行，
                目前只用于调试和错误提示
        """
        OpcodeBase.__init__(self, OPCODE_BREAK, None, line)


class OpcodeExpression(OpcodeBase):
    """
    OpcodeExpression 指示表达式求解。它是返回语句的替代品。
    这意味着如果没有显式的返回语句出现，
    则最后一次表达式求解的结果即为用户所有代码的返回值
    """

    opcode_id = OPCODE_EXPRESSION  # type: int
    opcode_payload = ExpressionCombine()  # type: ExpressionCombine
    origin_line = ""  # type: str

    def __init__(self, payload, line):  # type: (ExpressionCombine, str) -> None
        """初始化并返回一个新的 OpcodeExpression

        Args:
            payload (ExpressionCombine):
                欲求解的复杂表达式。
                将在运行时被求解
            line (str):
                复杂表达式对应的源代码行，
                目前只用于调试和错误提示
        """
        OpcodeBase.__init__(self, OPCODE_EXPRESSION, payload, line)


class OpcodeReturn(OpcodeBase):
    """
    OpcodeReturn 指示返回语句。

    它求解保存在其中的复杂表达式，
    并作为用户代码的最终返回值。

    在一个返回语句被执行后，
    用户的代码执行将被终止
    """

    opcode_id = OPCODE_RETURN  # type: int
    opcode_payload = ExpressionCombine()  # type: ExpressionCombine
    origin_line = ""  # type: str

    def __init__(self, payload, line):  # type: (ExpressionCombine, str) -> None
        """初始化并返回一个新的 OpcodeReturn

        Args:
            payload (ExpressionCombine):
                该返回语句的负载
            line (str):
                该返回语句的源代码行，
                目前只用于调试和错误提示
        """
        OpcodeBase.__init__(self, OPCODE_RETURN, payload, line)
