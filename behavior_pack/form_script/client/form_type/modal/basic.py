# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from mod.client.extraClientApi import ScreenNode
    from mod.client.component.actorMotionCompClient import ActorMotionComponentClient
    from mod.client.ui.controls.baseUIControl import (
        BaseUIControl,
        LabelUIControl,
        ImageUIControl,
    )

from mod.client.extraClientApi import GetEngineCompFactory, GetLocalPlayerId
from ..base import TRIGGER_TYPE_CLICK, BaseComponent
from ...utils import point_is_in_rect, rect_in_rect, input_mode_is_touch


class OptionGenericCore(BaseComponent):
    """
    OptionGenericCore 是模态表单中大多数元素的基类
    """

    background = None  # type: BaseUIControl | None
    _control_name = ""  # type: str
    _prefix_path = ""  # type: str
    _suffix_path = ""  # type: str
    _tooltip_text = ""  # type: str
    _actor_motion_comp = None  # type: ActorMotionComponentClient | None
    _should_update_screen = False  # type: bool

    def __init__(
        self, ui_node, control, background, control_name, prefix_path="", suffix_path=""
    ):  # type: (ScreenNode, BaseUIControl, BaseUIControl, str, str, str) -> None
        """初始化并返回一个新的 OptionGenericCore

        Args:
            ui_node (ScreenNode):
                该组件所在的屏幕结点
            control (BaseUIControl):
                该组件所在的控件结点
            background (BaseUIControl):
                该组件所在模态表单的背景控件
            control_name (str):
                该组件的 JSON UI Control 名称。
                例如 `settings_common.option_text_edit_control`
            prefix_path (str, optional):
                获取该组件各子控件所需的前置路径。
                默认值为空字符串
            suffix_path (str, optional):
                获取该组件各子控件所需的后置路径。
                默认值为空字符串
        """
        self.ui_node = ui_node
        self.control = control
        self.background = background
        self._control_name = control_name
        self._prefix_path = prefix_path
        self._suffix_path = suffix_path
        self._tooltip_text = ""
        self._actor_motion_comp = GetEngineCompFactory().CreateActorMotion(
            GetLocalPlayerId()
        )
        self._should_update_screen = False

    def _get_label_control(self):  # type: () -> LabelUIControl | None
        """_get_label_control 获取控制标题文本的控件

        Returns:
            LabelUIControl | None:
                如果成功，则返回对应的 LabelUIControl 实例；
                否则失败，那么返回 None
        """
        if self.control is None:
            return None

        child = self.control.GetChildByPath(
            self._prefix_path
            + "/option_generic_core/two_line_layout"
            + "/option_label_panel/option_label"
        )
        if child is None:
            child = self.control.GetChildByPath(
                self._prefix_path
                + "/option_generic_core/one_line_layout"
                + "/option_label"
            )
        if child is None:
            return None

        return child.asLabel()

    def _get_tooltip_control(self):  # type: () -> BaseUIControl | None
        """_get_tooltip_control 获取控制提示灯泡的控件

        Returns:
            BaseUIControl | None:
                如果成功，则返回对应的控件实例；
                如果失败，那么返回 None
        """
        if self.control is None:
            return None

        child = self.control.GetChildByPath(
            self._prefix_path
            + "/option_generic_core/two_line_layout"
            + "/option_label_panel/option_tooltip"
        )
        if child is not None:
            return child

        return self.control.GetChildByPath(
            "/option_generic_core/one_line_layout/option_tooltip"
        )

    def _get_tooltip_image(self):  # type: () -> ImageUIControl | None
        """
        _get_tooltip_image 获取提示灯泡对应的图片控件。

        特别地，如果该图片控件在获取时不可见，
        即便该控件存在，该函数也会返回 None

        Returns:
            ImageUIControl | None:
                如果成功，则返回对应的 ImageUIControl 实例；
                如果失败，那么返回 None
        """
        control = self._get_tooltip_control()
        if control is None:
            return None
        if not control.GetVisible():
            return None

        child = control.GetChildByPath(
            "/hover_detection_input_panel/option_generic_tooltip_image"
        )
        if child is None:
            return None

        return child.asImage()

    def _set_tooltip_visible(self, visible):  # type: (bool) -> OptionGenericCore
        """_set_tooltip_visible 设置该组件提示灯泡中提示文本的可见性

        Args:
            visible (bool): 提示灯泡中提示文本的可见性

        Returns:
            OptionGenericCore: 返回 OptionGenericCore 本身
        """
        if self.background is None:
            return self

        control = self._get_tooltip_control()
        if control is None:
            return self

        top_popup = control.GetChildByPath("/option_generic_tooltip_top_popup")
        if top_popup is None:
            return self
        top_popup = top_popup.asImage()
        if top_popup is None:
            return self
        bottom_popup = control.GetChildByPath("/option_generic_tooltip_bottom_popup")
        if bottom_popup is None:
            return self

        background = self.background.GetChildByPath("/background")
        if background is None:
            return self
        background = background.asImage()
        if background is None:
            return self

        origin = top_popup.GetVisible()
        _, _ = top_popup.SetVisible(True, False), background.SetVisible(True, False)
        rect1, rect2 = top_popup.GetRotateRect(), background.GetRotateRect()
        _, _ = top_popup.SetVisible(origin, False), background.SetVisible(False, False)

        if rect_in_rect(rect1, rect2):
            if top_popup.GetVisible() != visible:
                top_popup.SetVisible(visible, False)
                self._should_update_screen = True
            if bottom_popup.GetVisible() != False:
                bottom_popup.SetVisible(False, False)
                self._should_update_screen = True
        else:
            if top_popup.GetVisible() != False:
                top_popup.SetVisible(False, False)
                self._should_update_screen = True
            if bottom_popup.GetVisible() != visible:
                bottom_popup.SetVisible(visible, False)
                self._should_update_screen = True
        return self

    def on_update_screen(self):  # type: () -> bool
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Returns:
            bool: 指示是否需要刷新屏幕
        """
        if self._actor_motion_comp is None:
            return False

        should_update = self._should_update_screen
        if self._should_update_screen:
            self._should_update_screen = False

        if input_mode_is_touch():
            return should_update
        position = self._actor_motion_comp.GetMousePosition()
        if position is None:
            return should_update
        control = self._get_tooltip_image()
        if control is not None:
            _ = self._set_tooltip_visible(
                point_is_in_rect(control.GetRotateRect(), position)
            )

        return should_update

    def on_trigger_screen(
        self, is_touch, trigger_type, touch_pos
    ):  # type: (bool, int, tuple[float, float]) -> bool
        """on_trigger_screen 在用户点击屏幕时调用

        Args:
            is_touch (bool):
                指示用户本次点击屏幕时，
                是否是通过触摸屏点击的
            trigger_type (int):
                触发类型。可能的值及含义如下。
                    - TRIGGER_TYPE_CLICK: 用户点击屏幕
                    - TRIGGER_TYPE_RELEASE: 用户释放点击
            touch_pos (tuple[float, float]):
                用户点击的屏幕坐标

        Returns:
            bool:
                指示是否需要刷新屏幕。
                总是返回 False
        """
        _ = trigger_type
        if not is_touch:
            return False

        control = self._get_tooltip_image()
        if control is None:
            return False
        _ = self._set_tooltip_visible(
            point_is_in_rect(control.GetRotateRect(), touch_pos)
        )

        return False

    def get_current_control(self):  # type: () -> BaseUIControl | None
        """get_current_control 获取控制该组件的实际控件

        Returns:
            BaseUIControl | None:
                如果成功，则返回对应的控件实例；
                如果失败，那么返回 None
        """
        if self.control is None:
            return None

        path = "{}/option_generic_core/two_line_layout/{}{}".format(
            self._prefix_path, self._control_name, self._suffix_path
        )
        child = self.control.GetChildByPath(path)
        if child is not None:
            return child

        path = "{}/option_generic_core/one_line_layout/{}{}".format(
            self._prefix_path, self._control_name, self._suffix_path
        )
        return self.control.GetChildByPath(path)

    def get_title_label(self):  # type: () -> str | None
        """get_title_label 获取该组件的标题文本

        Returns:
            str | None: 如果成功，返回该组件的标题文本；
                        否则失败，那么返回 None
        """
        control = self._get_label_control()
        if control is None:
            return None
        return control.GetText()

    def get_tooltip_text(self):  # type: () -> str
        """
        get_tooltip_text 获取该组件中提示灯泡的文本

        Returns:
            str: 返回该组件中提示灯泡的文本
        """
        return self._tooltip_text

    def set_title_label(self, text):  # type: (str) -> OptionGenericCore
        """set_title_label 设置该组件的标题文本

        Args:
            text (str): 欲设置的标题文本

        Returns:
            OptionGenericCore: 返回 OptionGenericCore 本身
        """
        control = self._get_label_control()
        if control is None:
            return self

        control.SetText(text)
        self._should_update_screen = True

        return self

    def set_tooltip_text(self, text):  # type: (str) -> OptionGenericCore
        """set_tooltip_text 设置该组件中提示灯泡的文本

        Args:
            text (str): 欲提示灯泡显示的文本

        Returns:
            OptionGenericCore: 返回 OptionGenericCore 本身
        """
        control = self._get_tooltip_control()
        if control is None:
            return self

        top_popup = control.GetChildByPath(
            "/option_generic_tooltip_top_popup/image_and_text_stack_panel"
            + "/tooltip_text"
        )
        if top_popup is not None:
            top_popup = top_popup.asLabel()
            if top_popup is not None:
                top_popup.SetText(text)

        bottom_popup = control.GetChildByPath(
            "/option_generic_tooltip_bottom_popup/image_and_text_stack_panel"
            + "/tooltip_text"
        )
        if bottom_popup is not None:
            bottom_popup = bottom_popup.asLabel()
            if bottom_popup is not None:
                bottom_popup.SetText(text)

        self._tooltip_text = text
        self._should_update_screen = True
        return self
