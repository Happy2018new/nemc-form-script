# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl, ImageUIControl

import uuid
from ..base import (
    TRIGGER_TYPE_CLICK,
    TRIGGER_TYPE_RELEASE,
    KEY_PRESS_TYPE_DOWN,
    KEY_PRESS_TYPE_UP,
    BaseComponent,
)
from ...utils import (
    point_is_in_rect,
    input_mode_is_touch,
    check_esc_key,
    get_scorll_view_background,
    get_scroll_view_content,
)

ENUM_BUTTONS = [
    "unchecked",
    "checked",
    "unchecked_hover",
    "checked_hover",
    "unchecked_locked",
    "checked_locked",
    "unchecked_locked_hover",
    "checked_locked_hover",
]


class RadioWithLabel:
    """RadioWithLabel 是下拉框的单个子选项"""

    control = None  # type: BaseUIControl | None
    _can_toggled = False  # type: bool
    _toggle_label = ""  # type: str

    def __init__(
        self, ui_node, control, toggled, label
    ):  # type: (ScreenNode, BaseUIControl, bool, str) -> None
        """初始化并返回一个新的 下拉框子选项 实例

        Args:
            ui_node (ScreenNode): 子选项对应的屏幕节点
            control (BaseUIControl): 子选项要挂接在哪个夫节点下
            toggled (bool): 子选项当前是否已被选中
            label (str): 子选项所显示的文本内容
        """
        def_name = "modal_dropdown.radio_toggled"
        child_name = "radio_toggled"
        if not toggled:
            def_name = "modal_dropdown.custom_dropdown_radio"
            child_name = "radio_can_toggled"

        self.control = ui_node.CreateChildControl(
            def_name,
            child_name + "-" + str(uuid.uuid4()),
            control,
            False,
        )

        self._can_toggled = not toggled
        _ = self._set_radio_label(label)

    def _set_radio_label(self, label):  # type: (str) -> RadioWithLabel
        """_set_radio_label 设置当前子选项所显示的文本内容

        Args:
            label (str): 子选项需要显示的文本内容

        Returns:
            RadioWithLabel: 返回 RadioWithLabel 本身
        """
        if self.control is None:
            return self

        radio_label = self.control.GetChildByPath("/radio_with_label_core")
        if radio_label is None:
            return self

        for j in ENUM_BUTTONS:
            child = radio_label.GetChildByPath("/" + j + "/radio_label")
            if child is None:
                continue
            child = child.asLabel()
            if child is None:
                continue
            child.SetText(label)

        self._toggle_label = label
        return self

    def get_radio_label(self):  # type: () -> str
        """get_radio_label 返回子选项当前正在显示的文本内容

        Returns:
            str: 子选项当前正在显示的文本内容
        """
        return self._toggle_label

    def radio_can_toggled(self):  # type: () -> bool
        """
        radio_can_toggled 返回该子选项是否可
        以从未被选中的状态变更为已被选中的状态

        Returns:
            bool: 如果子选项已经被选中，则返回 False；
                  否则子选项具有变为被选中的可能，那么返回 True
        """
        return self._can_toggled

    def get_toggle_state(self):  # type: () -> bool
        """get_toggle_state 返回子选项是否已经被选中

        Returns:
            bool: 子选项当前是否已被选中
        """
        if self.control is None:
            return False

        radio_label = self.control.GetChildByName("/radio_with_label_core")
        if radio_label is None:
            return False

        raw_bag = radio_label.GetPropertyBag()  # type: Any
        property = raw_bag  # type: dict[str, Any]
        return property["#toggle_state"]

    def get_hover_state(self):  # type: () -> bool
        """get_hover_state 检查子选项当前是否处于鼠标悬停状态

        Returns:
            bool: 子选项当前是否处于鼠标悬停状态
        """
        if self.control is None:
            return False

        radio_label = self.control.GetChildByName("/radio_with_label_core")
        if radio_label is None:
            return False

        for i in ENUM_BUTTONS:
            if "hover" not in i:
                continue
            child = radio_label.GetChildByPath("/" + i)
            if child is None:
                continue
            if child.GetVisible():
                return True
        return False


