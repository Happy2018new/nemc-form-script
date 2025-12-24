# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any


class Marshaler:
    """
    Marshaler 定义了关于编码和解码的约束。
    任何实现了这这些功能的类都可以继承本接口
    """

    def __init__(self):  # type: () -> None
        """初始化并返回一个新的 Marshaler"""
        pass

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将该 Marshaler 编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 该 Marshaler 对应的 JSON 表示
        """
        return {}

    def unmarshal(self, data):  # type: (Any) -> Marshaler
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据置入该 Marshaler 中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            Marshaler: 返回 Marshaler 本身
        """
        _ = data
        return self


class BaseForm(Marshaler):
    """BaseForm 是所有形式化表单的父类"""
