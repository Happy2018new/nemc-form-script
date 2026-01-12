# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from ..base import StringWithHash
from ....formal.base import Marshaler

EMPTY_STRING_WITH_HASH = StringWithHash()


class BaseForm(Marshaler):
    """BaseForm 是数据保存实现中，所有表单的父类"""

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将该 BaseForm 编码为对应的 JSON 表示

        Returns:
            dict[str, Any]: 该 BaseForm 对应的 JSON 表示
        """
        return {}

    def unmarshal(self, data):  # type: (Any) -> BaseForm
        """
        unmarshal 从 JSON 中解码数据，
        并将解码所得的数据置入本实例中

        Args:
            data (Any): 给定的 data 数据。
                        应确保它是一个字典

        Returns:
            BaseForm: 返回 BaseForm 本身
        """
        _ = data
        return self

    def all_codes(self):  # type: () -> list[StringWithHash]
        """
        all_codes 返回该 BaseForm 中存在的所有代码

        Returns:
            list[StringWithHash]:
                该 BaseForm 中存在的所有代码
        """
        return []
