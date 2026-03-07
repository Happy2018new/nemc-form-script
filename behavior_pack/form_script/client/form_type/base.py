# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl

TRIGGER_TYPE_CLICK = 0
TRIGGER_TYPE_RELEASE = 1

KEY_PRESS_TYPE_DOWN = 0
KEY_PRESS_TYPE_UP = 1


class BaseComponent:
    """BaseComponent 是所有表单组件的父类"""

    ui_node = None  # type: ScreenNode | None
    control = None  # type: BaseUIControl | None

    def __init__(self, ui_node):  # type: (ScreenNode) -> None
        """初始化并返回一个新的 BaseComponent

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
        """
        self.ui_node = ui_node
        self.control = None

    def on_update_screen(self):  # type: () -> bool
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Returns:
            bool: 指示是否需要刷新屏幕
        """
        return False

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
        _, _, _ = is_touch, trigger_type, touch_pos
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
        _, _ = press_type, press_key
        return False

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        pass


class BaseForm:
    """BaseForm 是所有表单的父类"""

    ui_node = None  # type: ScreenNode | None
    control = None  # type: BaseUIControl | None
    childs = []  # type: list[BaseComponent]
    _should_update_screen = False  # type: bool

    def __init__(self, ui_node):  # type: (ScreenNode) -> None
        """初始化并返回一个新的 BaseForm

        Args:
            ui_node (ScreenNode): 该表单所在的屏幕结点
        """
        self.ui_node = ui_node
        self.control = None
        self.childs = []
        self._should_update_screen = False

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

        for i in self.childs:
            if i.on_update_screen():
                should_update = True

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
        should_update = False
        for i in self.childs:
            if i.on_trigger_screen(is_touch, trigger_type, touch_pos):
                should_update = True
        return should_update

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
        should_update = False
        for i in self.childs:
            if i.on_key_press(press_type, press_key):
                should_update = True
        return should_update

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None or self.control is None:
            return
        for i in self.childs:
            i.on_destroy()
        self.ui_node.RemoveChildControl(self.control)
