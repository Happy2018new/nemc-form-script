# -*- coding: utf-8 -*-
from __future__ import division

BYTECODE_LOAD_CONST = 0  # (0, CONST)
BYTECODE_LOAD_VALUE = 1  # (1, VAR_INDEX)
BYTECODE_STORE_VALUE = 2  # (2, VAR_INDEX)
BYTECODE_LOOP_JUMP = 3  # (3, VAR_INDEX, JUMP_TO)
BYTECODE_LOOP_CHECK = 4  # (4, CHECK_TYPE)
BYTECODE_DIRECT_JUMP = 5  # (5, JUMP_TO)
BYTECODE_FALSE_JUMP = 6  # (6, JUMP_TO)
BYTECODE_TRUE_JUMP = 7  # (7, JUMP_TO)
BYTECODE_HANDLE_COMPUTE = 8  # (8, POP_LEN, (+, -, *, /))
BYTECODE_HANDLE_COMPARE = 9  # (9, (==, !=, <, >, <=, >=))
BYTECODE_HANDLE_LOGIC_ANDOR = 10  # (10, (and, or)); NOTE: Copy the compare result
BYTECODE_HANDLE_LOGIC_INNOT = 11  # (11, (not, in))
BYTECODE_HANDLE_CAST = 12  # (12, (int, bool, float, str))
BYTECODE_HANDLE_FUNC = 13  # (13, POP_LEN, FUNC_NAME)
BYTECODE_HANDLE_INTERACT = 14  # (14, (command, score, selector)) or (14, ref, REF_TYPE)
BYTECODE_STORE_RETURN_VAL = 15  # (15)
BYTECODE_PROGRAM_STOP_RUN = 16  # (16)
BYTECODE_INTERNAL_PANIC = 17  # (17, ERROR)

LOOP_CHECK_TYPE_DATA_TYPE = 0
LOOP_CHECK_TYPE_POP_STACK = 1

COMPUTE_TYPE_ADD = 0
COMPUTE_TYPE_REMOVE = 1
COMPUTE_TYPE_TIMES = 2
COMPUTE_TYPE_DIVIDE = 3

COMPARE_TYPE_EQUAL = 0
COMPARE_TYPE_NOT_EQUAL = 1
COMPARE_TYPE_LESS_THAN = 2
COMPARE_TYPE_GREATER_THAN = 3
COMPARE_TYPE_LESS_EQUAL = 4
COMPARE_TYPE_GREATER_EQUAL = 5

LOGIC_ANDOR_TYPE_AND = 0
LOGIC_ANDOR_TYPE_OR = 1

LOGIC_INNOT_TYPE_NOT = 0
LOGIC_INNOT_TYPE_IN = 1

CAST_TYPE_INT = 0
CAST_TYPE_BOOL = 1
CAST_TYPE_FLOAT = 2
CAST_TYPE_STR = 3

INTERACT_TYPE_COMMAND = 0
INTERACT_TYPE_SCORE = 1
INTERACT_TYPE_SELECTOR = 2
INTERACT_TYPE_REF = 3

REF_TYPE_INT = 0
REF_TYPE_BOOL = 1
REF_TYPE_FLOAT = 2
REF_TYPE_STR = 3

CHECK_POINT_TYPE_NORMAL = 0
CHECK_POINT_TYPE_CONDITION = 1
CHECK_POINT_TYPE_FOR_LOOP = 2


