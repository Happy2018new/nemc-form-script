# -*- coding: utf-8 -*-
from __future__ import division

from .define import (
    BYTECODE_LOAD_CONST,
    BYTECODE_LOAD_VALUE,
    BYTECODE_STORE_VALUE,
    BYTECODE_LOOP_JUMP,
    BYTECODE_LOOP_POP,
    BYTECODE_DIRECT_JUMP,
    BYTECODE_FALSE_JUMP,
    BYTECODE_TRUE_JUMP,
    BYTECODE_HANDLE_COMPUTE,
    BYTECODE_HANDLE_COMPARE,
    BYTECODE_HANDLE_LOGIC_ANDOR,
    BYTECODE_HANDLE_LOGIC_INNOT,
    BYTECODE_HANDLE_CAST,
    BYTECODE_HANDLE_FUNC,
    BYTECODE_HANDLE_INTERACT,
    BYTECODE_STORE_RETURN_VAL,
    BYTECODE_PROGRAM_STOP_RUN,
    BYTECODE_INTERNAL_PANIC,
    COMPUTE_TYPE_ADD,
    COMPUTE_TYPE_REMOVE,
    COMPUTE_TYPE_TIMES,
    COMPUTE_TYPE_DIVIDE,
    COMPARE_TYPE_EQUAL,
    COMPARE_TYPE_NOT_EQUAL,
    COMPARE_TYPE_LESS_THAN,
    COMPARE_TYPE_GREATER_THAN,
    COMPARE_TYPE_LESS_EQUAL,
    COMPARE_TYPE_GREATER_EQUAL,
    LOGIC_ANDOR_TYPE_AND,
    LOGIC_ANDOR_TYPE_OR,
    LOGIC_INNOT_TYPE_NOT,
    LOGIC_INNOT_TYPE_IN,
    CAST_TYPE_INT,
    CAST_TYPE_BOOL,
    CAST_TYPE_FLOAT,
    CAST_TYPE_STR,
    INTERACT_TYPE_COMMAND,
    INTERACT_TYPE_SCORE,
    INTERACT_TYPE_SELECTOR,
    INTERACT_TYPE_REF,
    REF_TYPE_INT,
    REF_TYPE_BOOL,
    REF_TYPE_FLOAT,
    REF_TYPE_STR,
    CHECK_POINT_TYPE_NORMAL,
    CHECK_POINT_TYPE_CONDITION,
    CHECK_POINT_TYPE_FOR_LOOP,
    VariableMapping,
    CheckPoint,
)
from ..parser.expression.define import (
    ExpressionElement,
    TYPE_ENUM_INT,
    TYPE_ENUM_BOOL,
    TYPE_ENUM_FLOAT,
    TYPE_ENUM_STR,
    ELEMENT_ID_VAR,
    ELEMENT_ID_INT,
    ELEMENT_ID_BOOL,
    ELEMENT_ID_FLOAT,
    ELEMENT_ID_STR,
)
from ..parser.expression.basic import (
    ExpressionLiteral,
    ExpressionReference,
    ExpressionSelector,
    ExpressionScore,
    ExpressionCommand,
    ExpressionFunction,
)
from ..parser.expression.compare import (
    ExpressionLessThan,
    ExpressionGreaterThan,
    ExpressionLessEqual,
    ExpressionGreaterEqual,
    ExpressionEqual,
    ExpressionNotEqual,
    ExpressionAnd,
    ExpressionOr,
    ExpressionIn,
    ExpressionInverse,
)
from ..parser.expression.compute import (
    ExpressionAdd,
    ExpressionRemove,
    ExpressionTimes,
    ExpressionDivide,
)
from ..parser.expression.combine import ExpressionCombine
from ..parser.define import (
    OpcodeBase,
    OpcodeAssign,
    OpcodeCondition,
    OpcodeForLoop,
    OpcodeContinue,
    OpcodeBreak,
    OpcodeExpression,
    OpcodeReturn,
)


class ForLoopEnv:
    """
    ForLoopEnv 描述了一个循环语句的上下文环境。

    continue_pc 指示在处理到 continue 语句时，
    程序计数器应跳转的位置。

    end_indexes 储存了所有调用 break 语句的程序计数器位置。
    因此，当循环体的字节码被编译完成后，可通过重新修改它们，
    使得虚拟机执行到这些字节码时，可以正确的 break 出循环体。

    在实际设计上，因条件语句只能 continue/break 距离其最近的循环体，
    并且由于在多层的条件语句嵌套中，它们能操作的循环体也是唯一的，
    因此该实例可在编译阶段递归传递，因而较深的条件语句也能控制循环体
    """

    continue_pc = 0  # type: int
    end_indexes = []  # type: list[int]

    def __init__(self):  # type: () -> None
        """
        初始化并返回一个新的 ForLoopEnv
        """
        self.continue_pc = 0
        self.end_indexes = []


