# -*- coding: utf-8 -*-

from .define import (
    ExpressionElement,
    ELEMENT_ID_EQUAL,
    ELEMENT_ID_LESS_THAN,
    ELEMENT_ID_GREATER_THAN,
    ELEMENT_ID_LESS_EQUAL,
    ELEMENT_ID_GREATER_EQUAL,
    ELEMENT_ID_NOT_EQUAL,
    ELEMENT_ID_AND,
    ELEMENT_ID_OR,
    ELEMENT_ID_IN,
    ELEMENT_ID_INVERSE,
)


class ExpressionOperator(ExpressionElement):
    """ExpressionOperator 是所有比较运算符的基本实现"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload=[]):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的比较运算符

        Args:
            element_payload (list[ExpressionElement], optional):
                多个表达式元素组成的列表。
                默认值为空列表
        """
        self.element_id = 0
        self.element_payload = element_payload if len(element_payload) > 0 else []


class ExpressionGreaterThan(ExpressionOperator):
    """ExpressionGreaterThan 指示大于运算表示"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionGreaterThan

        Args:
            element_payload (list[ExpressionElement]):
                由 2 个表达式元素 A 和 B 组成的列表。
                运算 A > B 的结果即为 ExpressionGreaterThan 的值

        Raises:
            Exception:
                element_payload 只接受长度为 2 的列表。
                如果长度不满足，则将抛出相应的错误
        """
        if len(element_payload) != 2:
            raise Exception(
                'ExpressionGreaterThan/__init__: Only 2 parameters are accepted for operator ">"; element_payload={}'.format(
                    element_payload
                )
            )
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_GREATER_THAN


class ExpressionLessThan(ExpressionOperator):
    """ExpressionLessThan 指示小于运算表示"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionLessThan

        Args:
            element_payload (list[ExpressionElement]):
                由 2 个表达式元素 A 和 B 组成的列表。
                运算 A < B 的结果即为 ExpressionLessThan 的值

        Raises:
            Exception:
                element_payload 只接受长度为 2 的列表。
                如果长度不满足，则将抛出相应的错误
        """
        if len(element_payload) != 2:
            raise Exception(
                'ExpressionLessThan/__init__: Only 2 parameters are accepted for operator "<"; element_payload={}'.format(
                    element_payload
                )
            )
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_LESS_THAN


class ExpressionGreaterEqual(ExpressionOperator):
    """ExpressionGreaterEqual 指示大于等于运算表示"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionGreaterEqual

        Args:
            element_payload (list[ExpressionElement]):
                由 2 个表达式元素 A 和 B 组成的列表。
                运算 A >= B 的结果即为 ExpressionGreaterEqual 的值

        Raises:
            Exception:
                element_payload 只接受长度为 2 的列表。
                如果长度不满足，则将抛出相应的错误
        """
        if len(element_payload) != 2:
            raise Exception(
                'ExpressionGreaterEqual/__init__: Only 2 parameters are accepted for operator ">="; element_payload={}'.format(
                    element_payload
                )
            )
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_GREATER_EQUAL


class ExpressionLessEqual(ExpressionOperator):
    """ExpressionLessEqual 指示小于等于运算表示"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionLessEqual

        Args:
            element_payload (list[ExpressionElement]):
                由 2 个表达式元素 A 和 B 组成的列表。
                运算 A <= B 的结果即为 ExpressionLessEqual 的值

        Raises:
            Exception:
                element_payload 只接受长度为 2 的列表。
                如果长度不满足，则将抛出相应的错误
        """
        if len(element_payload) != 2:
            raise Exception(
                'ExpressionLessEqual/__init__: Only 2 parameters are accepted for operator "<="; element_payload={}'.format(
                    element_payload
                )
            )
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_LESS_EQUAL