class VariableMapping:
    """
    为了提升性能，在用户代码被实际运行时，
    变量名将被映射为一个整数，因此变量访问将直接通过列表下标进行。

    VariableMapping 便保存了这样的一个变量映射表，
    它既保存了变量名到整数索引的映射，也保存了整数索引到变量名的映射。

    对于前者的映射，它用于在编译代码期间确定变量的整数索引；
    对于后者的映射，它会在运行代码出错时在输出的错误信息中提供变量名
    """

    _name_to_index = {}  # type: dict[str, int]
    _index_to_name = []  # type: list[str]

    def __init__(self):  # type: () -> None
        """
        初始化并返回一个新的 VariableMapping
        """
        self._name_to_index = {}
        self._index_to_name = []

    def __repr__(self):  # type: () -> str
        """
        返回 VariableMapping 的字符串表示

        Returns:
            str: 该 VariableMapping 的字符串表示
        """
        return "VariableMapping(name_to_index={}, index_to_name={})".format(
            self._name_to_index, self._index_to_name
        )

    def variables_count(self):  # type: () -> int
        """
        variables_count 返回映射中变量的总数

        Returns:
            int: 映射中变量的总数
        """
        return len(self._index_to_name)

    def index_by_name(self, varname, readonly=False):  # type: (str, bool) -> int | None
        """
        index_by_name 通过变量名查找其对应的整数索引。
        如果 readonly 为假，则它会在变量不存在时创建

        Args:
            varname (str):
                欲查找的变量名
            readonly (bool, optional):
                当前查找是否只读。
                默认值为 False

        Returns:
            int | None:
                如果 readonly 为假，则将在变量不存在时创建索引并返回它；
                否则 readonly 为真，则若给出的变量不存在，那么返回 None
        """
        if varname in self._name_to_index:
            return self._name_to_index[varname]

        if not readonly:
            varindex = len(self._index_to_name)
            self._name_to_index[varname] = varindex
            self._index_to_name.append(varname)
            return varindex

        return None

    def name_by_index(self, varindex):  # type: (int) -> str
        """
        name_by_index 通过整数索引查找其对应的变量名

        Args:
            varindex (int):
                该变量的整数索引

        Raises:
            Exception:
                如果给出的索引超出范围，
                则抛出相应的错误

        Returns:
            str: 该变量的变量名
        """
        if varindex < 0 or varindex >= len(self._index_to_name):
            raise Exception(
                "name_by_index: Index out of range [{}] with length {}".format(
                    varindex, len(self._index_to_name)
                )
            )
        return self._index_to_name[varindex]


class CheckPoint:
    """
    CheckPoint 描述了用户代码中的检查点。

    每个检查点都应对应一个单行的代码，
    并同时指出其对应字节码的起始、终止位置。

    因此，检查点可用于在运行时出错时向用户提供源代码行，
    从而，用户可以容易的检查出出错的代码行
    """

    point_type = 0  # type: int
    start_pc = 0  # type: int
    end_pc = 0  # type: int
    payload = []  # type: list[str]

    def __init__(
        self,
        point_type,  # type: int
        start_pc,  # type: int
        end_pc,  # type: int
        payload,  # type: list[str]
    ):  # type: (...) -> None
        """
        初始化并返回一个新的 CheckPoint 用作检查点。

        检查点只可能有三种类型，第一种是常规的检查点。
        在这种情况下，源代码行不在条件语句和循环语句中，
        且 payload 只携带一个字符串，表示该行的源代码。

        第二种和第三种检查点分别适用于条件语句和循环语句。
        在这种情况下，payload 可携带一到两个字符串。

        可以确保第一个字符串始终表示包含条件语句或循环语句起始行的源代码。
        并且，若第二个字符串存在，则它指示条件语句或循环语句中具体的代码

        Args:
            point_type (int):
                该检查点的类型。只可能为下列之一。
                    - CHECK_POINT_TYPE_NORMAL
                    - CHECK_POINT_TYPE_CONDITION
                    - CHECK_POINT_TYPE_FOR_LOOP
            start_pc (int):
                源代码行对应字节码的起始位置
            end_pc (int):
                源代码行对应字节码的终止位置
            payload (list[str]):
                该检查点所携带的，关于源代码行的负载
        """
        self.point_type = point_type
        self.start_pc = start_pc
        self.end_pc = end_pc
        self.payload = payload

    def __repr__(self):  # type: () -> str
        """返回 CheckPoint 的字符串表示

        Returns:
            str: 该 CheckPoint 的字符串表示
        """
        return "CheckPoint(point_type={}, start_pc={}, end_pc={}, payload={})".format(
            self.point_type, self.start_pc, self.end_pc, self.payload
        )
