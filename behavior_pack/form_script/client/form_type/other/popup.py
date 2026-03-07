# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import (
        BaseUIControl,
        LabelUIControl,
        ButtonUIControl,
    )

from ..base import BaseForm
from ...utils import get_scroll_view_content
from mod.client.extraClientApi import PopScreen


class PopupForm(BaseForm):
    """PopupForm 描述一个信息表单"""

    _last_render_title = ""  # type: str
    _last_render_text = ""  # type: str
    _last_render_button = ["", ""]  # type: list[str]
    _callback = None  # type: Callable[[dict[str, Any], bool], None] | None

    def __init__(
        self, ui_node, control, callback=None
    ):  # type: (ScreenNode, BaseUIControl, Callable[[dict[str, Any], bool], None] | None) -> None
        """
        初始化并返回一个新的信息表单。

        另，对于 callback 参数：
            - 该函数的第一个参数是事件 SetButtonTouchUpCallback 的参数
            - 该函数的第二个参数，也即 bool 参数，用于指示用户点击的按钮是否代表“确定”

        Args:
            ui_node (ScreenNode): 该表单所在的屏幕结点
            control (BaseUIControl): 要将该表单挂接在哪个父节点下
            callback (Callable[[dict[str, Any], bool], None] | None, optional):
                当用户点击代表“确定”或代表“取消”按钮时，应当执行的回调函数。
                默认值为 None，指示不需要执行回调函数

        Raises:
            Exception: 如果 control 下已经挂接了一个信息表单，
                       则将创建失败，对抛出对应的错误
        """
        if control.GetChildByName("modal_dialog_popup") is not None:
            raise Exception(
                "PopupForm/__init__: PopupForm already exists in the given control"
            )

        BaseForm.__init__(self, ui_node)
        self.control = ui_node.CreateChildControl(
            "popup.modal_dialog_popup", "modal_dialog_popup", control, False
        )

        self._last_render_title = ""
        self._last_render_text = ""
        self._last_render_button = ["", ""]

        self._callback = callback
        self._init_button_callback(False)
        self._init_button_callback(True)

    def _init_button_callback(self, is_left_button=True):  # type: (bool) -> None
        """
        _init_button_callback 为信息表单中的确定或取消按钮注册对应的回调函数。
        当用户点击其中任何一个按钮，然后按钮弹起后，底层回调函数将会被执行

        Args:
            is_left_button (bool, optional):
                指示被注册的按钮是否代表“确定”。
                默认值为 True，代表该按钮代表“确定”
        """
        button = self._get_button_control(is_left_button)
        if button is None:
            return

        def _on_button_trigger(args):
            if self._callback is not None:
                try:
                    self._callback(args, is_left_button)
                except Exception:
                    pass
            PopScreen()

        button.AddTouchEventParams({"isSwallow": True})
        button.SetButtonTouchUpCallback(_on_button_trigger)  # type: ignore

    def _get_popup_content(self):  # type: () -> BaseUIControl | None
        """_get_popup_content 获取该信息表单中存放实际内容的控件

        Returns:
            BaseUIControl | None:
                如果成功，则返回对应的 BaseUIControl 实例；
                否则失败，那么返回 None
        """
        if self.control is None:
            return None
        return self.control.GetChildByPath("/modal_input/modal_bg_buttons")

    def _get_title_control(self):  # type: () -> LabelUIControl | None
        """_get_title_control 获取该信息表单中标题文本所对应的控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 LabelUIControl 实例；
                否则失败，那么返回 None
        """
        control = self._get_popup_content()
        if control is None:
            return None
        child = control.GetChildByPath("/title")
        if child is None:
            return None
        return child.asLabel()

    def _get_text_control(self):  # type: () -> LabelUIControl | None
        """_get_text_control 获取该信息表单中所显示文本内容对应的控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 LabelUIControl 实例；
                否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        content = self._get_popup_content()
        if content is None:
            return None

        control = get_scroll_view_content(self.ui_node, content.GetPath() + "/text")
        if control is None:
            return None

        child = control.GetChildByPath("/text")
        if child is None:
            return None
        return child.asLabel()

    def _get_button_control(
        self, is_left_button=True
    ):  # type: (bool) -> ButtonUIControl | None
        """_get_button_control 返回该信息表单中确定或取消按钮的控件

        Args:
            is_left_button (bool, optional):
                指示要获取的按钮是否是代表“确定”的按钮。
                默认值为 True，代表要获取的按钮代表“确定”

        Returns:
            ButtonUIControl | None:
                如果成功，则返回对应的 ButtonUIControl 实例；
                否则失败，那么返回 None
        """
        content = self._get_popup_content()
        if content is None:
            return None

        child = None
        if is_left_button:
            child = content.GetChildByPath("/button_panel/left")
        else:
            child = content.GetChildByPath("/button_panel/right")

        if child is None:
            return
        return child.asButton()

    def get_popup_title(self):  # type: () -> str
        """get_popup_title 获取该信息表单的标题文本

        Returns:
            str: 该信息表单的标题文本
        """
        return self._last_render_title

    def get_popup_text(self):  # type: () -> str
        """get_popup_text 获取该信息表单所显示的实际文字内容

        Returns:
            str: 该信息表单所显示的实际文字内容
        """
        return self._last_render_text

    def get_button_text(self, is_left_button=True):  # type: (bool) -> str
        """
        get_button_text 获取该信息表单中，
        确定或取消按钮所显示的文本

        Args:
            is_left_button (bool, optional):
                指示目标按钮是否代表“确定”。
                默认值为 True，代表目标按钮代表“确定”

        Returns:
            str: 目标按钮所显示的文本
        """
        if is_left_button:
            return self._last_render_button[0]
        else:
            return self._last_render_button[1]

    def set_popup_title(self, title):  # type: (str) -> PopupForm
        """set_popup_title 设置该信息表单的标题文本

        Args:
            title (str): 欲设置的标题文本

        Returns:
            PopupForm: 返回 PopupForm 本身
        """
        if self._last_render_title == title:
            return self

        control = self._get_title_control()
        if control is None:
            return self
        control.SetText(title)

        self._last_render_title = title
        self._should_update_screen = True
        return self

    def set_popup_text(self, text):  # type: (str) -> PopupForm
        """set_popup_text 设置该信息表单所显示的实际文字内容

        Args:
            text (str): 欲设置的实际文字内容

        Returns:
            PopupForm: 返回 PopupForm 本身
        """
        if self._last_render_text == text:
            return self

        control = self._get_text_control()
        if control is None:
            return self
        control.SetText(text)

        self._last_render_text = text
        self._should_update_screen = True
        return self

    def set_button_text(
        self, text, is_left_button=True
    ):  # type: (str, bool) -> PopupForm
        """
        set_button_text 设置该信息表单中，
        确定或取消按钮所显示的文本

        Args:
            text (str): 欲对应按钮显示的文本
            is_left_button (bool, optional):
                被修改的按钮是否代表“确定”。
                默认值为 True，代表被修改的按钮代表“确定”

        Returns:
            PopupForm: 返回 PopupForm 本身
        """
        if is_left_button:
            if self._last_render_button[0] == text:
                return self
        else:
            if self._last_render_button[1] == text:
                return self

        button = self._get_button_control(is_left_button)
        if button is None:
            return self
        for i in ["default", "hover", "pressed", "locked"]:
            child = button.GetChildByPath(
                "/" + i + "/button_content/common_buttons.new_ui_binding_button_label"
            )
            if child is None:
                continue
            child = child.asLabel()
            if child is None:
                continue
            child.SetText(text)

        if is_left_button:
            self._last_render_button[0] = text
        else:
            self._last_render_button[1] = text
        self._should_update_screen = True
        return self
