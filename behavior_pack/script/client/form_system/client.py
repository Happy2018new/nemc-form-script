# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from .base import BaseFormSystem
from .base import (
    STATES_SYSTEM_AVAILABLE,
    STATES_SCREEN_IS_PUSHING,
    STATES_SCREEN_IS_SHOWING,
    STATES_SCREEN_SUBMIT_POPPING,
    STATES_SCREEN_FORCE_POPPING,
)
from .parser import pack_modal_form_response
from ..form_type.other.long import LongForm
from ..form_type.other.popup import PopupForm
from ..form_type.modal.modal import ModalForm
from ...packet.option import OptionInt, OptionString
from ...packet.packet import (
    ModalFormRequest,
    ModalFormResponse,
    ClientBoundCloseForm,
    PACKET_NAME_MODAL_FORM_RESPONSE,
    MODAL_FORM_CANCEL_REASON_USER_CLOSED,
    MODAL_FORM_CANCEL_REASON_USER_BUSY,
)
from mod.client.extraClientApi import (
    GetEngineCompFactory,
    GetLevelId,
    GetTopUI,
    GetTopUINode,
    PushScreen,
    PopScreen,
)

BUSY_STATES_USER_BUSY = 0
BUSY_STATES_USER_AVAILABLE = 1
BUSY_STATES_NEED_WAITING = 2


