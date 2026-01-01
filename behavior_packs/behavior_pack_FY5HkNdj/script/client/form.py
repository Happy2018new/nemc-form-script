# -*- coding: utf-8 -*-

from .form_system.base import BaseFormSystem
from .form_system.client import ClientFormSystem
from .form_system.engine import EngineFormSystem
from ..packet.packet import (
    PACKET_NAME_MODAL_FORM_REQUEST,
    PACKET_NAME_CLIENT_BOUND_CLOSE_FORM,
)
from mod.client.extraClientApi import GetClientSystemCls

ClientSystem = GetClientSystemCls()


class FormSystem(BaseFormSystem):
    """
    FormSystem 是表单系统在客户端侧实现的接口
    """

    client_form_system = None  # type: ClientFormSystem | None
    engine_form_system = None  # type: EngineFormSystem | None

    def __init__(self, namespace, system_name):  # type: (str, str) -> None
        """初始化并返回一个新的 FormSystem

        Args:
            namespace (str):
                该表单模组的命名空间
            system_name (str):
                该表单模组在客户端侧的系统名称
        """
        BaseFormSystem.__init__(self, namespace, system_name)
        self.client_form_system = ClientFormSystem(self)
        self.engine_form_system = EngineFormSystem(self.client_form_system)

        self.listen_engine_event(
            "UiInitFinished",
            self.engine_form_system,
            self.engine_form_system.on_ui_init_finished,
        )
        self.listen_engine_event(
            "GetEntityByCoordEvent",
            self.engine_form_system,
            self.engine_form_system.on_click_screen,
        )
        self.listen_engine_event(
            "GetEntityByCoordReleaseClientEvent",
            self.engine_form_system,
            self.engine_form_system.on_release_screen,
        )
        self.listen_engine_event(
            "OnKeyPressInGame",
            self.engine_form_system,
            self.engine_form_system.on_key_press_in_game,
        )
        self.listen_engine_event(
            "PushScreenEvent",
            self.engine_form_system,
            self.engine_form_system.on_push_screen,
        )
        self.listen_engine_event(
            "PopScreenEvent",
            self.engine_form_system,
            self.engine_form_system.on_pop_screen,
        )

        self.listen_form_event(
            PACKET_NAME_MODAL_FORM_REQUEST,
            self.client_form_system,
            self.client_form_system.on_modal_form_request,
        )
        self.listen_form_event(
            PACKET_NAME_CLIENT_BOUND_CLOSE_FORM,
            self.client_form_system,
            self.client_form_system.on_client_bound_close_form,
        )

    def on_update_screen(self, force_update):  # type: (bool) -> None
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Args:
            force_update (bool): 指示是否需要在本次
                                 调用时强制刷新屏幕
        """
        if self.engine_form_system is None:
            return
        self.engine_form_system.on_update_screen(force_update)

    def on_shutdown(self):  # type: () -> None
        """
        on_shutdown 在当前表单所指示
        的底层系统被彻底销毁时被调用
        """
        if self.engine_form_system is None:
            return
        self.engine_form_system.on_shutdown()
