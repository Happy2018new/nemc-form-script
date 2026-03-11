# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl, LabelUIControl

import uuid
from ..base import BaseComponent


class Label(BaseComponent):
    """Label 是纯文本显示实现"""

    _last_render_label = ""  # type: str

    def __init__(self, ui_node, control):  # type: (ScreenNode, BaseUIControl) -> None
        """初始化并返回一个新的 纯文本显示 实例

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将该组件挂接在哪个父节点下
        """
        self.ui_node = ui_node
        self.control = ui_node.CreateChildControl(
            "modal_component.custom_label",
            "label-" + str(uuid.uuid4()),
            control,
            False,
        )
        self._last_render_label = ""

    def _get_label_control(self):  # type: () -> LabelUIControl | None
        """_get_label_control 获取该组件对应的 Label 控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 Label 控件；
                否则失败，那么返回 None
        """
        if self.control is None:
            return None
        child = self.control.GetChildByPath("/text")
        if child is None:
            return None
        return child.asLabel()

    def on_update_screen(self):  # type: () -> bool
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Returns:
            bool: 指示是否需要刷新屏幕
        """
        if self.control is None:
            return False

        current_label = self.get_label_text()
        if current_label is None:
            return False

        if self._last_render_label != current_label:
            self._last_render_label = current_label
            return True
        return False

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None or self.control is None:
            return
        _ = self.ui_node.RemoveChildControl(self.control)

    def get_label_text(self):  # type: () -> str | None
        """get_label_text 获取该组件正显示的文本内容

        Returns:
            str | None: 如果成功，返回该组件正显示的文本内容；
                        否则失败，那么返回 None
        """
        control = self._get_label_control()
        if control is None:
            return None
        return control.GetText()

    def set_label_text(self, text):  # type: (str) -> Label
        """set_label_text 设置该组件显示的文本内容

        Args:
            text (str): 欲显示的文本内容

        Returns:
            Label: 返回 Label 本身
        """
        control = self._get_label_control()
        if control is not None:
            control.SetText(text)
        return self
