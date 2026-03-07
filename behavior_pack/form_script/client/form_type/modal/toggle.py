# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import (
        BaseUIControl,
        LabelUIControl,
        SwitchToggleUIControl,
    )

import uuid
from ..base import BaseComponent


class Toggle(BaseComponent):
    """Toggle 是开关实现"""

    _should_update_screen = False
    _last_render_label = ""

    def __init__(self, ui_node, control):  # type: (ScreenNode, BaseUIControl) -> None
        """初始化并返回一个新的 开关 实例

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将该组件挂接在哪个父节点下
        """
        self.ui_node = ui_node
        self.control = ui_node.CreateChildControl(
            "modal_component.custom_toggle",
            "toggle-" + str(uuid.uuid4()),
            control,
            False,
        )
        self._should_update_screen = False
        self._last_render_label = ""

    def _get_label_control(self):  # type: () -> LabelUIControl | None
        """_get_label_control 获取开关中标题文本对应的控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 LabelUIControl 实例；
                否则失败，那么返回 None
        """
        if self.control is None:
            return None

        child = self.control.GetChildByPath(
            "/option_generic_core/two_line_layout/option_label_panel/option_label"
        )
        if child is None:
            child = self.control.GetChildByPath(
                "/option_generic_core/one_line_layout/option_label"
            )
        if child is None:
            return None

        return child.asLabel()

    def _get_toggle_control(self):  # type: () -> SwitchToggleUIControl | None
        """_get_toggle_control 获取开关本身对应的控件

        Returns:
            SwitchToggleUIControl | None:
                如果成功，则返回对应的 SwitchToggleUIControl 实例；
                否则失败，那么返回 None
        """
        if self.control is None:
            return None

        child = self.control.GetChildByPath(
            "/option_generic_core/one_line_layout"
            + "/settings_common.option_toggle_control"
        )
        if child is None:
            child = self.control.GetChildByPath(
                "/option_generic_core/two_line_layout"
                + "/settings_common.option_toggle_control"
            )
        if child is None:
            return None

        return child.asSwitchToggle()

    def on_update_screen(self):  # type: () -> bool
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Returns:
            bool: 指示是否需要刷新屏幕
        """
        should_update = self._should_update_screen
        if self._should_update_screen:
            self._should_update_screen = False

        label = self.get_toggle_label()
        if label is None:
            return False
        if self._last_render_label != label:
            self._last_render_label = label
            should_update = True

        return should_update

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None or self.control is None:
            return
        _ = self.ui_node.RemoveChildControl(self.control)

    def get_toggle_label(self):  # type: () -> str | None
        """get_toggle_label 获取开关的标题文本

        Returns:
            str | None: 如果成功，则返回开关的标题文本；
                        否则失败，那么返回 None
        """
        control = self._get_label_control()
        if control is None:
            return None
        return control.GetText()

    def get_toggle_state(self):  # type: () -> bool | None
        """get_toggle_state 获取开关的状态

        Returns:
            bool | None:
                返回 True 如果开关处于打开状态；
                返回 False 如果开关处于关闭状态；
                否则，获取开关状态失败，那么返回 None
        """
        control = self._get_toggle_control()
        if control is None:
            return None
        return control.GetToggleState("")

    def set_toggle_label(self, label):  # type: (str) -> Toggle
        """set_toggle_label 设置开关的标题文本

        Args:
            label (str): 欲设置的标题文本

        Returns:
            Toggle: 返回 Toggle 本身
        """
        control = self._get_label_control()
        if control is not None:
            control.SetText(label)
        return self

    def set_toggle_state(self, state):  # type: (bool) -> Toggle
        """set_toggle_state 设置开关的状态

        Args:
            state (bool): True 如果开关需要打开；
                          False 如果开关需要关闭

        Returns:
            Toggle: 返回 Toggle 本身
        """
        control = self._get_toggle_control()
        if control is not None:
            control.SetToggleState(state, "")
            self._should_update_screen = True
        return self
