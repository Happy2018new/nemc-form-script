# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl, LabelUIControl

import uuid
from .basic import OptionGenericCore


class Input(OptionGenericCore):
    """Input 是输入框实现"""

    def __init__(
        self, ui_node, control, background, tooltip
    ):  # type: (ScreenNode, BaseUIControl, BaseUIControl, str) -> None
        """初始化并返回一个新的 输入框 实例

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将该组件挂接在哪个父节点下
            background (BaseUIControl): 该组件所在模态表单的背景控件
            tooltip (str): 该组件的灯泡提示文本
        """
        def_name = "modal_component.custom_input"
        if len(tooltip) > 0:
            def_name = "modal_component.custom_tooltip_input"

        OptionGenericCore.__init__(
            self,
            ui_node,
            ui_node.CreateChildControl(
                def_name,
                "input-" + str(uuid.uuid4()),
                control,
                False,
            ),
            background,
            "settings_common.option_text_edit_control",
        )

        if len(tooltip) > 0:
            _ = self.set_tooltip_text(tooltip)

    def _get_place_holder_control(self):  # type: () -> LabelUIControl | None
        """_get_place_holder_control 获取输入框中提示文本对应的控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 LabelUIControl 实例；
                否则失败，那么返回 None
        """
        control = self.get_current_control()
        if control is None:
            return None
        control = control.GetChildByPath(
            "/centering_panel/clipper_panel/visibility_panel/place_holder_control"
        )
        if control is None:
            return None
        return control.asLabel()

    def get_place_holder_text(self):  # type: () -> str | None
        """
        get_place_holder_text 获取输入框提示栏显示的文本

        Returns:
            str | None:
                如果成功，则返回输入框提示栏显示的文本；
                否则失败，那么返回 None
        """
        control = self._get_place_holder_control()
        if control is None:
            return None
        return control.GetText()

    def get_edit_text(self):  # type: () -> str | None
        """get_edit_text 获取输入框中输入的文本

        Returns:
            str | None:
                如果成功，则返回输入栏中的文本；
                否则失败，那么返回 None
        """
        control = self.get_current_control()
        if control is None:
            return None
        control = control.asTextEditBox()
        if control is None:
            return None
        return control.GetEditText()

    def set_place_holder_text(self, text):  # type: (str) -> Input
        """set_place_holder_text 设置输入框的提示文本

        Args:
            text (str): 欲设置的提示文本

        Returns:
            Input: 返回 Input 本身
        """
        control = self._get_place_holder_control()
        if control is not None:
            control.SetText(text)
            self._should_update_screen = True
        return self

    def set_edit_text(self, text):  # type: (str) -> Input
        """set_edit_text 设置输入框中用户的输入内容

        Args:
            text (str): 欲设置的用户输入内容

        Returns:
            Input: 返回 Input 本身
        """
        control = self.get_current_control()
        if control is None:
            return self

        control = control.asTextEditBox()
        if control is None:
            return self

        control.SetEditText(text)
        self._should_update_screen = True
        return self
