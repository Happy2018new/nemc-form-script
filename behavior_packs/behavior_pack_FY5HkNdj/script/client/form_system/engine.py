# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from .base import BaseFormSystem
from .base import (
    STATES_SYSTEM_AVAILABLE,
    STATES_SCREEN_IS_PUSHING,
    STATES_SCREEN_IS_SHOWING,
    STATES_SCREEN_SUBMIT_POPPING,
    STATES_SCREEN_FORCE_POPPING,
    STATES_SYSTEM_SHUTDOWN,
)
from .client import ClientFormSystem
from .parser import (
    parse_json_to_long_form,
    parse_json_to_popup_form,
    parse_json_to_modal_form,
)
from ..utils import get_base_path, input_mode_is_touch
from ..form_type.base import (
    TRIGGER_TYPE_CLICK,
    TRIGGER_TYPE_RELEASE,
    KEY_PRESS_TYPE_DOWN,
    KEY_PRESS_TYPE_UP,
)
from ...packet.option import OptionInt
from ...packet.packet import (
    ModalFormResponse,
    PACKET_NAME_MODAL_FORM_RESPONSE,
    MODAL_FORM_CANCEL_REASON_USER_CLOSED,
    MODAL_FORM_CANCEL_REASON_USER_BUSY,
)
from mod.client.extraClientApi import (
    GetClientSystemCls,
    RegisterUI,
    GetTouchPos,
)

ClientSystem = GetClientSystemCls()


