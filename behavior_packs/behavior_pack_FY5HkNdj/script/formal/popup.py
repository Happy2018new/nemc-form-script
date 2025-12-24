# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from .base import BaseForm


class PopupForm(BaseForm):
    """PopupForm 是信息表单的形式化表示"""

    title = ""
    content = ""
    button1 = ""
    button2 = ""

    def __init__(
        self, title="", content="", button1="", button2=""
    ):  # type: (str, str, str, str) -> None
        """
        初始化并返回一个新的形
        式化的信息（消息）表单

        Args:
            title (str, optional):
                信息表单的标题文本。
                默认值为空字符串
            content (str, optional):
                信息表单的内容文本。
                默认值为空字符串
            button1 (str, optional):
                信息表单中代表“确定”按钮中，
                该按钮所显示的文本。
                默认值为空字符串
            button2 (str, optional):
                信息表单中代表“取消”按钮中，
                该按钮所显示的文本。
                默认值为空字符串
        """
        self.title = title
        self.content = content
        self.button1 = button1
        self.button2 = button2

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将形式化的信息表单编码为对应的 JSON 表示

        Returns:
            dict[str, Any]: 该信息表单对应的 JSON 表示
        """
        return {
            "title": self.title,
            "content": self.content,
            "button1": self.button1,
            "button2": self.button2,
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
        self.title = ""
        self.content = ""
        self.button1 = ""
        self.button2 = ""
        if not isinstance(data, dict):
            return self

        title = data.get("title", "")
        content = data.get("content", "")
        button1 = data.get("button1", "")
        button2 = data.get("button2", "")

        if isinstance(title, str):
            self.title = title
        if isinstance(content, str):
            self.content = content
        if isinstance(button1, str):
            self.button1 = button1
        if isinstance(button2, str):
            self.button2 = button2
        return self
