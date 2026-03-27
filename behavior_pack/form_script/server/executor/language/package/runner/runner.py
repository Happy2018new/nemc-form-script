# -*- coding: utf-8 -*-
from __future__ import division

import json
import bisect
from .compile import CompileResult
from .external import GameInteract, BuiltInFunction
from .define import (
    CHECK_POINT_TYPE_NORMAL,
    CHECK_POINT_TYPE_CONDITION,
    CHECK_POINT_TYPE_FOR_LOOP,
    VariableMapping,
    CheckPoint,
)

try:
    range = xrange  # type: ignore
except Exception:
    pass

EMPTY_COMPILE_RESULT = CompileResult([], [], VariableMapping())
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
    它用于运行已经过编译的字节码表示
    """

    _compiled = EMPTY_COMPILE_RESULT  # type: CompileResult
    _vars_len = 0  # type: int

    def __init__(self, compiled):  # type: (CompileResult) -> None
        """初始化并返回一个新的解释器

        Args:
            compiled (CompileResult):
                CodeCompiler 的编译结果
        """
        self._compiled = compiled
        self._vars_len = compiled.var_mapping.variables_count()

    def _chk_by_pc(self, pc):  # type: (int) -> CheckPoint
        """
        _chk_by_pc 通过给出的程序的计数器，
        查找它对应的原始代码行（的检查点）

        Args:
            pc (int):
                给出的程序计数器

        Returns:
            CheckPoint:
                该程序计数器对应的检查点
        """
        all_start_pc = [cp.start_pc for cp in self._compiled.check_point]
        index = bisect.bisect_right(all_start_pc, pc) - 1

        if index >= 0:
            chk = self._compiled.check_point[index]
            if pc <= chk.end_pc:
                return chk

        err = "Unresolved program counter; pc={}, self._compiled={}".format(
            pc, self._compiled
        )
        return CheckPoint(CHECK_POINT_TYPE_NORMAL, 0, 0, [err])

    def _fast_panic(self, chk, err):  # type: (CheckPoint, str) -> None
        """_fast_panic 抛出运行时错误

        Args:
            chk (CheckPoint):
                当前程序计数器对应的检查点
            err (str):
                需要抛出的错误信息

        Raises:
            InternalException:
                err 所指示的错误
        """
        if chk.point_type == CHECK_POINT_TYPE_NORMAL:
            raise InternalException(
                "Runtime Error.\n\n- Error -\n  {}\n\n- Code -\n  {}".format(
                    err, chk.payload[0]
                )
            )
        elif chk.point_type == CHECK_POINT_TYPE_CONDITION:
            prefix = "Runtime Error in Condition.\n\n- Error -\n  {}\n\n- Condition -\n  {}".format(
                err, chk.payload[0]
            )
            if len(chk.payload) > 1:
                prefix += "\n\n- Code -\n  {}".format(chk.payload[1])
            raise InternalException(prefix)
        elif chk.point_type == CHECK_POINT_TYPE_FOR_LOOP:
            prefix = "Runtime Error in For Loop.\n\n- Error -\n  {}\n\n- For Loop -\n  {}".format(
                err, chk.payload[0]
            )
            if len(chk.payload) > 1:
                prefix += "\n\n- Code -\n  {}".format(chk.payload[1])
            raise InternalException(prefix)
        else:
            raise Exception("unreachable")

    def running(
        self,
        require_return=True,  # type: bool
        var_maps=EMPTY_VARIABLES,  # type: dict[str, int | bool | float | str]
        interact=EMPTY_GAME_INTERACT,  # type: GameInteract
        builtins=EMPTY_BUILTIN_FUNCTION,  # type: BuiltInFunction
    ):  # type: (...) -> int | bool | float | str | None
        """
        running 通过启动了一个虚拟机，
        它以解释方式的运行所有代码，
        并返回它们在运行时的返回值。

        您可以选择预先指定 var_maps 参数，
        这意味着您将可以预先初始化一些变量。

        给出的 var_maps 在返回前不应修改，
        但在该函数返回后进行修改是被允许的

        Args:
            require_return (bool, optional):
                是否检查这些代码是否返回值。
                如果为真且没有返回值，则抛出异常。
                默认值为真
            var_maps (dict[str, int | bool | float | str], optional):
                运行代码前已经初始化的变量。
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
        pc = 0  # type: int
        stack = []  # type: list[int | bool | float | str]
        result = None  # type: int | bool | float | str | None

        _push = stack.append
        _pop = stack.pop

        byte_code = self._compiled.byte_code  # type: list[int | bool | float | str]
        variables = [
            None
        ] * self._vars_len  # type: list[int | bool | float | str | None]

        for key, value in var_maps.items():
            index = self._compiled.var_mapping.index_by_name(key, True)
            if index is not None:
                variables[index] = value

        try:
            while True:
                op = byte_code[pc]

                if op == 0:  # LOAD_CONST (0, CONST)
                    _push(byte_code[pc + 1])
                    pc += 2
                elif op == 1:  # LOAD_VALUE (1, VAR_INDEX)
                    value = variables[byte_code[pc + 1]]  # type: ignore
                    if value is not None:
                        _push(value)
                        pc += 2
                    else:
                        varname = self._compiled.var_mapping.name_by_index(byte_code[pc + 1])  # type: ignore
                        raise Exception(
                            "Variable {} used before assignment".format(
                                json.dumps(varname, ensure_ascii=False)
                            )
                        )
                elif op == 2:  # STORE_VALUE (2, VAR_INDEX)
                    variables[byte_code[pc + 1]] = _pop()  # type: ignore
                    pc += 2
                elif op == 3:  # LOOP_JUMP (3, VAR_INDEX, JUMP_TO)
                    if stack[-1] < stack[-2]:  # type: ignore
                        variables[byte_code[pc + 1]] = stack[-1]  # type: ignore
                        stack[-1] += 1  # type: ignore
                        pc += 3
                    else:
                        pc = byte_code[pc + 2]  # type: ignore
                elif op == 4:  # LOOP_POP (4)
                    _pop()
                    _pop()
                    pc += 1
                elif op == 5:  # DIRECT_JUMP (5, JUMP_TO)
                    pc = byte_code[pc + 1]  # type: ignore
                elif op == 6:  # FALSE_JUMP (6, JUMP_TO)
                    if not _pop():
                        pc = byte_code[pc + 1]  # type: ignore
                    else:
                        pc += 2
                elif op == 7:  # TRUE_JUMP (7, JUMP_TO)
                    if _pop():
                        pc = byte_code[pc + 1]  # type: ignore
                    else:
                        pc += 2
                elif op == 8:  # HANDLE_COMPUTE (8, POP_LEN, (+, -, *, /))
                    pop_len = byte_code[pc + 1]
                    sub_type = byte_code[pc + 2]
                    if sub_type == 0:  # +
                        if pop_len == 2:
                            temp = _pop()
                            _push(_pop() + temp)  # type: ignore
                        elif pop_len == 3:
                            temp1 = _pop()
                            temp2 = _pop()
                            _push(_pop() + temp2 + temp1)  # type: ignore
                        elif pop_len > 1:  # type: ignore
                            temp = stack[-pop_len]  # type: ignore
                            for i in range(pop_len - 1):  # type: ignore
                                temp += stack[-pop_len + i + 1]  # type: ignore
                            del stack[-pop_len:]  # type: ignore
                            _push(temp)
                    elif sub_type == 1:  # -
                        if pop_len == 2:
                            temp = _pop()
                            _push(_pop() - temp)  # type: ignore
                        elif pop_len == 3:
                            temp1 = _pop()
                            temp2 = _pop()
                            _push(_pop() - temp2 - temp1)  # type: ignore
                        elif pop_len > 1:  # type: ignore
                            temp = stack[-pop_len]  # type: ignore
                            for i in range(pop_len - 1):  # type: ignore
                                temp -= stack[-pop_len + i + 1]  # type: ignore
                            del stack[-pop_len:]  # type: ignore
                            _push(temp)
                    elif sub_type == 2:  # *
                        if pop_len == 2:
                            temp = _pop()
                            _push(_pop() * temp)  # type: ignore
                        elif pop_len == 3:
                            temp1 = _pop()
                            temp2 = _pop()
                            _push(_pop() * temp2 * temp1)  # type: ignore
                        elif pop_len > 1:  # type: ignore
                            temp = stack[-pop_len]  # type: ignore
                            for i in range(pop_len - 1):  # type: ignore
                                temp *= stack[-pop_len + i + 1]  # type: ignore
                            del stack[-pop_len:]  # type: ignore
                            _push(temp)
                    elif sub_type == 3:  # /
                        if pop_len == 2:
                            temp = _pop()
                            _push(_pop() / temp)  # type: ignore
                        elif pop_len == 3:
                            temp1 = _pop()
                            temp2 = _pop()
                            _push(_pop() / temp2 / temp1)  # type: ignore
                        elif pop_len > 1:  # type: ignore
                            temp = stack[-pop_len]  # type: ignore
                            for i in range(pop_len - 1):  # type: ignore
                                temp /= stack[-pop_len + i + 1]  # type: ignore
                            del stack[-pop_len:]  # type: ignore
                            _push(temp)
                    pc += 3
                elif op == 9:  # HANDLE_COMPARE (9, (==, !=, <, >, <=, >=))
                    sub_type = byte_code[pc + 1]
                    if sub_type == 0:  # ==
                        _push(_pop() == _pop())
                    elif sub_type == 1:  # !=
                        _push(_pop() != _pop())
                    elif sub_type == 2:  # <
                        _push(_pop() > _pop())  # type: ignore
                    elif sub_type == 3:  # >
                        _push(_pop() < _pop())  # type: ignore
                    elif sub_type == 4:  # <=
                        _push(_pop() >= _pop())  # type: ignore
                    elif sub_type == 5:  # >=
                        _push(_pop() <= _pop())  # type: ignore
                    pc += 2
                elif (
                    op == 10
                ):  # HANDLE_LOGIC_ANDOR (10, (and, or)); NOTE: Copy the compare result
                    sub_type = byte_code[pc + 1]
                    if sub_type == 0:  # and
                        temp1 = _pop()
                        temp2 = _pop()
                        temp3 = temp2 and temp1
                        _push(temp3)
                        _push(temp3)
                    elif sub_type == 1:  # or
                        temp1 = _pop()
                        temp2 = _pop()
                        temp3 = temp2 or temp1
                        _push(temp3)
                        _push(temp3)
                    pc += 2
                elif op == 11:  # HANDLE_LOGIC_INNOT (11, (not, in))
                    sub_type = byte_code[pc + 1]
                    if sub_type == 0:  # not
                        _push(not _pop())
                    elif sub_type == 1:  # in
                        temp = _pop()
                        _push(_pop() in temp)  # type: ignore
                    pc += 2
                elif op == 12:  # HANDLE_CAST (12, (int, bool, float, str))
                    sub_type = byte_code[pc + 1]
                    if sub_type == 0:  # int
                        _push(int(_pop()))
                    elif sub_type == 1:  # bool
                        _push(bool(_pop()))
                    elif sub_type == 2:  # float
                        _push(float(_pop()))
                    elif sub_type == 3:  # str
                        _push(str(_pop()))
                    pc += 2
                elif op == 13:  # HANDLE_FUNC (13, POP_LEN, FUNC_NAME)
                    # Calling the target function
                    pop_len = byte_code[pc + 1]
                    if pop_len > 0:  # type: ignore
                        args = stack[-pop_len:]  # type: ignore
                        del stack[-pop_len:]  # type: ignore
                        val = builtins.get_func(byte_code[pc + 2])(*args)  # type: ignore
                    else:
                        val = builtins.get_func(byte_code[pc + 2])()  # type: ignore
                    # Do type check for the return value
                    if isinstance(val, (int, bool, float, str)):
                        _push(val)
                        pc += 3
                        continue
                    try:
                        if isinstance(val, unicode):  # type: ignore
                            _push(str(val))
                            pc += 3
                            continue
                    except Exception:
                        pass
                    # Raise error if type check failed
                    raise Exception(
                        "The data type of return value from func {} must be int/bool/float/str, but got {}".format(
                            byte_code[pc + 2], val
                        )
                    )
                elif (
                    op == 14
                ):  # HANDLE_INTERACT (14, (command, score, selector)) or (14, ref, REF_TYPE)
                    sub_type = byte_code[pc + 1]
                    if sub_type == 0:  # command
                        command = _pop()
                        if not isinstance(command, str):
                            raise Exception(
                                'The argument for "command" must be str; value={}'.format(
                                    command
                                )
                            )
                        _push(interact.command_func()(command))
                        pc += 2
                    elif sub_type == 1:  # score
                        scoreboard = _pop()
                        target = _pop()
                        if not isinstance(target, str):
                            raise Exception(
                                'The target argument for "score" must be str; target={}'.format(
                                    target
                                )
                            )
                        if not isinstance(scoreboard, str):
                            raise Exception(
                                'The scoreboard argument for "score" must be str; scoreboard={}'.format(
                                    scoreboard
                                )
                            )
                        _push(interact.score_func()(target, scoreboard))
                        pc += 2
                    elif sub_type == 2:  # selector
                        value = _pop()
                        if not isinstance(value, str):
                            raise Exception(
                                'The argument for "selector" must be str; value={}'.format(
                                    value
                                )
                            )
                        _push(interact.selector_func()(value))
                        pc += 2
                    elif sub_type == 3:  # ref
                        # Get index and value
                        index = _pop()
                        if isinstance(index, bool) or not isinstance(index, int):
                            raise Exception(
                                'The index for "ref" statement must be int; index={}'.format(
                                    index
                                )
                            )
                        value = interact.ref_func()(index)
                        # Do assertion for value type
                        ref_type = byte_code[pc + 2]
                        if ref_type == 0:  # int
                            if isinstance(value, bool) or not isinstance(value, int):
                                raise Exception(
                                    "Assertion failed: Expect an int but got {}".format(
                                        value
                                    )
                                )
                        elif ref_type == 1:  # bool
                            if not isinstance(value, bool):
                                raise Exception(
                                    "Assertion failed: Expect a bool but got {}".format(
                                        value
                                    )
                                )
                        elif ref_type == 2:  # float
                            if not isinstance(value, float):
                                raise Exception(
                                    "Assertion failed: Expect a float but got {}".format(
                                        value
                                    )
                                )
                        elif ref_type == 3:  # str
                            if not isinstance(value, str):
                                raise Exception(
                                    "Assertion failed: Expect a str but got {}".format(
                                        value
                                    )
                                )
                        # Push stack and update pc
                        _push(value)
                        pc += 3
                elif op == 15:  # STORE_RETURN_VAL (15)
                    result = _pop()
                    pc += 1
                elif op == 16:  # PROGRAM_STOP_RUN (16)
                    break
                elif op == 17:  # INTERNAL_PANIC (17, ERROR)
                    raise Exception(byte_code[pc + 1])
        except Exception as e:
            if isinstance(e, InternalException):
                raise e
            else:
                self._fast_panic(self._chk_by_pc(pc), str(e))
                raise Exception("unreachable")

        if require_return and result is None:
            raise Exception("Runtime Error: No return value after running the code")
        return result