class ExpressionEqual(ExpressionOperator):
    """ExpressionEqual 指示相等运算表示"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionEqual

        Args:
            element_payload (list[ExpressionElement]):
                由 2 个表达式元素 A 和 B 组成的列表。
                运算 A == B 的结果即为 ExpressionEqual 的值

        Raises:
            Exception:
                element_payload 只接受长度为 2 的列表。
                如果长度不满足，则将抛出相应的错误
        """
        if len(element_payload) != 2:
            raise Exception(
                'ExpressionEqual/__init__: Only 2 parameters are accepted for operator "=="; element_payload={}'.format(
                    element_payload
                )
            )
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_EQUAL


class ExpressionNotEqual(ExpressionOperator):
    """ExpressionNotEqual 指示不等运算表示"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionNotEqual

        Args:
            element_payload (list[ExpressionElement]):
                由 2 个表达式元素 A 和 B 组成的列表。
                运算 A != B 的结果即为 ExpressionNotEqual 的值

        Raises:
            Exception:
                element_payload 只接受长度为 2 的列表。
                如果长度不满足，则将抛出相应的错误
        """
        if len(element_payload) != 2:
            raise Exception(
                'ExpressionNotEqual/__init__: Only 2 parameters are accepted for operator "!="; element_payload={}'.format(
                    element_payload
                )
            )
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_NOT_EQUAL


class ExpressionAnd(ExpressionOperator):
    """ExpressionAnd 指示 AND 运算"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload=[]):  # type: (list[ExpressionElement]) -> None
        """
        初始化并返回一个新的 ExpressionAnd。

        它对 element_payload 中的所有元素进行 AND 运算，
        并将运算的结果作为 ExpressionAnd 的值。

        特别地，在按顺序运算时，若 element_payload 中的
        某个元素被断言为假，则 ExpressionAnd 将为假，
        并且无论后续表达式元素如何，都不会继续计算

        Args:
            element_payload (list[ExpressionElement]):
                多个表达式元素组成的列表
        """
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_AND


class ExpressionOr(ExpressionOperator):
    """ExpressionOr 指示 OR 运算"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload=[]):  # type: (list[ExpressionElement]) -> None
        """
        初始化并返回一个新的 ExpressionOr。

        它对 element_payload 中的所有元素进行 OR 运算，
        并将运算的结果作为 ExpressionOr 的值。

        特别地，在按顺序运算时，若 element_payload 中的
        某个元素被断言为真，则 ExpressionOr 将为真，
        并且无论后续表达式元素如何，都不会继续计算

        Args:
            element_payload (list[ExpressionElement]):
                多个表达式元素组成的列表
        """
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_OR


class ExpressionIn(ExpressionOperator):
    """ExpressionIn 指示 IN 运算"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionIn

        Args:
            element_payload (list[ExpressionElement]):
                由 2 个表达式元素 A 和 B 组成的列表。
                运算 A in B 的结果即为 ExpressionIn 的值

        Raises:
            Exception:
                element_payload 只接受长度为 2 的列表。
                如果长度不满足，则将抛出相应的错误
        """
        if len(element_payload) != 2:
            raise Exception(
                'ExpressionIn/__init__: Only 2 parameters are accepted for operator "in"; element_payload={}'.format(
                    element_payload
                )
            )
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_IN


class ExpressionInverse(ExpressionOperator):
    """ExpressionInverse 指示 NOT 运算"""

    element_id = 0  # type: int
    element_payload = []  # type: list[ExpressionElement]

    def __init__(self, element_payload):  # type: (list[ExpressionElement]) -> None
        """初始化并返回一个新的 ExpressionInverse

        Args:
            element_payload (list[ExpressionElement]):
                由 1 个表达式元素 A 组成的列表。
                运算 not A 的结果即为 ExpressionInverse 的值

        Raises:
            Exception:
                element_payload 只接受长度为 1 的列表。
                如果长度不满足，则将抛出相应的错误
        """
        if len(element_payload) != 1:
            raise Exception(
                'ExpressionInverse/__init__: Only 1 parameter is accepted for operator "not"; element_payload={}'.format(
                    element_payload
                )
            )
        ExpressionOperator.__init__(self, element_payload)
        self.element_id = ELEMENT_ID_INVERSE
