# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from mod.client.extraClientApi import ScreenNode

import threading
from ..form_type.base import BaseForm
from ...packet.packet import ModalFormRequest
from mod.client.extraClientApi import (
    GetEngineNamespace,
    GetEngineSystemName,
    GetClientSystemCls,
)

ClientSystem = GetClientSystemCls()

STATES_SYSTEM_INITIALIZING = 0
STATES_SYSTEM_AVAILABLE = 1
STATES_SCREEN_IS_PUSHING = 2
STATES_SCREEN_IS_SHOWING = 3
STATES_SCREEN_SUBMIT_POPPING = 4
STATES_SCREEN_FORCE_POPPING = 5
STATES_SYSTEM_SHUTDOWN = 6


class BaseFormSystem(ClientSystem):
    states = 0  # type: int
    locker = None  # type: threading.Lock | None
    ui_node = None  # type: ScreenNode | None
    base_form = None  # type: BaseForm | None
    server_pk = None  # type: ModalFormRequest | None
    pending_pk = None  # type: ModalFormRequest | None

    def __init__(self, namespace, system_name):  # type: (str, str) -> None
        ClientSystem.__init__(self, namespace, system_name)
        self.states = STATES_SYSTEM_INITIALIZING
        self.locker = threading.Lock()
        self.ui_node = None
        self.base_form = None
        self.server_pk = None
        self.pending_pk = None

    def listen_engine_event(
        self, event_name, instance, callback
    ):  # type: (str, Any, Callable[[dict[str, Any]], None]) -> None
        """listen_engine_event 监听引擎事件

        Args:
            event_name (str): 引擎事件名称
            instance (Any): callback 所在类的实例
            callback (Callable[[dict[str, Any]], None]):
                在监听到事件时，调用的函数
        """
        self.ListenForEvent(
            GetEngineNamespace(),
            GetEngineSystemName(),
            event_name,
            instance,
            callback,  # type: ignore
        )

    def listen_form_event(
        self, event_name, instance, callback
    ):  # type: (str, Any, Callable[[dict[str, Any]], None]) -> None
        """listen_form_event 监听本系统，也即表单系统的事件

        Args:
            event_name (str): 要监听的事件名
            instance (Any): callback 所在类的实例
            callback (Callable[[dict[str, Any]], None]):
                在监听到事件时，调用的函数
        """
        self.ListenForEvent("FormScript", "FormServerSystem", event_name, instance, callback)  # type: ignore