class ClientFormSystem:
    """
    ClientFormSystem 是表单系统在客户端侧的主要实现
    """

    base = None  # type: BaseFormSystem | None

    def __init__(self, base):  # type: (BaseFormSystem) -> None
        """初始化并返回一个新的 ClientFormSystem

        Args:
            base (BaseFormSystem):
                表单系统在客户端侧的基本实现
        """
        self.base = base
        game_comp = GetEngineCompFactory().CreateGame(GetLevelId())
        game_comp.AddRepeatedTimer(0.05, self._pending_request_poller)  # type: ignore

    def _check_is_popping(self):  # type: () -> bool
        """_check_is_popping 检查表单 UI 是否正在被弹出

        Returns:
            bool: 表单 UI 是否正在被弹出
        """
        if self.base is None:
            return False
        if self.base.states == STATES_SCREEN_SUBMIT_POPPING:
            return True
        if self.base.states == STATES_SCREEN_FORCE_POPPING:
            return True
        return False

    def _get_user_busy_states(self, pending=False):  # type: (bool) -> int
        """
        _get_user_busy_states 检查并给出玩家当前的忙碌状态。
        正忙情况下不适合弹出表单 UI。下面列出的情况属于正忙。

        - 表单 UI 仍未完成初始化
        - 用户当前正在其他 UI 界面中（如聊天框）
        - 用户当前已经打开了一个表单 UI

        应当注意的是，当且仅当 pending 为真时，
        _get_user_busy_states 才可能返回 BUSY_STATES_NEED_WAITING

        Args:
            pending (bool, optional):
                指示该函数的调用者是否是待处理表单的处理者。
                默认值为 False

        Returns:
            int:
                用户当前的忙碌状态。可能的值及含义如下。
                    - BUSY_STATES_USER_BUSY: 用户正忙
                    - BUSY_STATES_USER_AVAILABLE: 用户空闲
                    - BUSY_STATES_NEED_WAITING: 需要等待直到空闲
        """
        if self.base is None:
            return BUSY_STATES_USER_BUSY
        if self.base.states != STATES_SYSTEM_AVAILABLE:
            if pending:
                return BUSY_STATES_NEED_WAITING
            else:
                return BUSY_STATES_USER_BUSY

        top_ui_node = GetTopUINode()
        if top_ui_node is None:
            return BUSY_STATES_USER_BUSY

        top_screen_name = top_ui_node.GetScreenName()
        if top_screen_name == "hud.hud_screen":
            return BUSY_STATES_USER_AVAILABLE
        if top_screen_name == "form.form_main_screen" and pending:
            return BUSY_STATES_NEED_WAITING
        return BUSY_STATES_USER_BUSY

    def _pending_request_poller(self):  # type: () -> None
        """
        _pending_request_poller 轮询用户当前的忙碌状态。
        应注意的是，轮询应当由相应的上层调用者统筹和管理。

        如果用户当前空闲并且还存在待处理的表单请求，
        则立即向用户弹出对应的表单 UI。

        如果用户当前正忙，但仍然存在待处理的表单请求，
        则该函数不会向服务器回应用户正忙，而是等待上层调用者的下次轮询。
        这意味着 _pending_request_poller 在本轮次中不执行任何操作。

        当然，若用户当前没有未决的表单请求，则此函数将会立即返回值
        """
        if self.base is None:
            return
        if self.base.locker is None:
            return

        with self.base.locker:
            if self.base.pending_pk is None:
                return

            busy_states = self._get_user_busy_states(True)
            if busy_states == BUSY_STATES_NEED_WAITING:
                return
            if busy_states == BUSY_STATES_USER_AVAILABLE:
                self.base.states = STATES_SCREEN_IS_PUSHING
                self.base.server_pk, self.base.pending_pk = self.base.pending_pk, None
                self.base.ui_node = PushScreen("FormScript", "form", {"isHud": 1})
                return

            resp = ModalFormResponse(
                form_id=self.base.pending_pk.form_id,
                cancel_reason=OptionInt(MODAL_FORM_CANCEL_REASON_USER_BUSY),
            )
            self.base.NotifyToServer(
                PACKET_NAME_MODAL_FORM_RESPONSE,
                resp.marshal(),
            )
            self.base.pending_pk = None

    def on_modal_form_request(self, args):  # type: (dict[str, Any]) -> None
        """
        on_modal_form_request 处理来自服务器的模态表单请求。

        如果玩家当前空闲，则它将试图向玩家弹出对应的表单 UI。
        如果玩家当前正忙，则它将向服务器报告玩家正忙，并且不会弹出表单 UI。

        一种极端情况是，上一个表单 UI 正在弹出，而服务器请求了一个新的模态表单。
        在这种情况下，该请求会被标记为待处理请求，并由相应的轮询器在弹出结束后重新处理该请求

        Args:
            args (dict[str, Any]):
                数据包 ModalFormRequest 的负载
        """
        if self.base is None:
            return
        if self.base.locker is None:
            return

        pk = ModalFormRequest()
        pk.unmarshal(args)

        with self.base.locker:
            if self._check_is_popping() and self.base.pending_pk is None:
                self.base.pending_pk = pk
                return

            if self._get_user_busy_states(False) == BUSY_STATES_USER_AVAILABLE:
                if self.base.pending_pk is not None:
                    pk, self.base.pending_pk = self.base.pending_pk, pk
                self.base.states = STATES_SCREEN_IS_PUSHING
                self.base.server_pk = pk
                self.base.ui_node = PushScreen("FormScript", "form", {"isHud": 1})
                return

            resp = ModalFormResponse(
                form_id=pk.form_id,
                cancel_reason=OptionInt(MODAL_FORM_CANCEL_REASON_USER_BUSY),
            )
            self.base.NotifyToServer(
                PACKET_NAME_MODAL_FORM_RESPONSE,
                resp.marshal(),
            )

    def on_client_bound_close_form(self, args):  # type: (dict[str, Any]) -> None
        """
        on_client_bound_close_form 处理来自服务器的关闭表单请求。
        该函数会试图关闭当前已经打开的所有表单 UI 的堆栈。
        应注意的是，正在被推入的表单 UI 不会在打开后被关闭。

        Args:
            args (dict[str, Any]):
                数据包 ClientBoundCloseForm 的负载
        """
        if self.base is None:
            return
        if self.base.locker is None:
            return

        pk = ClientBoundCloseForm()
        pk.unmarshal(args)

        with self.base.locker:
            forms_id = []  # type: list[int]

            if self.base.pending_pk is not None:
                forms_id.append(self.base.pending_pk.form_id)
                self.base.pending_pk = None

            if (
                GetTopUI() == "form_main_screen"
                and self.base.states == STATES_SCREEN_IS_SHOWING
            ):
                if self.base.server_pk is not None:
                    forms_id.append(self.base.server_pk.form_id)
                    self.base.server_pk = None
                self.base.states = STATES_SCREEN_FORCE_POPPING
                PopScreen()

            for form_id in forms_id:
                self.base.NotifyToServer(
                    PACKET_NAME_MODAL_FORM_RESPONSE,
                    ModalFormResponse(
                        form_id,
                        cancel_reason=OptionInt(MODAL_FORM_CANCEL_REASON_USER_CLOSED),
                    ).marshal(),
                )

    def on_long_form_submit(self, _, index):  # type: (dict[str, Any], int) -> None
        """on_long_form_submit 是玩家提交长表单时执行的回调函数

        Args:
            _ (dict[str, Any]):
                SetButtonTouchUpCallback 传入的字典参数
            index (int):
                玩家点击的按钮的索引
        """
        if self.base is None:
            return
        if self.base.locker is None:
            return

        with self.base.locker:
            if self.base.server_pk is None:
                return
            if not isinstance(self.base.base_form, LongForm):
                return

            pk = ModalFormResponse(
                form_id=self.base.server_pk.form_id,
                response_data=OptionString(json.dumps(index, ensure_ascii=False)),
            )
            self.base.NotifyToServer(
                PACKET_NAME_MODAL_FORM_RESPONSE,
                pk.marshal(),
            )

            self.base.states = STATES_SCREEN_SUBMIT_POPPING
            self.base.server_pk = None

    def on_popup_form_submit(self, _, confirm):  # type: (dict[str, Any], bool) -> None
        """on_popup_form_submit 是玩家提交信息表单时执行的回调函数

        Args:
            _ (dict[str, Any]):
                SetButtonTouchUpCallback 传入的字典参数
            confirm (bool):
                指示玩家点击的按钮是否代表“确定”。
                如果为假，那么玩家点击的按钮代表“取消”
        """
        if self.base is None:
            return
        if self.base.locker is None:
            return

        with self.base.locker:
            if self.base.server_pk is None:
                return
            if not isinstance(self.base.base_form, PopupForm):
                return

            pk = ModalFormResponse(
                form_id=self.base.server_pk.form_id,
                response_data=OptionString(json.dumps(confirm, ensure_ascii=False)),
            )
            self.base.NotifyToServer(
                PACKET_NAME_MODAL_FORM_RESPONSE,
                pk.marshal(),
            )

            self.base.states = STATES_SCREEN_SUBMIT_POPPING
            self.base.server_pk = None

    def on_modal_form_submit(self, _):  # type: (dict[str, Any]) -> None
        """on_modal_form_submit 是玩家提交模态表单时执行的回调函数

        Args:
            _ (dict[str, Any]):
                SetButtonTouchUpCallback 传入的字典参数
        """
        if self.base is None:
            return
        if self.base.locker is None:
            return

        with self.base.locker:
            if self.base.server_pk is None:
                return
            if not isinstance(self.base.base_form, ModalForm):
                return

            pk = ModalFormResponse(
                form_id=self.base.server_pk.form_id,
                response_data=OptionString(
                    json.dumps(
                        pack_modal_form_response(self.base.base_form),
                        ensure_ascii=False,
                    )
                ),
            )
            self.base.NotifyToServer(
                PACKET_NAME_MODAL_FORM_RESPONSE,
                pk.marshal(),
            )

            self.base.states = STATES_SCREEN_SUBMIT_POPPING
            self.base.server_pk = None
