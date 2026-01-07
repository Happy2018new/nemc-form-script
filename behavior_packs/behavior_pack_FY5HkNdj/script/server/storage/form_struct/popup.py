# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from ..base import BaseForm
from ..base import StringWithHash

EMPTY_STRING_WITH_HASH = StringWithHash()


class PopupForm(BaseForm):
    """PopupForm 是数据保存实现中的信息表单"""

    title = EMPTY_STRING_WITH_HASH
    content = EMPTY_STRING_WITH_HASH
    button1 = EMPTY_STRING_WITH_HASH
    button2 = EMPTY_STRING_WITH_HASH

    def __init__(
        self,
        title=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        content=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        button1=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        button2=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
    ):  # type: (...) -> None
        """
        初始化并返回一个新的 PopupForm

        Args:
            title (StringWithHash, optional):
                信息表单的标题文本。
                默认值为 EMPTY_STRING_WITH_HASH
            content (StringWithHash, optional):
                信息表单的内容文本。
                默认值为 EMPTY_STRING_WITH_HASH
            button1 (StringWithHash, optional):
                信息表单中代表“确定”按钮中，
                该按钮所显示的文本。
                默认值为 EMPTY_STRING_WITH_HASH
            button2 (StringWithHash, optional):
                信息表单中代表“取消”按钮中，
                该按钮所显示的文本。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.title = title
        self.content = content
        self.button1 = button1
        self.button2 = button2

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将该 PopupForm 编码为对应的 JSON 表示

        Returns:
            dict[str, Any]: 该信息表单对应的 JSON 表示
        """
        return {
            "title": self.title.marshal(),
            "content": self.content.marshal(),
            "button1": self.button1.marshal(),
            "button2": self.button2.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> PopupForm
        """
        unmarshal 从 JSON 中解码数据，
        并将解码所得的数据置入本实例中

        Args:
            data (Any): 给定的 data 数据。
                        应确保它是一个字典

        Returns:
            LongForm: 返回 LongForm 本身
        """
        self.title = StringWithHash().unmarshal(data["title"])
        self.content = StringWithHash().unmarshal(data["content"])
        self.button1 = StringWithHash().unmarshal(data["button1"])
        self.button2 = StringWithHash().unmarshal(data["button2"])
        return self

    def all_codes(self):  # type: () -> list[StringWithHash]
        """
        all_codes 返回该 PopupForm 中存在的所有代码

        Returns:
            list[StringWithHash]:
                该 PopupForm 中存在的所有代码
        """
        return [self.title, self.content, self.button1, self.button2]
