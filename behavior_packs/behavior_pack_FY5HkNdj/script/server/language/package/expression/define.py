# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json

CONTEXT_PARSE_ASSIGN = 1 << 0
CONTEXT_PARSE_IF = 1 << 1
CONTEXT_PARSE_FOR = 1 << 2
CONTEXT_PARSE_ARGUMENT = 1 << 3
CONTEXT_PARSE_SUB_EXPR = 1 << 4
CONTEXT_PARSE_BARRIER = 1 << 5

TYPE_ENUM_INT = 0
TYPE_ENUM_BOOL = 1
TYPE_ENUM_FLOAT = 2
TYPE_ENUM_STR = 3

ELEMENT_ID_VAR = 0
ELEMENT_ID_EXPR = 1
ELEMENT_ID_EQUAL = 2
ELEMENT_ID_LESS_THAN = 3
ELEMENT_ID_GREATER_THAN = 4
ELEMENT_ID_LESS_EQUAL = 5
ELEMENT_ID_GREATER_EQUAL = 6
ELEMENT_ID_ADD = 7
ELEMENT_ID_REMOVE = 8
ELEMENT_ID_TIMES = 9
ELEMENT_ID_DIVIDE = 10
ELEMENT_ID_NOT_EQUAL = 11
ELEMENT_ID_INT = 12
ELEMENT_ID_BOOL = 13
ELEMENT_ID_FLOAT = 14
ELEMENT_ID_STR = 15
ELEMENT_ID_REF = 16
ELEMENT_ID_SELECTOR = 17
ELEMENT_ID_SCORE = 18
ELEMENT_ID_COMMAND = 19
ELEMENT_ID_FUNC = 20
ELEMENT_ID_AND = 21
ELEMENT_ID_OR = 22
ELEMENT_ID_IN = 23
ELEMENT_ID_INVERSE = 24

ELEMENT_ID_TO_NAME = {
    ELEMENT_ID_VAR: "variable",
    ELEMENT_ID_EXPR: "expression",
    ELEMENT_ID_EQUAL: "==",
    ELEMENT_ID_LESS_THAN: "<",
    ELEMENT_ID_GREATER_THAN: ">",
    ELEMENT_ID_LESS_EQUAL: "<=",
    ELEMENT_ID_GREATER_EQUAL: ">=",
    ELEMENT_ID_ADD: "+",
    ELEMENT_ID_REMOVE: "-",
    ELEMENT_ID_TIMES: "*",
    ELEMENT_ID_DIVIDE: "/",
    ELEMENT_ID_NOT_EQUAL: "!=",
    ELEMENT_ID_INT: "int(...)",
    ELEMENT_ID_BOOL: "bool(...)",
    ELEMENT_ID_FLOAT: "float(...)",
    ELEMENT_ID_STR: "str(...)",
    ELEMENT_ID_REF: "{ref, ...}",
    ELEMENT_ID_SELECTOR: "{selector, ...}",
    ELEMENT_ID_SCORE: "{score, ...}",
    ELEMENT_ID_FUNC: "{func, ...}",
    ELEMENT_ID_AND: "... and ...",
    ELEMENT_ID_OR: "... or ...",
    ELEMENT_ID_IN: "... in ...",
    ELEMENT_ID_INVERSE: "not ...",
}


class ExpressionElement:
    """ExpressionElement 是任何表达式元素的基本实现"""

    element_id = 0  # type: int
    element_payload = None  # type: Any | None

    def __init__(self, element_id, element_payload):  # type: (int, Any) -> None
        """初始化并返回一个新的基本表达式元素

        Args:
            element_id (int): 表达式元素的 ID
            element_payload (Any): 表达式元素的负载
        """
        self.element_id = element_id
        self.element_payload = element_payload

    def __repr__(self):  # type: () -> str
        """返回表达式元素的字符串表示

        Returns:
            str: 该表达式元素的字符串表示
        """
        prefix = "ExpressionElement(id={}, name={}".format(
            self.element_id,
            json.dumps(ELEMENT_ID_TO_NAME[self.element_id], ensure_ascii=False),
        )
        if self.element_payload is not None:
            if isinstance(self.element_payload, str):
                prefix += ", payload={}".format(
                    json.dumps(self.element_payload, ensure_ascii=False)
                )
            else:
                prefix += ", payload={}".format(self.element_payload)
        return prefix + ")"