class CompileResult:
    """
    CompileResult 是编译器将 AST 语法树处理为字节码的结果
    """

    byte_code = []  # type: list[int | bool | float | str]
    check_point = []  # type: list[CheckPoint]
    var_mapping = VariableMapping()  # type: VariableMapping

    def __init__(
        self,
        byte_code,  # type: list[int | bool | float | str]
        check_point,  # type: list[CheckPoint]
        var_mapping,  # type: VariableMapping
    ):  # type: (...) -> None
        """
        初始化并返回一个新的 CompileResult

        Args:
            byte_code (list[int | bool | float | str]):
                编译器编译所得的字节码序列
            check_point (list[CheckPoint]):
                编译器编译过程中产生的检查点序列。
                应确保该序列已经按源代码行的顺序排序
            var_mapping (VariableMapping):
                编译器编译过程中所用的变量映射表
        """
        self.byte_code = byte_code
        self.check_point = check_point
        self.var_mapping = var_mapping

    def __repr__(self):  # type: () -> str
        """返回 CompileResult 的字符串表示

        Returns:
            str: 该 CompileResult 的字符串表示
        """
        return "CompileResult(byte_code={}, check_point={}, var_mapping={})".format(
            self.byte_code, self.check_point, self.var_mapping
        )


class CodeCompiler:
    """
    CodeCompiler 是将 AST 语法树编译为字节码的编译器
    """

    _ast = []  # type: list[OpcodeBase]
    _ans = []  # type: list[int | bool | float | str]
    _chk = []  # type: list[CheckPoint]
    _map = VariableMapping()  # type: VariableMapping

    def __init__(self, code_block=[]):  # type: (list[OpcodeBase]) -> None
        """初始化并返回一个新的编译器

        Args:
            code_block (list[OpcodeBase], optional):
                CodeParser 的编译结果
                默认值为空列表
        """
        self._ast = code_block if len(code_block) > 0 else []
        self._ans = []
        self._chk = []
        self._map = VariableMapping()

    def _get_line_code(self, opcode):  # type: (OpcodeBase) -> str | None
        """_get_line_code 返回 opcode 对应的源代码行

        Args:
            opcode (OpcodeBase): 目标操作码实例

        Returns:
            str | None:
                如果给出的操作码不是条件语句或循环语句，则返回其对应的源代码行；
                否则给出的操作码是条件语句或循环语句，那么返回 None
        """
        if isinstance(opcode, OpcodeAssign):
            return opcode.origin_line
        elif isinstance(opcode, OpcodeContinue):
            return opcode.origin_line
        elif isinstance(opcode, OpcodeBreak):
            return opcode.origin_line
        elif isinstance(opcode, OpcodeExpression):
            return opcode.origin_line
        elif isinstance(opcode, OpcodeReturn):
            return opcode.origin_line
        else:
            return None

    def _handle_literal(self, element):  # type: (ExpressionLiteral) -> None
        """
        _handle_literal 将一个字面量表达式元素编译为字节码。
        可以保证这些字节码执行完成后，栈的顶部是它的求值结果

        Args:
            element (ExpressionLiteral):
                待处理的字面量表达式元素
        """
        if element.element_id == ELEMENT_ID_VAR:
            self._ans.append(BYTECODE_LOAD_VALUE)
            self._ans.append(self._map.index_by_name(element.element_payload))  # type: ignore
            return

        if isinstance(element.element_payload, ExpressionCombine):
            self._handle_element(element.element_payload)
            if element.element_id == ELEMENT_ID_INT:
                self._ans.append(BYTECODE_HANDLE_CAST)
                self._ans.append(CAST_TYPE_INT)
            elif element.element_id == ELEMENT_ID_BOOL:
                self._ans.append(BYTECODE_HANDLE_CAST)
                self._ans.append(CAST_TYPE_BOOL)
            elif element.element_id == ELEMENT_ID_FLOAT:
                self._ans.append(BYTECODE_HANDLE_CAST)
                self._ans.append(CAST_TYPE_FLOAT)
            elif element.element_id == ELEMENT_ID_STR:
                self._ans.append(BYTECODE_HANDLE_CAST)
                self._ans.append(CAST_TYPE_STR)
            return

        self._ans.append(BYTECODE_LOAD_CONST)
        self._ans.append(element.element_payload)

    def _handle_element(self, element):  # type: (ExpressionElement) -> None
        """
        _handle_element 将一个表达式元素编译为对应的字节码。
        可以保证这些字节码执行完成后，栈的顶部是它的求值结果

        Args:
            element (ExpressionElement):
                待处理的表达式元素
        """
        if isinstance(element, ExpressionLiteral):
            self._handle_literal(element)
        elif isinstance(element, ExpressionCombine):
            self._handle_element(element.element_payload[0])
        elif isinstance(
            element,
            (ExpressionAdd, ExpressionRemove, ExpressionTimes, ExpressionDivide),
        ):
            for i in element.element_payload:
                self._handle_element(i)
            self._ans.append(BYTECODE_HANDLE_COMPUTE)
            self._ans.append(len(element.element_payload))
            if isinstance(element, ExpressionAdd):
                self._ans.append(COMPUTE_TYPE_ADD)
            elif isinstance(element, ExpressionRemove):
                self._ans.append(COMPUTE_TYPE_REMOVE)
            elif isinstance(element, ExpressionTimes):
                self._ans.append(COMPUTE_TYPE_TIMES)
            elif isinstance(element, ExpressionDivide):
                self._ans.append(COMPUTE_TYPE_DIVIDE)

        elif isinstance(
            element,
            (
                ExpressionEqual,
                ExpressionNotEqual,
                ExpressionLessThan,
                ExpressionGreaterThan,
                ExpressionLessEqual,
                ExpressionGreaterEqual,
            ),
        ):
            self._handle_element(element.element_payload[0])
            self._handle_element(element.element_payload[1])
            if isinstance(element, ExpressionEqual):
                self._ans.append(BYTECODE_HANDLE_COMPARE)
                self._ans.append(COMPARE_TYPE_EQUAL)
            elif isinstance(element, ExpressionNotEqual):
                self._ans.append(BYTECODE_HANDLE_COMPARE)
                self._ans.append(COMPARE_TYPE_NOT_EQUAL)
            elif isinstance(element, ExpressionLessThan):
                self._ans.append(BYTECODE_HANDLE_COMPARE)
                self._ans.append(COMPARE_TYPE_LESS_THAN)
            elif isinstance(element, ExpressionGreaterThan):
                self._ans.append(BYTECODE_HANDLE_COMPARE)
                self._ans.append(COMPARE_TYPE_GREATER_THAN)
            elif isinstance(element, ExpressionLessEqual):
                self._ans.append(BYTECODE_HANDLE_COMPARE)
                self._ans.append(COMPARE_TYPE_LESS_EQUAL)
            elif isinstance(element, ExpressionGreaterEqual):
                self._ans.append(BYTECODE_HANDLE_COMPARE)
                self._ans.append(COMPARE_TYPE_GREATER_EQUAL)

        elif isinstance(element, ExpressionAnd):
            # Prepare
            jump_end_indexes = []
            self._ans.append(BYTECODE_LOAD_CONST)
            self._ans.append(True)
            # Handle each logic
            for i in element.element_payload:
                self._handle_element(i)
                self._ans.append(BYTECODE_HANDLE_LOGIC_ANDOR)
                self._ans.append(LOGIC_ANDOR_TYPE_AND)
                self._ans.append(BYTECODE_FALSE_JUMP)
                self._ans.append(0)
                jump_end_indexes.append(len(self._ans) - 1)
            # Handle jump end
            end_index = len(self._ans)
            for i in jump_end_indexes:
                self._ans[i] = end_index
        elif isinstance(element, ExpressionOr):
            # Prepare
            jump_end_indexes = []
            self._ans.append(BYTECODE_LOAD_CONST)
            self._ans.append(False)
            # Handle each logic
            for i in element.element_payload:
                self._handle_element(i)
                self._ans.append(BYTECODE_HANDLE_LOGIC_ANDOR)
                self._ans.append(LOGIC_ANDOR_TYPE_OR)
                self._ans.append(BYTECODE_TRUE_JUMP)
                self._ans.append(0)
                jump_end_indexes.append(len(self._ans) - 1)
            # Handle jump end
            end_index = len(self._ans)
            for i in jump_end_indexes:
                self._ans[i] = end_index

        elif isinstance(element, ExpressionInverse):
            self._handle_element(element.element_payload[0])
            self._ans.append(BYTECODE_HANDLE_LOGIC_INNOT)
            self._ans.append(LOGIC_INNOT_TYPE_NOT)
        elif isinstance(element, ExpressionIn):
            self._handle_element(element.element_payload[0])
            self._handle_element(element.element_payload[1])
            self._ans.append(BYTECODE_HANDLE_LOGIC_INNOT)
            self._ans.append(LOGIC_INNOT_TYPE_IN)

        elif isinstance(element, ExpressionFunction):
            for i in element.element_payload[1]:
                self._handle_element(i)
            self._ans.append(BYTECODE_HANDLE_FUNC)
            self._ans.append(len(element.element_payload[1]))
            self._ans.append(element.element_payload[0])
        elif isinstance(element, ExpressionCommand):
            assert element.element_payload is not None
            self._handle_element(element.element_payload)
            self._ans.append(BYTECODE_HANDLE_INTERACT)
            self._ans.append(INTERACT_TYPE_COMMAND)
        elif isinstance(element, ExpressionSelector):
            assert element.element_payload is not None
            self._handle_element(element.element_payload)
            self._ans.append(BYTECODE_HANDLE_INTERACT)
            self._ans.append(INTERACT_TYPE_SELECTOR)
        elif isinstance(element, ExpressionScore):
            self._handle_element(element.element_payload[0])
            self._handle_element(element.element_payload[1])
            self._ans.append(BYTECODE_HANDLE_INTERACT)
            self._ans.append(INTERACT_TYPE_SCORE)
        elif isinstance(element, ExpressionReference):
            self._handle_element(element.element_payload[1])
            self._ans.append(BYTECODE_HANDLE_INTERACT)
            self._ans.append(INTERACT_TYPE_REF)
            if element.element_payload[0] == TYPE_ENUM_INT:
                self._ans.append(REF_TYPE_INT)
            elif element.element_payload[0] == TYPE_ENUM_BOOL:
                self._ans.append(REF_TYPE_BOOL)
            elif element.element_payload[0] == TYPE_ENUM_FLOAT:
                self._ans.append(REF_TYPE_FLOAT)
            elif element.element_payload[0] == TYPE_ENUM_STR:
                self._ans.append(REF_TYPE_STR)

    def _handle_condition(
        self, code_block, for_loop_env
    ):  # type: (OpcodeCondition, ForLoopEnv | None) -> None
        """
        _handle_condition 将给出的条件语句编译为字节码

        Args:
            code_block (OpcodeCondition):
                要编译为字节码的条件语句
            for_loop_env (ForLoopEnv | None):
                该条件语句所在循环语句的上下文环境。
                若它不位于循环体中，请设置为 None
        """
        # Jump end for all branches
        jump_end_indexes = []

        for i in code_block.opcode_payload:
            # Handle else statement
            if i.condition is None:
                for j in i.code_block:
                    start_pc = len(self._ans)
                    self._handle_code_block(j, for_loop_env)
                    line_code = self._get_line_code(j)
                    if line_code is not None:
                        self._chk.append(
                            CheckPoint(
                                CHECK_POINT_TYPE_CONDITION,
                                start_pc,
                                len(self._ans) - 1,
                                [i.state_line, line_code],
                            )
                        )
                break

            # Handle condition and jump false
            start_pc = len(self._ans)
            self._handle_element(i.condition)
            self._ans.append(BYTECODE_FALSE_JUMP)
            self._ans.append(0)
            false_jump = len(self._ans) - 1
            self._chk.append(
                CheckPoint(
                    CHECK_POINT_TYPE_CONDITION, start_pc, false_jump, [i.state_line]
                )
            )

            # Handle code block
            for j in i.code_block:
                start_pc = len(self._ans)
                self._handle_code_block(j, for_loop_env)
                line_code = self._get_line_code(j)
                if line_code is not None:
                    self._chk.append(
                        CheckPoint(
                            CHECK_POINT_TYPE_CONDITION,
                            start_pc,
                            len(self._ans) - 1,
                            [i.state_line, line_code],
                        )
                    )

            # Handle false jump and jump end
            self._ans.append(BYTECODE_DIRECT_JUMP)
            self._ans.append(0)
            jump_end_indexes.append(len(self._ans) - 1)
            self._ans[false_jump] = len(self._ans)

        # Set the pc for all jump end
        end_index = len(self._ans)
        for index in jump_end_indexes:
            self._ans[index] = end_index

    def _handle_for_loop(self, code_block):  # type: (OpcodeForLoop) -> None
        """
        _handle_for_loop 将给出的循环语句编译为字节码

        Args:
            code_block (OpcodeForLoop):
                要编译为字节码的循环语句
        """
        # Prepare
        assert code_block.opcode_payload is not None
        for_loop_env = ForLoopEnv()
        for_loop = code_block.opcode_payload
        varindex = self._map.index_by_name(for_loop.variable)

        # Handle repeat times
        start_pc = len(self._ans)
        self._handle_element(for_loop.repeat_times)
        self._ans.append(BYTECODE_LOAD_CONST)
        self._ans.append(0)
        self._chk.append(
            CheckPoint(
                CHECK_POINT_TYPE_FOR_LOOP,
                start_pc,
                len(self._ans) - 1,
                [for_loop.state_line],
            )
        )

        # Handle continue loop or break loop
        continue_pc = len(self._ans)
        for_loop_env.continue_pc = continue_pc
        self._ans.append(BYTECODE_LOOP_JUMP)
        self._ans.append(varindex)  # type: ignore
        self._ans.append(0)
        for_loop_env.end_indexes.append(len(self._ans) - 1)

        # Handle loop body
        for i in for_loop.code_block:
            start_pc = len(self._ans)
            self._handle_code_block(i, for_loop_env)
            line_code = self._get_line_code(i)
            if line_code is not None:
                self._chk.append(
                    CheckPoint(
                        CHECK_POINT_TYPE_FOR_LOOP,
                        start_pc,
                        len(self._ans) - 1,
                        [for_loop.state_line, line_code],
                    )
                )
        self._ans.append(BYTECODE_DIRECT_JUMP)
        self._ans.append(continue_pc)

        # Pop the repeat times and set the pc for all jump end
        end_index = len(self._ans)
        self._ans.append(BYTECODE_LOOP_POP)
        for index in for_loop_env.end_indexes:
            self._ans[index] = end_index

    def _handle_code_block(
        self, code_block, for_loop_env
    ):  # type: (OpcodeBase, ForLoopEnv | None) -> None
        """
        _handle_code_block 将给出的代码块编译为字节码

        Args:
            code_block (OpcodeBase):
                待处理的代码块
            for_loop_env (ForLoopEnv | None):
                该代码块所在循环语句的上下文环境。
                若它不位于循环体中，请设置为 None
        """
        if isinstance(code_block, OpcodeAssign):
            self._handle_element(code_block.opcode_payload[1])
            self._ans.append(BYTECODE_STORE_VALUE)
            self._ans.append(self._map.index_by_name(code_block.opcode_payload[0]))  # type: ignore
        elif isinstance(code_block, OpcodeCondition):
            self._handle_condition(code_block, for_loop_env)
        elif isinstance(code_block, OpcodeForLoop):
            self._handle_for_loop(code_block)
        elif isinstance(code_block, OpcodeContinue):
            if for_loop_env is None:
                self._ans.append(BYTECODE_INTERNAL_PANIC)
                self._ans.append(
                    "Continue statement only accepted under for loop code block"
                )
            else:
                self._ans.append(BYTECODE_DIRECT_JUMP)
                self._ans.append(for_loop_env.continue_pc)
        elif isinstance(code_block, OpcodeBreak):
            if for_loop_env is None:
                self._ans.append(BYTECODE_INTERNAL_PANIC)
                self._ans.append(
                    "Break statement only accepted under for loop code block"
                )
            else:
                self._ans.append(BYTECODE_DIRECT_JUMP)
                self._ans.append(0)
                for_loop_env.end_indexes.append(len(self._ans) - 1)
        elif isinstance(code_block, OpcodeExpression):
            self._handle_element(code_block.opcode_payload)
            self._ans.append(BYTECODE_STORE_RETURN_VAL)
        elif isinstance(code_block, OpcodeReturn):
            self._handle_element(code_block.opcode_payload)
            self._ans.append(BYTECODE_STORE_RETURN_VAL)
            self._ans.append(BYTECODE_PROGRAM_STOP_RUN)

    def compile(self):  # type: () -> CompileResult
        """
        compile 将 AST 语法树编译为字节码

        Returns:
            CompileResult: 编译所得结果
        """
        self._ans = []
        self._chk = []
        self._map = VariableMapping()

        for i in self._ast:
            start_pc = len(self._ans)
            self._handle_code_block(i, None)
            line_code = self._get_line_code(i)
            if line_code is not None:
                self._chk.append(
                    CheckPoint(
                        CHECK_POINT_TYPE_NORMAL,
                        start_pc,
                        len(self._ans) - 1,
                        [line_code],
                    )
                )

        self._ans.append(BYTECODE_PROGRAM_STOP_RUN)
        return CompileResult(self._ans, self._chk, self._map)
