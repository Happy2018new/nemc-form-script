# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl, ButtonUIControl

from .label import Label
from .toggle import Toggle
from .input import Input
from .dropdown import DropDown
from .slider import Slider, StepSlider
from ..base import BaseForm
from ...utils import get_scroll_view_content
from mod.client.extraClientApi import PopScreen


class ModalForm(BaseForm):
    """ModalForm 表示一个模态表单"""

    _submit_button_inited = False  # type: bool
    _submit_button_callback = None  # type: Callable[[dict[str, Any]], None] | None
    _last_render_label = ""  # type: str
    _last_render_submit_button = ""  # type: str

    def __init__(
        self, ui_node, control, callback=None
    ):  # type: (ScreenNode, BaseUIControl, Callable[[dict[str, Any]], None] | None) -> None
        """初始化并返回一个新的模态表单

        Args:
            ui_node (ScreenNode): 该表单所在的屏幕结点
            control (BaseUIControl): 要将该表单挂接在哪个父节点下
            callback (Callable[[dict[str, Any]], None] | None, optional):
                当用户点击提交按钮时，应当执行的回调函数。
                默认值为 None，指示不需要执行回调函数
        Raises:
            Exception: 如果 control 下已经挂接了一个模态表单，
                       则将创建失败，对抛出对应的错误
        """
        if control.GetChildByName("custom_form") is not None:
            raise Exception(
                "ModalForm/__init__: ModalForm already exists in the given control"
            )

        BaseForm.__init__(self, ui_node)
        self.control = ui_node.CreateChildControl(
            "modal.custom_form", "custom_form", control, False
        )
        self._last_render_label = ""
        self._last_render_submit_button = ""

        self._submit_button_inited = False
        self._submit_button_callback = callback
        self._init_submit_callback()

    def _get_submit_button_control(self):  # type: () -> ButtonUIControl | None
        """_get_submit_button_control 获取提交按钮对应的控件

        Returns:
            ButtonUIControl | None:
                如果成功，则返回对应的 ButtonUIControl 实例；
                否则失败，那么返回 None
        """
        if self.ui_node is None or self.control is None:
            return None

        control = get_scroll_view_content(self.ui_node, self.control.GetPath())
        if control is None:
            return None
        button = control.GetChildByPath("/submit_button")
        if button is None:
            return None

        return button.asButton()

    def _init_submit_visual(self):  # type: () -> None
        """
        _init_submit_visual 将提交按钮的显示状态设置为默认状态。
        这用于解决在模态表单被创建后，提交按钮默认为绿色的问题
        """
        button = self._get_submit_button_control()
        if button is None:
            return
        for i in ["default", "hover", "pressed", "locked"]:
            child = button.GetChildByPath("/" + i)
            if child is None:
                continue
            child.SetVisible(i == "default")

    def _init_submit_callback(self):  # type: () -> None
        """
        _init_submit_callback 为提交按钮
        启用按下后回调的功能，
        并注册对应的回调函数
        """
        button = self._get_submit_button_control()
        if button is None:
            return
        button.AddTouchEventParams({"isSwallow": True})
        button.SetButtonTouchUpCallback(self._on_trigger_submit_button)  # type: ignore

    def _on_trigger_submit_button(self, args):  # type: (dict[str, Any]) -> None
        """
        _on_trigger_submit_button 是模态表单中“提交”按钮被点击时，
        将被实际执行的回调函数。它在安全的上下文中执行用户提供的函数，
        并在完成后弹出当前的模态表单 UI

        Args:
            args (dict[str, Any]):
                SetButtonTouchUpCallback 传入的字典参数
        """
        if self._submit_button_callback is not None:
            try:
                self._submit_button_callback(args)
            except Exception:
                pass
        PopScreen()

    def _get_generated_form(self):  # type: () -> BaseUIControl | None
        """
        _get_generated_form 获取该模态表单的 generated_form，
        因为 generated_form 存放了模态表单中的各个子组件

        Returns:
            BaseUIControl | None:
                generated_form 所对应的基础控件实例。
                如果获取失败，则返回 None
        """
        if self.ui_node is None or self.control is None:
            return None

        control = get_scroll_view_content(self.ui_node, self.control.GetPath())
        if control is None:
            return None

        return control.GetChildByPath("/generated_form")

    def on_update_screen(self):  # type: () -> bool
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Returns:
            bool: 指示是否需要刷新屏幕
        """
        should_update = BaseForm.on_update_screen(self)
        if not self._submit_button_inited:
            self._submit_button_inited = True
            self._init_submit_visual()
            should_update = True
        return should_update

    def set_modal_label(self, label):  # type: (str) -> ModalForm
        """set_modal_label 设置模态表单的标题

        Args:
            label (str): 要设置的标题

        Returns:
            ModalForm: 返回 ModalForm 本身
        """
        if self._last_render_label == label:
            return self
        else:
            self._last_render_label = label
            self._should_update_screen = True

        if self.control is None:
            return self
        child = self.control.GetChildByPath("/title_label/common_dialogs_0")
        if child is None:
            return self

        child = child.asLabel()
        if child is None:
            return self
        child.SetText(label)
        return self

    def set_modal_submit_button(self, text="提交"):  # type: (str) -> ModalForm
        """set_modal_submit_button 设置模态表单中提交按钮的文本

        Args:
            text (str, optional): 提交按钮的文本。
                                  默认为“提交”

        Returns:
            ModalForm: 返回 ModalForm 本身
        """
        if self._last_render_submit_button == text:
            return self
        else:
            self._last_render_submit_button = text
            self._should_update_screen = True

        button = self._get_submit_button_control()
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

        return self

    def push_slider(
        self, label, contents, index=-1
    ):  # type: (str, list[str], int) -> Slider | None
        """push_slider 向模态表单追加一个隐式步进滑块

        Args:
            label (str): 该滑块的标题
            contents (list[str]): 该滑块可以选择的内容
            index (int, optional): 该滑块最开始的位置。
                                   不使用请置为 -1

        Returns:
            Slider | None: 如果成功，则返回追加的滑块；
                           否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        control = self._get_generated_form()
        if control is None:
            return None

        slider = (
            Slider(self.ui_node, control)
            .set_slider_label(label)
            .set_slider_contents(contents, index)
        )
        self.childs.append(slider)
        self._should_update_screen = True
        return slider

    def push_step_slider(
        self, label, contents, index=-1
    ):  # type: (str, list[str], int) -> StepSlider | None
        """push_step_slider 向模态表单追加一个显式步进滑块

        Args:
            label (str): 该滑块的标题
            contents (list[str]): 该滑块可以选择的内容
            index (int, optional): 该滑块最开始的位置。
                                   不使用请置为 -1

        Returns:
            StepSlider | None: 如果成功，则返回追加的滑块；
                               否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        control = self._get_generated_form()
        if control is None:
            return None

        step_slider = StepSlider(self.ui_node, control)
        step_slider.set_slider_label(label)
        step_slider.set_slider_contents(contents, index)

        self.childs.append(step_slider)
        self._should_update_screen = True
        return step_slider

    def push_dropdown(
        self, label, contents, index=-1
    ):  # type: (str, list[str], int) -> DropDown | None
        """push_dropdown 向模态表单追加一个下拉框

        Args:
            label (str): 该下拉框的标题
            contents (list[str]): 该下拉框的可选择内容
            index (int, optional): 该下拉框在一开始所选择的内容。
                                   如果不使用该字段，请置为 -1

        Returns:
            DropDown | None: 如果成功，则返回追加的下拉框；
                             否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        control = self._get_generated_form()
        if control is None:
            return None

        dropdown = DropDown(self.ui_node, control)
        for i in contents:
            dropdown.add_new_option(i)
        dropdown.set_dropdown_label(label)
        dropdown.set_selected_option(index if index != -1 else 0)

        self.childs.append(dropdown)
        self._should_update_screen = True
        return dropdown

    def push_label(self, label):  # type: (str) -> Label | None
        """push_label 向模态表单追加一个纯文本显示组件

        Args:
            label (str): 该组件要显示的纯文本

        Returns:
            Label | None: 如果成功，则返回追加的组件；
                          否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        control = self._get_generated_form()
        if control is None:
            return None

        result = Label(self.ui_node, control)
        result.set_label_text(label)

        self.childs.append(result)
        self._should_update_screen = True
        return result

    def push_toggle(self, label, toggled=False):  # type: (str, bool) -> Toggle | None
        """push_toggle 向模态表单追加一个开关

        Args:
            label (str): 开关的标题文本
            toggled (bool, optional):
                True 如果开关需要打开；
                False 如果开关需要关闭；
                默认值为 False

        Returns:
            Toggle | None: 如果成功，则返回追加的开关；
                           否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        control = self._get_generated_form()
        if control is None:
            return None

        toggle = (
            Toggle(self.ui_node, control)
            .set_toggle_label(label)
            .set_toggle_state(toggled)
        )
        self.childs.append(toggle)
        self._should_update_screen = True
        return toggle

    def push_input(
        self, label_text, place_holder_text="", edit_text=""
    ):  # type: (str, str, str) -> Input | None
        """push_input 向模态表单追加一个输入框

        Args:
            label_text (str): 输入框的标题文本
            place_holder_text (str, optional): 输入框的提示内容。
                                          默认为空字符串
            edit_text (str, optional): 输入框中用户输入的内容。
                                      默认为空字符串

        Returns:
            Input | None: 如果成功，则返回追加的输入框；
                          否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        control = self._get_generated_form()
        if control is None:
            return None

        panel = (
            Input(self.ui_node, control)
            .set_label_text(label_text)
            .set_place_holder_text(place_holder_text)
            .set_edit_text(edit_text)
        )
        self.childs.append(panel)
        self._should_update_screen = True
        return panel
