# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import (
        BaseUIControl,
        ButtonUIControl,
        LabelUIControl,
    )

import uuid
from ..base import BaseComponent, BaseForm
from ...utils import get_scroll_view_content
from mod.client.extraClientApi import PopScreen


DYNAMIC_BUTTON_IMAGE_TYPE_TEXTURE = 0
DYNAMIC_BUTTON_IMAGE_TYPE_URL = 1


class DynamicButton(BaseComponent):
    """DynamicButton 是长表单中的单个按钮"""

    button_image_type = 0
    _should_update_screen = False
    _last_render_label = ""
    _last_image_view_state = False
    _last_image_load_state = False
    _last_render_image_path = ""

    def __init__(self, ui_node, control):  # type: (ScreenNode, BaseUIControl) -> None
        """初始化并返回一个新的，可以附加在长表单中的按钮

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将该组件挂接在哪个父节点下
        """
        self.ui_node = ui_node
        self.control = ui_node.CreateChildControl(
            "long.dynamic_button",
            "dynamic_button-" + str(uuid.uuid4()),
            control,
            False,
        )
        self.button_image_type = DYNAMIC_BUTTON_IMAGE_TYPE_TEXTURE
        self._should_update_screen = False
        self._last_render_label = ""
        self._last_image_view_state = True
        self._last_image_load_state = True
        self._last_render_image_path = ""

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
        return should_update

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None or self.control is None:
            return
        self.ui_node.RemoveChildControl(self.control)

    def get_button_control(self):  # type: () -> ButtonUIControl | None
        """get_button_control 获取按钮所对应的控件

        Returns:
            ButtonUIControl | None:
                如果成功，则返回对应的 ButtonUIControl 实例；
                否则失败，那么返回 None
        """
        if self.control is None:
            return None
        button = self.control.GetChildByPath("/form_button")
        if button is None:
            return None
        return button.asButton()

    def get_button_text(self):  # type: () -> str
        """get_button_text 获取按钮当前显示的文本

        Returns:
            str: 按钮当前显示的文本
        """
        return self._last_render_label

    def button_image_is_visible(self):  # type: () -> bool
        """button_image_is_visible 检查按钮左方的图片是否可见

        Returns:
            bool: 按钮左方的图片是否可见
        """
        return self._last_image_view_state

    def button_image_is_loading(self):  # type: () -> bool
        """button_image_is_loading 检查按钮左方的图片是否仍在加载

        Returns:
            bool: 按钮左方的图片是否仍在加载
        """
        return self._last_image_load_state

    def get_button_image_path(self):  # type: () -> str
        """
        get_button_image_path 获取按钮左方图片所使用的贴图。
        如果该按钮使用的是 URL 图片，则它将返回对应的 URL

        Returns:
            _type_: _description_
        """
        return self._last_render_image_path

    def set_button_label(self, label):  # type: (str) -> DynamicButton
        """set_button_label 设置按钮要显示的文本

        Args:
            label (str): 欲该按钮显示的文本

        Returns:
            DynamicButton: 返回 DynamicButton 本身
        """
        if self._last_render_label == label:
            return self

        button = self.get_button_control()
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
            child.SetText(label)

        self._last_render_label = label
        self._should_update_screen = True
        return self

    def set_button_image_view_state(self, visible):  # type: (bool) -> DynamicButton
        """set_button_image_view_state 设置该按钮左方的图片是否可见

        Args:
            visible (bool):
                如果为 True，则该按钮左方的图片将可见；
                如果为 False，则该按钮左方的图片将不可见

        Returns:
            DynamicButton: 返回 DynamicButton 本身
        """
        if self.control is None:
            return self
        if self._last_image_view_state == visible:
            return self

        child = self.control.GetChildByPath("/panel_name")
        if child is None:
            return self
        child.SetVisible(visible)

        self._last_image_view_state = visible
        self._should_update_screen = True
        return self

    def set_button_image_load_state(self, loading):  # type: (bool) -> DynamicButton
        """set_button_image_load_state 设置该按钮左方的图片是否未加载完毕

        Args:
            loading (bool):
                如果为 True，则图片将被置于加载状态；
                如果为 False，则图片将被置于加载完成状态

        Returns:
            DynamicButton: 返回 DynamicButton 本身
        """
        if self.control is None:
            return self
        if self._last_image_load_state == loading:
            return self

        child = self.control.GetChildByPath("/panel_name/progress")
        if child is None:
            return self
        child.SetVisible(loading)

        self._last_image_load_state = loading
        self._should_update_screen = True
        return self

    def set_button_image(self, path):  # type: (str) -> DynamicButton
        """set_button_image 设置按钮左方图片所使用的本地贴图

        Args:
            path (str):
                本地贴图路径，如 "textures/ui/anvil_icon.png"。
                如果该按钮使用的是 URL 图片，则该函数不会执行任何操作

        Returns:
            DynamicButton: 返回 DynamicButton 本身
        """
        if self.control is None:
            return self
        if self.button_image_type == DYNAMIC_BUTTON_IMAGE_TYPE_URL:
            return self
        if self._last_render_image_path == path:
            return self

        image = self.control.GetChildByPath("/panel_name/image")
        if image is None:
            return self
        image = image.asImage()
        if image is None:
            return self
        image.SetSprite(path)

        self._last_render_image_path = path
        self._should_update_screen = True
        return self


