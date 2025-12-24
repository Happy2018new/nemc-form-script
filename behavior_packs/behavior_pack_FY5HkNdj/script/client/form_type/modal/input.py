# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import (
        BaseUIControl,
        LabelUIControl,
        TextEditBoxUIControl,
    )

import uuid
from ..base import BaseComponent


class Input(BaseComponent):
    """Input 是输入框实现"""

    _should_update_screen = False
    _last_render_label = ""
    _last_render_place_holder = ""

    def __init__(self, ui_node, control):  # type: (ScreenNode, BaseUIControl) -> None
        """初始化并返回一个新的 输入框 实例

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将该组件挂接在哪个父节点下
        """
        self.ui_node = ui_node
        self.control = ui_node.CreateChildControl(
            "modal_component.custom_input",
            "input-" + str(uuid.uuid4()),
            control,
            False,
        )
        self._should_update_screen = False
        self._last_render_label = ""
        self._last_render_place_holder = ""

    def _get_label_control(self):  # type: () -> LabelUIControl | None
        """_get_label_control 获取输入框中标题文本对应的控件

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
            return None
        return child.asLabel()

    def _get_edit_box_control(self):  # type: () -> TextEditBoxUIControl | None
        """_get_edit_box_control 获取输入框中输入栏对应的控件

        Returns:
            TextEditBoxUIControl | None:
                如果成功，则返回对应的 TextEditBoxUIControl 实例；
                否则失败，那么返回 None
        """
        if self.control is None:
            return None
        child = self.control.GetChildByName(
            "/option_generic_core/two_line_layout"
            + "/settings_common.option_text_edit_control"
        )
        if child is None:
            return None
        return child.asTextEditBox()

    def _get_place_holder_control(self):  # type: () -> LabelUIControl | None
        """_get_place_holder_control 获取输入框中提示文本对应的控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 LabelUIControl 实例；
                否则失败，那么返回 None
        """
        edit_box = self._get_edit_box_control()
        if edit_box is None:
            return None
        control = edit_box.GetChildByPath(
            "/centering_panel/clipper_panel/visibility_panel/place_holder_control"
        )
        if control is None:
            return None
        return control.asLabel()

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

        label_text = self.get_label_text()
        if label_text is None:
            return False
        place_holder = self.get_place_holder_text()
        if place_holder is None:
            return False

        if self._last_render_label != label_text:
            self._last_render_label = label_text
            should_update = True
        if self._last_render_place_holder != place_holder:
            self._last_render_place_holder = place_holder
            should_update = True

        return should_update

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None or self.control is None:
            return
        _ = self.ui_node.RemoveChildControl(self.control)

    def get_label_text(self):  # type: () -> str | None
        """get_label_text 获取输入框的标题文本

        Returns:
            str | None: 如果成功，则返回输入框的标题文本；
                        否则失败，那么返回 None
        """
        control = self._get_label_control()
        if control is None:
            return None
        return control.GetText()

    def get_place_holder_text(self):  # type: () -> str | None
        """get_place_holder_text 获取输入框提示栏显示的文本

        Returns:
            str | None: 如果成功，则返回输入框提示栏显示的文本；
                        否则失败，那么返回 None
        """
        control = self._get_place_holder_control()
        if control is None:
            return None
        return control.GetText()

    def get_edit_text(self):  # type: () -> str | None
        """get_edit_text 获取输入框中输入的文本

        Returns:
            str | None: 如果成功，则返回输入栏中的文本；
                        否则失败，那么返回 None
        """
        control = self._get_edit_box_control()
        if control is None:
            return None
        return control.GetEditText()

    def set_label_text(self, label):  # type: (str) -> Input
        """set_label_text 设置输入框的标题文本

        Args:
            text (str): 欲设置的标题文本

        Returns:
            Input: 返回 Input 本身
        """
        control = self._get_label_control()
        if control is not None:
            control.SetText(label)
        return self

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
        return self

    def set_edit_text(self, text):  # type: (str) -> Input
        """set_edit_text 设置输入框中用户的输入内容

        Args:
            text (str): 欲设置的用户输入内容

        Returns:
            Input: 返回 Input 本身
        """
        control = self._get_edit_box_control()
        if control is not None:
            control.SetEditText(text)
            self._should_update_screen = True
        return self
