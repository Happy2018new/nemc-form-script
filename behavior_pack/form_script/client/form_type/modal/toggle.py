# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl

import uuid
from .base import OptionGenericCore


class Toggle(OptionGenericCore):
    """Toggle 是开关实现"""

    def __init__(
        self, ui_node, control, background, tooltip
    ):  # type: (ScreenNode, BaseUIControl, BaseUIControl, str) -> None
        """初始化并返回一个新的 开关 实例

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将该组件挂接在哪个父节点下
            background (BaseUIControl): 该组件所在模态表单的背景控件
            tooltip (str): 该组件的灯泡提示文本
        """
        def_name = "modal_component.custom_toggle"
        if len(tooltip) > 0:
            def_name = "modal_component.custom_tooltip_toggle"

        OptionGenericCore.__init__(
            self,
            ui_node,
            ui_node.CreateChildControl(
                def_name,
                "toggle-" + str(uuid.uuid4()),
                control,
                False,
            ),
            background,
            "settings_common.option_toggle_control",
        )

        if len(tooltip) > 0:
            _ = self.set_tooltip_text(tooltip)

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None or self.control is None:
            return
        _ = self.ui_node.RemoveChildControl(self.control)

    def get_toggle_state(self):  # type: () -> bool | None
        """get_toggle_state 获取开关的状态

        Returns:
            bool | None:
                返回 True 如果开关处于打开状态；
                返回 False 如果开关处于关闭状态；
                否则，获取开关状态失败，那么返回 None
        """
        control = self._get_current_control()
        if control is None:
            return None
        control = control.asSwitchToggle()
        if control is None:
            return None
        return control.GetToggleState("")

    def set_toggle_state(self, state):  # type: (bool) -> Toggle
        """set_toggle_state 设置开关的状态

        Args:
            state (bool): True 如果开关需要打开；
                          False 如果开关需要关闭

        Returns:
            Toggle: 返回 Toggle 本身
        """
        control = self._get_current_control()
        if control is None:
            return self
        control = control.asSwitchToggle()
        if control is not None:
            control.SetToggleState(state, "")
            self._should_update_screen = True
        return self