class EngineFormSystem:
    parent = None  # type: ClientFormSystem | None

    def __init__(self, parent):  # type: (ClientFormSystem) -> None
        self.parent = parent

    def _render_screen(self, force_update):  # type: (bool) -> None
        """
        _render_screen 重新渲染当前屏幕上的所有已挂载组件。
        如果 force_update 为假，则本函数只会在这些已挂载组
        件发生变化时才会重新进行渲染

        Args:
            force_update (bool): 指示是否需要在本次
                                 调用时强制重新渲染
        """
        base = self.base()
        if base is None:
            return
        should_update = force_update
        if base.base_form is not None and base.base_form.on_update_screen():
            should_update = True
        if base.ui_node is not None and should_update:
            base.ui_node.UpdateScreen()

    def _on_destroy(self):  # type: () -> None
        """_on_destroy 在当前表单被销毁时调用。它是内部实现细节"""
        base = self.base()
        if base is None:
            return
        if base.base_form is not None:
            base.base_form.on_destroy()
            base.base_form = None
        if base.ui_node is not None:
            base.ui_node.SetRemove()
            base.ui_node = None
        base.server_pk = None

    def base(self):  # type: () -> BaseFormSystem | None
        if self.parent is None:
            return None
        return self.parent.base

    def check_incoming_screen(self, args):  # type: (dict[str, Any]) -> bool
        if "screenDef" in args and args["screenDef"] != "form.form_main_screen":
            return False
        if "screenName" in args and args["screenName"] != "form_main_screen":
            return False
        return True

    def on_ui_init_finished(self, _):  # type: (dict[str, Any]) -> None
        base = self.base()
        if base is None:
            return
        if base.locker is None:
            return

        with base.locker:
            RegisterUI(
                "FormScript",
                "form",
                "script.client.node.FormScreenNode",
                "form.form_main_screen",
            )

            if base.server_pk is not None:
                if (
                    base.states == STATES_SCREEN_IS_PUSHING
                    or base.states == STATES_SCREEN_IS_SHOWING
                ):
                    pk = ModalFormResponse(
                        form_id=base.server_pk.form_id,
                        cancel_reason=OptionInt(MODAL_FORM_CANCEL_REASON_USER_BUSY),
                    )
                    base.NotifyToServer(
                        PACKET_NAME_MODAL_FORM_RESPONSE,
                        pk.marshal(),
                    )

            self._on_destroy()
            base.states = STATES_SYSTEM_AVAILABLE

    def on_click_screen(self, _):  # type: (dict[str, Any]) -> None
        self.on_trigger_screen(TRIGGER_TYPE_CLICK)

    def on_release_screen(self, _):  # type: (dict[str, Any]) -> None
        self.on_trigger_screen(TRIGGER_TYPE_RELEASE)

    def on_key_press_in_game(self, args):  # type: (dict[str, Any]) -> None
        base = self.base()
        if base is None:
            return
        if base.locker is None:
            return

        with base.locker:
            if not self.check_incoming_screen(args):
                return

            should_update = False
            press_key = args["key"]
            press_type = (
                KEY_PRESS_TYPE_UP if args["isDown"] == "0" else KEY_PRESS_TYPE_DOWN
            )

            if base.base_form is not None:
                if base.base_form.on_key_press(press_type, press_key):
                    should_update = True

            if not should_update:
                return
            if base.ui_node is not None:
                base.ui_node.UpdateScreen()

    def on_push_screen(self, args):  # type: (dict[str, Any]) -> None
        base = self.base()
        if base is None:
            return
        if base.locker is None:
            return

        with base.locker:
            if base.states != STATES_SCREEN_IS_PUSHING:
                return
            if base.ui_node is None:
                return
            if base.server_pk is None:
                return
            if self.parent is None:
                return
            if not self.check_incoming_screen(args):
                return

            base_control = base.ui_node.GetBaseUIControl(get_base_path())
            form_type = base.server_pk.form_data.get("type", "custom_form")

            if form_type == "form":
                base.base_form = parse_json_to_long_form(
                    base.server_pk.form_data,
                    base.ui_node,
                    base_control,
                    self.parent.on_long_form_submit,
                )
            elif form_type == "modal":
                base.base_form = parse_json_to_popup_form(
                    base.server_pk.form_data,
                    base.ui_node,
                    base_control,
                    self.parent.on_popup_form_submit,
                )
            elif form_type == "custom_form":
                base.base_form = parse_json_to_modal_form(
                    base.server_pk.form_data,
                    base.ui_node,
                    base_control,
                    self.parent.on_modal_form_submit,
                )

            self._render_screen(True)
            base.states = STATES_SCREEN_IS_SHOWING

    def on_pop_screen(self, args):  # type: (dict[str, Any]) -> None
        base = self.base()
        if base is None:
            return
        if base.locker is None:
            return

        with base.locker:
            if self.parent is None:
                return
            if not self.check_incoming_screen(args):
                return

            if (
                base.states != STATES_SCREEN_SUBMIT_POPPING
                and base.states != STATES_SCREEN_FORCE_POPPING
                and base.states != STATES_SCREEN_IS_SHOWING
            ):
                return

            if base.server_pk is not None and base.states == STATES_SCREEN_IS_SHOWING:
                pk = ModalFormResponse(
                    form_id=base.server_pk.form_id,
                    cancel_reason=OptionInt(MODAL_FORM_CANCEL_REASON_USER_CLOSED),
                )
                base.NotifyToServer(
                    PACKET_NAME_MODAL_FORM_RESPONSE,
                    pk.marshal(),
                )

            self._on_destroy()
            base.states = STATES_SYSTEM_AVAILABLE

    def on_update_screen(self, force_update):  # type: (bool) -> None
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Args:
            force_update (bool): 指示是否需要在本次
                                 调用时强制刷新屏幕
        """
        base = self.base()
        if base is None:
            return
        if base.locker is None:
            return

        with base.locker:
            self._render_screen(force_update)

    def on_trigger_screen(self, trigger_type):  # type: (int) -> None
        """on_trigger_screen 在用户点击屏幕时调用

        Args:
            trigger_type (int):
                触发类型。可能的值及含义如下。
                    - TRIGGER_TYPE_CLICK: 用户点击屏幕
                    - TRIGGER_TYPE_RELEASE: 用户释放点击
        """
        base = self.base()
        if base is None:
            return
        if base.locker is None:
            return

        with base.locker:
            should_update = False
            is_touch = input_mode_is_touch()
            touch_pos = GetTouchPos()

            if base.base_form is not None:
                if base.base_form.on_trigger_screen(is_touch, trigger_type, touch_pos):
                    should_update = True

            if not should_update:
                return
            if base.ui_node is not None:
                base.ui_node.UpdateScreen()

    def on_shutdown(self):  # type: () -> None
        """
        on_shutdown 在当前表单所指示
        的底层系统被彻底销毁时被调用
        """
        base = self.base()
        if base is None:
            return
        if base.locker is None:
            return

        with base.locker:
            self._on_destroy()
            base.states = STATES_SYSTEM_SHUTDOWN