class LongForm(BaseForm):
    """LongForm 是长表单实现"""

    _last_render_title_label = ""  # type: str
    _last_render_inside_label = ""  # type: str
    _callback = None  # type: Callable[[dict[str, Any], int], None] | None

    def __init__(
        self, ui_node, control, callback=None
    ):  # type: (ScreenNode, BaseUIControl, Callable[[dict[str, Any], int], None] | None) -> None
        """初始化并返回一个新的长表单

        Args:
            ui_node (ScreenNode): 该表单所在的屏幕结点
            control (BaseUIControl): 要将该表单挂接在哪个父节点下
            callback (Callable[[dict[str, Any], int], None] | None, optional):
                在用户点击长表单中的任何一个按钮时，执行的回调函数。
                回调函数的第二个参数，也即 int 参数指示按钮的索引。
                默认值为 None，指示不需要执行回调函数

        Raises:
            Exception: 如果 control 下已经挂接了一个长表单，
                       则将创建失败，对抛出对应的错误
        """
        if control.GetChildByName("long_form") is not None:
            raise Exception(
                "LongForm/__init__: LongForm already exists in the given control"
            )

        BaseForm.__init__(self, ui_node)
        self.control = ui_node.CreateChildControl(
            "long.long_form", "long_form", control, False
        )

        self._last_render_title_label = ""
        self._last_render_inside_label = ""
        self._callback = callback

    def _get_title_label_control(self):  # type: () -> LabelUIControl | None
        """_get_title_label_control 获取该长表单的标题文本所对应的控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 LabelUIControl 实例；
                否则失败，那么返回 None
        """
        if self.control is None:
            return None
        child = self.control.GetChildByPath("/title_label/common_dialogs_0")
        if child is None:
            return None
        return child.asLabel()

    def _get_long_form_content(self):  # type: () -> BaseUIControl | None
        """
        _get_long_form_content 获取该长表单的实际内容，
        因为其存放了长表单中的各个子组件

        Returns:
            BaseUIControl | None:
                如果成功，则返回对应的控件实例；
                如果失败，那么返回 None
        """
        if self.ui_node is None or self.control is None:
            return None
        return get_scroll_view_content(self.ui_node, self.control.GetPath())

    def _get_inside_label_control(self):  # type: () -> LabelUIControl | None
        """
        _get_inside_label_control 获取该长表单中，
        框内的标题文本，所对应的控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 LabelUIControl 实例；
                否则失败，那么返回 None
        """
        content = self._get_long_form_content()
        if content is None:
            return None
        child = content.GetChildByPath("/label_offset_panel/main_label")
        if child is None:
            return None
        return child.asLabel()

    def _get_buttons_control(self):  # type: () -> BaseUIControl | None
        """_get_buttons_control 获取该长表单中存放各个子按钮的控件

        Returns:
            BaseUIControl | None:
                如果成功，则返回对应的控件实例；
                如果失败，那么返回 None
        """
        content = self._get_long_form_content()
        if content is None:
            return None
        return content.GetChildByPath("/wrapping_panel/long_form_dynamic_buttons_panel")

    def _register_callback(self, button):  # type: (DynamicButton) -> None
        """
        _register_callback 为 button 注册回调函数。
        该回调函数将在该 button 被用户点击然后弹起时调用。

        应须确保在 _register_callback 调用后，
        再将 button 追加到 self.childs 中

        Args:
            button (DynamicButton): 该 button 所指示的子按钮组件
        """
        control = button.get_button_control()
        if control is None:
            return
        index = len(self.childs)

        def _on_button_trigger(args):  # type: (dict[str, Any]) -> None
            """
            _on_button_trigger 是底层的回调函数。
            该函数会在 button 被点击然后弹起后调用。

            index 是所引用的闭包变量之一，
            外围调用者需要保证它是正确的

            Args:
                args (dict[str, Any]):
                    SetButtonTouchUpCallback 传入的字典参数
            """
            if self._callback is not None:
                try:
                    self._callback(args, index)
                except Exception:
                    pass
            PopScreen()

        control.AddTouchEventParams({"isSwallow": True})
        control.SetButtonTouchUpCallback(_on_button_trigger)  # type: ignore

    def get_title_label(self):  # type: () -> str
        """get_title_label 获取该长表单的标题文本

        Returns:
            str: 该长表单的标题文本
        """
        return self._last_render_title_label

    def get_inside_label(self):  # type: () -> str
        """get_inside_label 获取该长表单中，框内的标题文本

        Returns:
            str: 该长表单中，框内的标题文本
        """
        return self._last_render_inside_label

    def set_title_label(self, label):  # type: (str) -> LongForm
        """set_title_label 设置该长表单的标题文本

        Args:
            label (str): 欲设置的标题文本

        Returns:
            LongForm: 返回 LongForm 本身
        """
        if self._last_render_title_label == label:
            return self

        control = self._get_title_label_control()
        if control is None:
            return self
        control.SetText(label)

        self._last_render_title_label = label
        self._should_update_screen = True
        return self

    def set_inside_label(self, label):  # type: (str) -> LongForm
        """set_inside_label 设置该长表单中，框内的标题文本

        Args:
            label (str): 欲设置的标题文本

        Returns:
            LongForm: 返回 LongForm 本身
        """
        if self._last_render_inside_label == label:
            return self

        control = self._get_inside_label_control()
        if control is None:
            return self
        control.SetText(label)

        self._last_render_inside_label = label
        self._should_update_screen = True
        return self

    def push_button(
        self, label, image_path="", is_url=False
    ):  # type: (str, str, bool) -> DynamicButton | None
        """push_button 向长表单追加一个新的按钮

        Args:
            label (str): 该按钮所显示的文本
            image_path (str, optional):
                该按钮所使用的本地贴图路径。
                例如 "textures/ui/anvil_icon.png"。
                默认值为空字符串，指示不使用贴图
            is_url (bool, optional):
                该按钮所使用的图片是否是 URL 上的。
                由于网易限制，我们实际上无法发起 HTTP 请求，
                因此在将它设为 True 后，实际不会显示任何图片。
                默认值为 False，指示使用本地贴图

        Returns:
            DynamicButton | None: 如果成功，则返回追加的按钮；
                                  否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        control = self._get_buttons_control()
        if control is None:
            return None

        button = (
            DynamicButton(self.ui_node, control)
            .set_button_label(label)
            .set_button_image_load_state(False)
        )
        if is_url:
            button.button_image_type = DYNAMIC_BUTTON_IMAGE_TYPE_URL
            button.set_button_image_view_state(False)
        else:
            if len(image_path) > 0:
                button.set_button_image_view_state(True)
                button.set_button_image(image_path)
            else:
                button.set_button_image_view_state(False)
        self._register_callback(button)

        self.childs.append(button)
        self._should_update_screen = True
        return button
