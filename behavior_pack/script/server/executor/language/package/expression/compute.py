# -*- coding: utf-8 -*-

from .define import (
    ExpressionElement,
    ELEMENT_ID_ADD,
    ELEMENT_ID_REMOVE,
    ELEMENT_ID_TIMES,
    ELEMENT_ID_DIVIDE,
)
from .compare import ExpressionOperator


class ExpressionTimes(ExpressionOperator):
    """ExpressionTimes 指示乘法运算表示"""

    element_id = ELEMENT_ID_TIMES  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload=[]):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionTimes

        Args:
            element_payload (list[ExpressionElement], optional):
                多个表达式元素组成的列表。
                它们相乘的结果即为该表达式的值。
                默认值为空列表
        """
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_TIMES


class ExpressionDivide(ExpressionOperator):
    """ExpressionDivide 指示除法运算表示"""

    element_id = ELEMENT_ID_DIVIDE  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload=[]):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionDivide

        Args:
            element_payload (list[ExpressionElement], optional):
                多个表达式元素组成的列表。以列表中第一个元素作为被除数，
                其余元素作为除数，依次进行除法运算后的结果，即为该表达式的值。
                默认值为空列表
        """
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_DIVIDE


class ExpressionAdd(ExpressionOperator):
    """ExpressionAdd 指示加法运算表示"""

    element_id = ELEMENT_ID_ADD  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload=[]):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionAdd

        Args:
            element_payload (list[ExpressionElement], optional):
                多个表达式元素组成的列表。
                它们的加和即为该表达式的值。
                默认值为空列表
        """
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_ADD


class ExpressionRemove(ExpressionOperator):
    """ExpressionRemove 指示减法运算表示"""

    element_id = ELEMENT_ID_REMOVE  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload=[]):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionRemove

        Args:
            element_payload (list[ExpressionElement], optional):
                多个表达式元素组成的列表。以列表中第一个元素作为被减数，
                其余元素作为减数，依次进行减法运算后的结果，即为该表达式的值。
                默认值为空列表
        """
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_REMOVE
