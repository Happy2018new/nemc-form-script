# -*- coding: utf-8 -*-

import json
from .external import GameInteract, BuiltInFunction
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
    ExpressionElement,
    TYPE_ENUM_INT,
    TYPE_ENUM_BOOL,
    TYPE_ENUM_FLOAT,
    TYPE_ENUM_STR,
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
from ..expression.basic import (
    ExpressionLiteral,
    ExpressionReference,
    ExpressionSelector,
    ExpressionScore,
    ExpressionCommand,
    ExpressionFunction,
)

try:
    range = xrange  # type: ignore
except Exception:
    pass

STATES_KEEP_RUNNING = 0
STATES_LOOP_CONTINUE = 1
STATES_LOOP_BREAK = 2
STATES_CODE_RETURN = 3

EMPTY_VARIABLES = {}
EMPTY_GAME_INTERACT = GameInteract()
EMPTY_BUILTIN_FUNCTION = BuiltInFunction()


class InternalException(Exception):
    """
    InternalException 是解释器运行时，其自身抛出的异常。
    该异常可以与其他异常进行区分，以解决错误格式化问题
    """

    pass


class CodeRunner:
    """
    CodeRunner 是该编程语言的解释器。
    它用于运行已经过编译的抽象语法表示
    """

    code_block = []  # type: list[OpcodeBase]
    _interact = EMPTY_GAME_INTERACT  # type: GameInteract
    _builtins = EMPTY_BUILTIN_FUNCTION  # type: BuiltInFunction
    _variables = EMPTY_VARIABLES  # type: dict[str, int | bool | float | str]
    _return = None  # type: int | bool | float | str | None

    def __init__(
        self,
        code_block=[],  # type: list[OpcodeBase]
    ):  # type: (...) -> None
        """初始化并返回一个新的解释器

        Args:
            code_block (list[OpcodeBase], optional):
                CodeParser 的编译结果。
                默认值为空列表
        """
        self.code_block = code_block if len(code_block) > 0 else []
        self._interact = EMPTY_GAME_INTERACT
        self._builtins = EMPTY_BUILTIN_FUNCTION
        self._variables = EMPTY_VARIABLES
        self._return = None

    def _fast_normal_panic(self, code_block, err):  # type: (OpcodeBase, str) -> None
        """_fast_normal_panic 抛出标准的运行时错误

        Args:
            code_block (OpcodeBase):
                运行时错误发生时，
                错误所在的代码块
            err (str):
                需要抛出的错误信息

        Raises:
            InternalException:
                err 所指示的错误
        """
        raise InternalException(
            "Runtime Error.\n\n- Error -\n  {}\n\n- Code -\n  {}".format(
                err, code_block.origin_line
            )
        )

    def _fast_condition_panic(
        self, condition, index=-1, err=""
    ):  # type: (ConditionCodeBlock, int, str) -> None
        """
        _fast_condition_panic 抛出发生在条件代码块中的运行时错误

        Args:
            condition (ConditionCodeBlock):
                错误所在的条件代码块
            index (int, optional):
                如果错误发生在条件本身，则应提供 -1。
                否则，错误发生在内部代码块中，那么请提供相应的索引。
                默认值为 -1
            err (str, optional):
                需要抛出的错误信息。
                默认值为空字符串

        Raises:
            InternalException:
                err 所指示的错误
        """
        prefix = "Runtime Error in Condition.\n\n- Error -\n  {}\n\n- Condition -\n  {}".format(
            err, condition.state_line
        )
        if index != -1:
            prefix += "\n\n- Code -\n  {}".format(
                condition.code_block[index].origin_line
            )
        raise InternalException(prefix)

    def _fast_for_loop_panic(
        self, for_loop, index=-1, err=""
    ):  # type: (ForLoopCodeBlock, int, str) -> None
        """
        _fast_for_loop_panic 抛出发生在循环代码块中的运行时错误

        Args:
            for_loop (ForLoopCodeBlock):
                错误所在的循环代码块
            index (int, optional):
                如果错误发生在循环次数解析，则应提供 -1。
                否则，错误发生在内部代码块中，那么请提供相应的索引。
                默认值为 -1
            err (str, optional):
                需要抛出的错误信息。
                默认值为空字符串

        Raises:
            InternalException:
                err 所指示的错误
        """
        prefix = "Runtime Error in For Loop.\n\n- Error -\n  {}\n\n- For Loop -\n  {}".format(
            err, for_loop.state_line
        )
        if index != -1:
            prefix += "\n\n- Code -\n  {}".format(
                for_loop.code_block[index].origin_line
            )
        raise InternalException(prefix)

    def _process_literal(
        self, element
    ):  # type: (ExpressionLiteral) -> int | bool | float | str
        """
        _process_literal 解析并返回字面量表达式元素的值

        Args:
            element (ExpressionLiteral):
                给定的字面量表达式元素

        Raises:
            Exception:
                当求值出错时抛出

        Returns:
            int | bool | float | str:
                目标字面量表达式元素的求值结果
        """
        if element.element_id == ELEMENT_ID_VAR:
            if element.element_payload not in self._variables:
                raise Exception(
                    "Variable {} used before assignment".format(
                        json.dumps(element.element_payload, ensure_ascii=False)
                    )
                )
            return self._variables[element.element_payload]  # type: ignore

        if isinstance(element.element_payload, ExpressionCombine):
            value = self._process_element(element.element_payload)
            if element.element_id == ELEMENT_ID_INT:
                return int(value)
            elif element.element_id == ELEMENT_ID_BOOL:
                return bool(value)
            elif element.element_id == ELEMENT_ID_FLOAT:
                return float(value)
            elif element.element_id == ELEMENT_ID_STR:
                return str(value)
            return value

        return element.element_payload

    def _process_ref(
        self, element
    ):  # type: (ExpressionReference) -> int | bool | float | str
        """
        _process_ref 处理引用表达式元素。

        它对其中保存的索引进行求值，调用相应的函数，
        并以这样的方式来获取对应的表单响应数据

        Args:
            element (ExpressionReference):
                给定的引用表达式元素

        Raises:
            Exception:
                当求值出错时抛出

        Returns:
            int | bool | float | str:
                目标引用表达式元素的求值结果
        """
        index = self._process_element(element.element_payload[1])
        if isinstance(index, bool) or not isinstance(index, int):
            raise Exception(
                'The index for "ref" statement must be int; index={}'.format(index)
            )
        value = self._interact.ref_func()(index)

        if element.element_payload[0] == TYPE_ENUM_INT:
            if isinstance(value, bool) or not isinstance(value, int):
                raise Exception(
                    "Assertion failed: Expect an int but got {}".format(value)
                )
        elif element.element_payload[0] == TYPE_ENUM_BOOL:
            if not isinstance(value, bool):
                raise Exception(
                    "Assertion failed: Expect a bool but got {}".format(value)
                )
        elif element.element_payload[0] == TYPE_ENUM_FLOAT:
            if not isinstance(value, float):
                raise Exception(
                    "Assertion failed: Expect a float but got {}".format(value)
                )
        elif element.element_payload[0] == TYPE_ENUM_STR:
            if not isinstance(value, str):
                raise Exception(
                    "Assertion failed: Expect a str but got {}".format(value)
                )

        return value

    def _process_selector(self, element):  # type: (ExpressionSelector) -> str
        """
        _process_selector 解析目标选择器表达式元素所指示的目标选择器，
        并返回解析所得的，对应这个目标选择器的实体名

        Args:
            element (ExpressionSelector):
                给定的目标选择器表达式元素

        Raises:
            Exception:
                当解析目标选择器发生错误时抛出

        Returns:
            str:
                对应相应目标选择器的实体名
        """
        assert element.element_payload is not None
        value = self._process_element(element.element_payload)
        if not isinstance(value, str):
            raise Exception(
                'The argument for "selector" must be str; value={}'.format(value)
            )
        return self._interact.selector_func()(value)

    def _process_score(self, element):  # type: (ExpressionScore) -> int
        """
        _process_score 获取记分板分数表达式元素所指示的实体的分数。
        应当说明的是，其中所涉及的记分板亦可在表达式元素中找到

        Args:
            element (ExpressionScore):
                给定的记分板分数表达式元素

        Raises:
            Exception:
                当获取分数发生错误时抛出

        Returns:
            int:
                对应实体在相应记分板上的分数
        """
        target = self._process_element(element.element_payload[0])
        if not isinstance(target, str):
            raise Exception(
                'The target argument for "score" must be str; target={}'.format(target)
            )
        scoreboard = self._process_element(element.element_payload[1])
        if not isinstance(scoreboard, str):
            raise Exception(
                'The scoreboard argument for "score" must be str; scoreboard={}'.format(
                    scoreboard
                )
            )
        return self._interact.score_func()(target, scoreboard)

    def _process_command(self, element):  # type: (ExpressionCommand) -> int
        """
        _process_command 运行命令表达式元素所指示的命令，
        并返回命令的成功次数。

        就目前而言，由于网易接口只能判定命令是否成功，
        因此返回值应只可能是 0 或 1

        Args:
            element (ExpressionCommand):
                给定的命令表达式元素

        Raises:
            Exception:
                在运行相应命令发生错误时抛出

        Returns:
            int:
                命令的成功次数。
                应只可能是 0 或 1
        """
        assert element.element_payload is not None
        command = self._process_element(element.element_payload)
        if not isinstance(command, str):
            raise Exception(
                'The argument for "command" must be str; value={}'.format(command)
            )
        return self._interact.command_func()(command)

    def _process_function(
        self, element
    ):  # type: (ExpressionFunction) -> int | bool | float | str
        """
        _process_function 对给定的函数表达式元素进行求值

        Args:
            element (ExpressionFunction):
                给定的函数表达式元素

        Raises:
            Exception:
                当求值出错时抛出

        Returns:
            int | bool | float | str:
                给定表达式元素的求值结果
        """
        val = self._builtins.get_func(element.element_payload[0])(
            *[self._process_element(i) for i in element.element_payload[1]]
        )

        if isinstance(val, (int, bool, float, str)):
            return val
        try:
            if isinstance(val, unicode):  # type: ignore
                return str(val)
        except Exception:
            pass

        raise Exception(
            "_process_function: The data type of return value from func {} must be int/bool/float/str, but got {}".format(
                element.element_payload[0], val
            )
        )

    def _process_element(
        self, element
    ):  # type: (ExpressionElement) -> int | bool | float | str
        """_process_element 对给定的表达式元素进行求值

        Args:
            element (ExpressionElement):
                欲被求值的表达式元素

        Raises:
            Exception:
                当求值出错时抛出

        Returns:
            int | bool | float | str:
                给定表达式元素的求值结果
        """
        # Literal and expression process first
        if isinstance(element, ExpressionLiteral):
            return self._process_literal(element)
        if element.element_id == ELEMENT_ID_EXPR:
            return self._process_element(element.element_payload[0])  # type: ignore
        # Then process compute operations
        if element.element_id == ELEMENT_ID_ADD:
            temp = self._process_element(element.element_payload[0])  # type: ignore
            for i in element.element_payload[1:]:  # type: ignore
                temp += self._process_element(i)  # type: ignore
            return temp
        if element.element_id == ELEMENT_ID_REMOVE:
            temp = self._process_element(element.element_payload[0])  # type: ignore
            for i in element.element_payload[1:]:  # type: ignore
                temp -= self._process_element(i)  # type: ignore
            return temp
        if element.element_id == ELEMENT_ID_TIMES:
            temp = self._process_element(element.element_payload[0])  # type: ignore
            for i in element.element_payload[1:]:  # type: ignore
                temp *= self._process_element(i)  # type: ignore
            return temp
        if element.element_id == ELEMENT_ID_DIVIDE:
            temp = self._process_element(element.element_payload[0])  # type: ignore
            for i in element.element_payload[1:]:  # type: ignore
                temp /= self._process_element(i)  # type: ignore
            return temp
        # Then process compare operations
        if element.element_id == ELEMENT_ID_EQUAL:
            left = self._process_element(element.element_payload[0])  # type: ignore
            right = self._process_element(element.element_payload[1])  # type: ignore
            return left == right  # type: ignore
        if element.element_id == ELEMENT_ID_NOT_EQUAL:
            left = self._process_element(element.element_payload[0])  # type: ignore
            right = self._process_element(element.element_payload[1])  # type: ignore
            return left != right  # type: ignore
        if element.element_id == ELEMENT_ID_GREATER_THAN:
            left = self._process_element(element.element_payload[0])  # type: ignore
            right = self._process_element(element.element_payload[1])  # type: ignore
            return left > right  # type: ignore
        if element.element_id == ELEMENT_ID_LESS_THAN:
            left = self._process_element(element.element_payload[0])  # type: ignore
            right = self._process_element(element.element_payload[1])  # type: ignore
            return left < right  # type: ignore
        if element.element_id == ELEMENT_ID_GREATER_EQUAL:
            left = self._process_element(element.element_payload[0])  # type: ignore
            right = self._process_element(element.element_payload[1])  # type: ignore
            return left >= right  # type: ignore
        if element.element_id == ELEMENT_ID_LESS_EQUAL:
            left = self._process_element(element.element_payload[0])  # type: ignore
            right = self._process_element(element.element_payload[1])  # type: ignore
            return left <= right  # type: ignore
        # Then process logic operations
        if element.element_id == ELEMENT_ID_AND:
            temp = self._process_element(element.element_payload[0])  # type: ignore
            for i in element.element_payload[1:]:  # type: ignore
                temp = temp and self._process_element(i)
                if not temp:
                    return temp
            return temp
        if element.element_id == ELEMENT_ID_OR:
            temp = self._process_element(element.element_payload[0])  # type: ignore
            for i in element.element_payload[1:]:  # type: ignore
                temp = temp or self._process_element(i)
                if temp:
                    return temp
            return temp
        if element.element_id == ELEMENT_ID_INVERSE:
            value = self._process_element(element.element_payload[0])  # type: ignore
            return not value  # type: ignore
        if element.element_id == ELEMENT_ID_IN:
            left = self._process_element(element.element_payload[0])  # type: ignore
            right = self._process_element(element.element_payload[1])  # type: ignore
            return left in right  # type: ignore
        # At last, we process the game interact operations
        if element.element_id == ELEMENT_ID_COMMAND:
            return self._process_command(element)  # type: ignore
        if element.element_id == ELEMENT_ID_FUNC:
            return self._process_function(element)  # type: ignore
        if element.element_id == ELEMENT_ID_SCORE:
            return self._process_score(element)  # type: ignore
        if element.element_id == ELEMENT_ID_SELECTOR:
            return self._process_selector(element)  # type: ignore
        if element.element_id == ELEMENT_ID_REF:
            return self._process_ref(element)  # type: ignore
        # If the element is unknown, raise an exception
        raise Exception("Unknown element is given; element={}".format(element))

    def _process_block(self, code_block):  # type: (OpcodeBase) -> int
        """
        _process_block 运行一个语句（操作码），或者一个代码块

        Args:
            code_block (OpcodeBase):
                给定的基本操作对象

        Raises:
            Exception:
                当运行发生错误时抛出

        Returns:
            int:
                在运行该操作码后，解释器应该转移到哪个状态。
                应只可能是下面列出的可能之一。
                    - STATES_KEEP_RUNNING: 解释器继续运行
                    - STATES_LOOP_CONTINUE: 解释器单次跳过循环体
                    - STATES_LOOP_BREAK: 解释器终止循环体
                    - STATES_CODE_RETURN: 解释器返回值，然后终止
        """
        if isinstance(code_block, OpcodeAssign):
            name = code_block.opcode_payload[0]
            value = self._process_element(code_block.opcode_payload[1])
            self._variables[name] = value
            return STATES_KEEP_RUNNING
        if isinstance(code_block, OpcodeContinue):
            return STATES_LOOP_CONTINUE
        if isinstance(code_block, OpcodeBreak):
            return STATES_LOOP_BREAK
        if isinstance(code_block, OpcodeExpression):
            self._return = self._process_element(code_block.opcode_payload)
            return STATES_KEEP_RUNNING
        if isinstance(code_block, OpcodeReturn):
            self._return = self._process_element(code_block.opcode_payload)
            return STATES_CODE_RETURN

        if isinstance(code_block, OpcodeCondition):
            for i in code_block.opcode_payload:
                cond = False

                if i.condition is None:
                    cond = True
                else:
                    try:
                        if self._process_element(i.condition):
                            cond = True
                    except Exception as e:
                        if isinstance(e, InternalException):
                            raise e
                        else:
                            self._fast_condition_panic(i, -1, str(e))
                            raise Exception("unreachable")

                if cond:
                    for ind, val in enumerate(i.code_block):
                        try:
                            states = self._process_block(val)
                            if states != STATES_KEEP_RUNNING:
                                return states
                        except Exception as e:
                            if isinstance(e, InternalException):
                                raise e
                            else:
                                self._fast_condition_panic(i, ind, str(e))
                                raise Exception("unreachable")
                    break
            return STATES_KEEP_RUNNING

        if isinstance(code_block, OpcodeForLoop):
            assert code_block.opcode_payload is not None
            for_loop = code_block.opcode_payload
            variable = for_loop.variable

            try:
                repeat_times = self._process_element(for_loop.repeat_times)
            except Exception as e:
                if isinstance(e, InternalException):
                    raise e
                else:
                    self._fast_for_loop_panic(for_loop, -1, str(e))
                    raise Exception("unreachable")
            if isinstance(repeat_times, bool) or not isinstance(repeat_times, int):
                self._fast_for_loop_panic(
                    for_loop, -1, "The repeat times of for loop must be int"
                )
                raise Exception("unreachable")

            for i in range(repeat_times):
                self._variables[variable] = i
                for ind, val in enumerate(for_loop.code_block):
                    try:
                        states = self._process_block(val)
                        if states == STATES_KEEP_RUNNING:
                            continue
                        elif states == STATES_LOOP_CONTINUE:
                            break
                        elif states == STATES_LOOP_BREAK:
                            return STATES_KEEP_RUNNING
                        elif states == STATES_CODE_RETURN:
                            return STATES_CODE_RETURN
                    except Exception as e:
                        if isinstance(e, InternalException):
                            raise e
                        else:
                            self._fast_for_loop_panic(for_loop, ind, str(e))
                            raise Exception("unreachable")
            return STATES_KEEP_RUNNING

        return STATES_KEEP_RUNNING

    def _running(
        self, require_return
    ):  # type: (bool) -> int | bool | float | str | None
        """
        _running 以解释的方式运行所有代码，
        并返回这些代码在运行时的返回值。

        它没有进行任何初始化工作，
        也不会进行任何的垃圾回收

        Args:
            require_return (bool):
                是否检查这些代码是否返回值。
                如果为真且没有返回值，则抛出异常

        Raises:
            Exception:
                当运行发生错误时抛出

        Returns:
            int | bool | float | str | None:
                运行代码时所得的返回值
        """
        for i in self.code_block:
            try:
                states = self._process_block(i)
                if states == STATES_KEEP_RUNNING:
                    continue
                elif states == STATES_CODE_RETURN:
                    break
                else:
                    raise Exception(
                        "Continue and break statement only accepted under for loop code block"
                    )
            except Exception as e:
                if isinstance(e, InternalException):
                    raise e
                else:
                    self._fast_normal_panic(i, str(e))
                    raise Exception("unreachable")

        if require_return and self._return is None:
            raise Exception("Runtime Error: No return value after running the code")
        return self._return

    def running(
        self,
        require_return=True,  # type: bool
        variables=EMPTY_VARIABLES,  # type: dict[str, int | bool | float | str]
        interact=EMPTY_GAME_INTERACT,  # type: GameInteract
        builtins=EMPTY_BUILTIN_FUNCTION,  # type: BuiltInFunction
    ):  # type: (...) -> int | bool | float | str | None
        """
        running 以解释方式的运行所有代码，
        并返回这些代码在运行时的返回值。

        您可以选择预先指定 variables 参数，
        这意味着您将可以预先初始化一些变量，
        并在 running 返回值后查看这些变量
        的最终状态

        Args:
            require_return (bool, optional):
                是否检查这些代码是否返回值。
                如果为真且没有返回值，则抛出异常。
                默认值为真
            variables (dict[str, int | bool | float | str], optional):
                运行代码前已经初始化的变量。
                该字典会在运行时被动态修改。
                默认值为 EMPTY_VARIABLES
            interact (GameInteract, optional):
                用于与 Minecraft 进行交互的接口。
                默认值为 EMPTY_GAME_INTERACT
            builtins (BuiltInFunction, optional):
                外部函数提供者为用户定义的内建函数。
                默认值为 EMPTY_BUILTIN_FUNCTION

        Returns:
            int | bool | float | str | None:
                运行代码时所得的返回值
        """
        self._interact = interact
        self._builtins = builtins

        frame = self._variables
        self._variables = variables if variables is not EMPTY_VARIABLES else {}

        try:
            return self._running(require_return)
        finally:
            self._variables = frame
            self._return = None