class DropDown(BaseComponent):
    """DropDown 是下拉框实现"""

    dropdown = None  # type: BaseUIControl | None
    options = []  # type: list[RadioWithLabel]
    _should_update_screen = False  # type: bool
    _should_close_dropdown = False  # type: bool
    _last_click_pos = (0.0, 0.0)  # type: tuple[float, float]
    _last_select_index = 0  # type: int
    _last_render_label = ""  # type: str

    def __init__(self, ui_node, control):  # type: (ScreenNode, BaseUIControl) -> None
        """初始化并返回一个新的 下拉框 实例

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将下拉框挂接在哪个父节点下
        """
        self.ui_node = ui_node
        self.control = ui_node.CreateChildControl(
            "modal_dropdown.custom_dropdown",
            "dropdown_root-" + str(uuid.uuid4()),
            control,
            False,
        )

        child = self.control.GetChildByPath("/dropdown")
        if child is not None:
            _ = ui_node.RemoveChildControl(child)
        self.dropdown = ui_node.CreateChildControl(
            "modal_dropdown.custom_dropdown",
            "dropdown-" + str(uuid.uuid4()),
            self.control,
            False,
        )

        self.options = []
        self._should_update_screen = False
        self._should_close_dropdown = False
        self._last_click_pos = (0.0, 0.0)
        self._last_select_index = 0
        self._last_render_label = ""

    def _get_dropdown_control(self):  # type: () -> BaseUIControl | None
        """
        _get_dropdown_control 获取该组件
        所对应的下拉框 BaseUIControl 实例

        Returns:
            BaseUIControl | None: 如果获取成功，返回对应的 BaseUIControl 实例；
                                  否则获取失败，那么返回 None
        """
        if self.dropdown is None:
            return None
        return self.dropdown.GetChildByPath(
            "/dropdown/option_generic_core"
            + "/two_line_layout/settings_common.option_dropdown_control"
            + "/dropdown"
        )

    def _get_mouse_box(self):  # type: () -> ImageUIControl | None
        """
        _get_mouse_box 获取下拉框最右方的鼠标可拖动区域中，
        用于控制滚轮的底层图形。通过控制滚轮，可以使下拉框
        快速滚动，以显示不同的子选项

        Returns:
            ImageUIControl | None:
                如果当前用户输入模式是鼠标，那么试图获取目标底层图形。
                若获取失败，或用户输入模式不是鼠标，那么返回 None
        """
        if self.ui_node is None:
            return None

        dropdown = self._get_dropdown_control()
        if dropdown is None:
            return None

        mouse_box = dropdown.GetChildByPath(
            "/dropdown_content/scroll"
            + "/scroll_mouse/scroll_view"
            + "/panel/bar_and_track"
            + "/stack_panel/panel"
            + "/centered_panel/scroll_box"
            + "/box/mouse_box"
        )
        if mouse_box is None:
            return None

        return mouse_box.asImage()

    def _get_mouse_bar_indent(self):  # type: () -> ImageUIControl | None
        """
        _get_mouse_bar_indent 获取下拉框最右方的鼠标可拖动区域的底层图形。
        通过点击它对应的上层控件，可以使下拉框立即切换到不同的显示区域

        Returns:
            ImageUIControl | None:
                如果当前用户输入模式是鼠标，那么试图获取目标底层图形。
                若获取失败，或用户输入模式不是鼠标，那么返回 None
        """
        if self.ui_node is None:
            return None

        dropdown = self._get_dropdown_control()
        if dropdown is None:
            return None

        bar_indent = dropdown.GetChildByPath(
            "/dropdown_content/scroll"
            + "/scroll_mouse/scroll_view"
            + "/panel/bar_and_track"
            + "/stack_panel/panel"
            + "/centered_panel/track"
            + "/bar_indent"
        )
        if bar_indent is None:
            return None

        return bar_indent.asImage()

    def _get_radio_control_group(self):  # type: () -> BaseUIControl | None
        """_get_radio_control_group 返回下拉框中存储所有下拉框子选项的控件

        Returns:
            BaseUIControl | None:
                如果成功，则返回下拉框中存储所有下拉框子选项的控件；
                否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        dropdown = self._get_dropdown_control()
        if dropdown is None:
            return None

        content = get_scroll_view_content(
            self.ui_node,
            dropdown.GetPath() + "/dropdown_content",
        )
        if content is None:
            return None

        return content.GetChildByPath("/radio_control_group")

    def _get_dropdown_background(self):  # type: () -> ImageUIControl | None
        """_get_dropdown_background 返回下拉框的背景所指示的底层图形

        Returns:
            ImageUIControl | None: 如果成功，则返回对应的底层图形；
                                   否则失败，那么返回 None
        """
        if self.ui_node is None:
            return None

        dropdown = self._get_dropdown_control()
        if dropdown is None:
            return None

        background = get_scorll_view_background(
            self.ui_node,
            dropdown.GetPath() + "/dropdown_content",
        )
        if background is None:
            return None

        background = background.GetChildByPath("/background")
        if background is None:
            return None
        return background.asImage()

    def _is_showing_dropdown_content(self):  # type: () -> bool
        """_is_showing_dropdown_content 检查下拉框是否正处于展开状态

        Returns:
            bool: 下拉框是否正处于展开状态
        """
        dropdown = self._get_dropdown_control()
        if dropdown is None:
            return False

        control = dropdown.GetChildByPath("/custom_dropdown")
        if control is None:
            return False

        raw_bag = control.GetPropertyBag()  # type: Any
        property = raw_bag  # type: dict[str, Any]
        return property["#toggle_state"]

    def _is_someone_hover(self):  # type: () -> bool
        """
        _is_someone_hover 检查鼠标是否悬停于下拉框中的任何子选项上。
        要达成这样的条件，应确保用户至少展开了下拉框

        Returns:
            bool: 鼠标是否悬停于下拉框中的任何子选项上
        """
        for i in self.options:
            if i.get_hover_state():
                return True
        return False

    def _set_dropdown_label(self, label):  # type: (str) -> DropDown
        """_set_dropdown_label 设置下拉框所使用的标题文本

        Args:
            label (str): 下拉框希望使用的标题文本

        Returns:
            DropDown: 返回 DropDown 本身
        """
        if self.dropdown is None:
            return self

        child = self.dropdown.GetChildByPath(
            "/dropdown/option_generic_core"
            + "/two_line_layout/option_label_panel"
            + "/option_label"
        )
        if child is None:
            return self

        child = child.asLabel()
        if child is None:
            return self
        child.SetText(label)

        return self

    def _set_inside_label(self, label):  # type: (str) -> DropDown
        """
        _set_inside_label 设置下拉框在未展开时，
        其框中显示的“已选中内容”的文本

        Args:
            label (str): 欲显示的对应文本

        Returns:
            DropDown: 返回 DropDown 本身
        """
        dropdown = self._get_dropdown_control()
        if dropdown is None:
            return self

        control = dropdown.GetChildByPath("/custom_dropdown")
        if control is None:
            return self

        for i in ENUM_BUTTONS:
            child = control.GetChildByPath(
                "/"
                + i
                + "/button_panel/button_content"
                + "/settings_common.default_options_dropdown_toggle_button_state_content/label_panel"
                + "/label"
            )
            if child is None:
                continue

            child = child.asLabel()
            if child is None:
                continue

            child.SetText(label)

        return self

    def _add_options_on_batch(
        self, option_names, selected_index
    ):  # type: (list[str], int) -> DropDown
        """
        _add_options_on_batch 批量化的添加下拉框子选项。
        应确保调用该函数前，已经从画布上移除了已存在的子选项。

        该函数被调用后，self.options 会被重新设置；
        保证调用后，下拉框的所有子选项与 option_names 保持一致，
        并且已选中的下拉框子选项对应的索引是 selected_index

        Args:
            option_names (list[str]): 下拉框新的子选项内容
            selected_index (int): 下拉框要显示的选项之索引

        Returns:
            DropDown: 返回 DropDown 本身
        """
        if self.ui_node is None:
            return self

        control = self._get_radio_control_group()
        if control is None:
            return self

        self.options = []
        for index, value in enumerate(option_names):
            if index == selected_index:
                self._set_inside_label(value)
            radio_with_label = RadioWithLabel(
                self.ui_node,
                control,
                index == selected_index,
                value,
            )
            self.options.append(radio_with_label)

        return self

    def _set_selected_option(self, index):  # type: (int) -> DropDown
        """
        _set_selected_option 设置下拉框已选中的选项。
        实际上，它移除底层的所有下拉框子选项，然后重新添加一次

        Args:
            index (int): 目标选项的索引

        Returns:
            DropDown: 返回 DropDown 本身
        """
        if self.ui_node is None:
            return self

        option_names = []  # type: list[str]
        for i in self.options:
            if i.control is None:
                continue
            option_names.append(i.get_radio_label())
            _ = self.ui_node.RemoveChildControl(i.control)
        self._add_options_on_batch(option_names, index)

        return self

    def on_update_screen(self):  # type: () -> bool
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Returns:
            bool: 指示是否需要刷新屏幕
        """
        if self.ui_node is None or self.control is None or self.dropdown is None:
            return False

        should_update = self._should_update_screen
        if self._should_update_screen:
            self._should_update_screen = False

        selected_index = self.get_selected_option()
        if selected_index != self._last_select_index:
            self._last_select_index = selected_index
            should_update = True

        if self._should_close_dropdown:
            self._should_close_dropdown = False
            option_names = []

            for i in self.options:
                if i.control is None:
                    continue
                option_names.append(i.get_radio_label())
                _ = self.ui_node.RemoveChildControl(i.control)

            _ = self.ui_node.RemoveChildControl(self.dropdown)
            self.dropdown = self.ui_node.CreateChildControl(
                "modal_dropdown.custom_dropdown",
                "dropdown-" + str(uuid.uuid4()),
                self.control,
                False,
            )

            self._last_render_label = self.get_dropdown_label()
            self._set_dropdown_label(self._last_render_label)
            self._add_options_on_batch(option_names, selected_index)
            return True

        if should_update:
            self._last_render_label = self.get_dropdown_label()
            self._set_dropdown_label(self._last_render_label)
            self._set_selected_option(selected_index)
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
                指示是否需要刷新屏幕
        """
        if not self._is_showing_dropdown_content():
            return False

        background = self._get_dropdown_background()
        if background is None:
            return False
        background_rect = background.GetRotateRect()

        if is_touch:
            # The first click just record the touch pos
            if trigger_type == TRIGGER_TYPE_CLICK:
                self._last_click_pos = touch_pos
                return False
            # Now the user release, and we can start processing
            if trigger_type == TRIGGER_TYPE_RELEASE:
                if point_is_in_rect(background_rect, self._last_click_pos):
                    if not point_is_in_rect(background_rect, touch_pos):
                        return False
                    if abs(touch_pos[1] - self._last_click_pos[1]) > 5.25:
                        return False
        else:
            # If mouse is in mouse box
            mouse_box = self._get_mouse_box()
            if mouse_box is None:
                return False
            box_rect = mouse_box.GetRotateRect()
            if point_is_in_rect(box_rect, touch_pos):
                return False
            # If mouse is in mouse bar indent and no radio is hovered
            if not self._is_someone_hover():
                bar_indent = self._get_mouse_bar_indent()
                if bar_indent is None:
                    return False
                bar_indent_rect = bar_indent.GetRotateRect()
                if point_is_in_rect(bar_indent_rect, touch_pos):
                    return False

        self._should_close_dropdown = True
        return False

    def on_key_press(self, press_type, press_key):  # type: (int, str) -> bool
        """on_key_press 在玩家点击键盘时调用

        Args:
            press_type (int):
                触发类型。可能的值及含义如下。
                    - KEY_PRESS_TYPE_DOWN: 用户按下按键
                    - KEY_PRESS_TYPE_UP: 用户释放按键
            press_key (str):
                指示玩家所按下的按键

        Returns:
            bool:
                指示是否需要刷新屏幕
        """
        if not self._is_showing_dropdown_content():
            return False
        if not check_esc_key(press_key):
            return False

        if input_mode_is_touch():
            if press_type != KEY_PRESS_TYPE_UP:
                return False
        else:
            if press_type != KEY_PRESS_TYPE_DOWN:
                return False

        self._should_close_dropdown = True
        return False

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None:
            return

        for i in self.options:
            if i.control is None:
                continue
            _ = self.ui_node.RemoveChildControl(i.control)

        if self.dropdown is not None:
            _ = self.ui_node.RemoveChildControl(self.dropdown)
        if self.control is not None:
            _ = self.ui_node.RemoveChildControl(self.control)

    def get_dropdown_label(self):  # type: () -> str
        """get_dropdown_label 返回下拉框当前所使用的标题文本

        Returns:
            str: 下拉框当前所使用的标题文本
        """
        return self._last_render_label

    def get_selected_option(self):  # type: () -> int
        """
        get_selected_option 返回下拉
        框当前已选中的选项所对应的索引

        Returns:
            int: 该下拉框当前已被选中选项所对应的索引
        """
        for index, value in enumerate(self.options):
            if not value.radio_can_toggled():
                continue
            if value.get_toggle_state():
                return index
        for index, value in enumerate(self.options):
            if value.radio_can_toggled():
                continue
            if value.get_toggle_state():
                return index
        return 0

    def set_dropdown_label(self, label):  # type: (str) -> DropDown
        """set_dropdown_label 设置下拉框所使用的标题文本

        Args:
            label (str): 欲设置的标题文本

        Returns:
            DropDown: 返回 DropDown 本身
        """
        if self.dropdown is None:
            return self
        if label != self._last_render_label:
            self._set_dropdown_label(label)
            self._last_render_label = label
            self._should_update_screen = True
        return self

    def set_selected_option(self, index):  # type: (int) -> DropDown
        """
        set_selected_option 设置下拉框已选中的选项。
        实际上，它移除底层的所有下拉框子选项，然后重新添加一次

        Args:
            index (int): 目标选项的索引

        Returns:
            DropDown: 返回 DropDown 本身
        """
        self._set_selected_option(index)
        self._should_update_screen = True
        return self

    def add_new_option(self, option_name):  # type: (str) -> DropDown
        """
        add_new_option 向下拉框追加一个新的子选项。
        特别地，如果这是首个子选项，那么它将被选中

        Args:
            option_name (int): 要追加的子选项的文本内容

        Returns:
            DropDown: 返回 DropDown 本身
        """
        if self.ui_node is None:
            return self

        control = self._get_radio_control_group()
        if control is None:
            return self

        if len(self.options) == 0:
            self._set_inside_label(option_name)
        radio_with_label = RadioWithLabel(
            self.ui_node,
            control,
            len(self.options) == 0,
            option_name,
        )
        self.options.append(radio_with_label)

        self._should_update_screen = True
        return self
