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
    base = None  # type: BaseFormSystem | None

    def __init__(self, base):  # type: (BaseFormSystem) -> None
        self.base = base
        game_comp = GetEngineCompFactory().CreateGame(GetLevelId())
        game_comp.AddRepeatedTimer(0.05, self._pending_request_poller)  # type: ignore

    def _check_is_popping(self):  # type: () -> bool
        if self.base is None:
            return False
        if self.base.states == STATES_SCREEN_SUBMIT_POPPING:
            return True
        if self.base.states == STATES_SCREEN_FORCE_POPPING:
            return True
        return False

    def _get_user_busy_states(self, pending=False):  # type: (bool) -> int
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
        if self.base is None:
            return
        if self.base.locker is None:
            return

        pk = ClientBoundCloseForm()
        pk.unmarshal(args)

        with self.base.locker:
            if self.base.pending_pk is not None:
                self.base.pending_pk = None

            if GetTopUI() != "form_main_screen":
                return
            if self.base.states != STATES_SCREEN_IS_SHOWING:
                return

            self.base.states = STATES_SCREEN_FORCE_POPPING
            self.base.server_pk = None
            PopScreen()

    def on_long_form_submit(self, _, index):  # type: (dict[str, Any], int) -> None
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
