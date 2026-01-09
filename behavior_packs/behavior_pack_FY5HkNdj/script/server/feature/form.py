# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from mod.server.extraServerApi import ServerSystem

import json
import threading
from mod.server.extraServerApi import GetEngineCompFactory
from .form_depends.define import FormalWithCallback, FormRefProcesser
from .form_depends.generator import generate_any_form
from ..storage.form import FORM_TYPE_LONG, FORM_TYPE_MODAL, FormStorage
from ..storage.form_struct.long import (
    LongForm as LongStorageForm,
    LongFormIconPathImage as LongStorageFormIconPathImage,
)
from ..storage.form_struct.modal import (
    ModalForm as ModalStorageForm,
    ModalFormElementLabel as ModalStorageFormElementLabel,
    ModalFormElementInput as ModalStorageFormElementInput,
    ModalFormElementToggle as ModalStorageFormElementToggle,
    ModalFormElementDropdown as ModalStorageFormElementDropdown,
    ModalFormElementSlider as ModalStorageFormElementSlider,
    ModalFormElementStepSlider as ModalStorageFormElementStepSlider,
)
from ..executor.executor import GameCodeExecutor
from ...formal.long import LongForm as LongFormalForm
from ...formal.popup import PopupForm as PopupFormalForm
from ...formal.modal import ModalForm as ModalFormalForm
from ...packet.packet import (
    PACKET_NAME_MODAL_FORM_REQUEST,
    MODAL_FORM_CANCEL_REASON_USER_CLOSED,
    MODAL_FORM_CANCEL_REASON_USER_BUSY,
    ModalFormRequest,
    ModalFormResponse,
)


LONG_FORM_ICON_TYPE_NONE = 0
LONG_FORM_ICON_TYPE_PATH_IMAGE = 1

MODAL_FORM_ELEMENT_TYPE_LABEL = 0
MODAL_FORM_ELEMENT_TYPE_INPUT = 1
MODAL_FORM_ELEMENT_TYPE_TOGGLE = 2
MODAL_FORM_ELEMENT_TYPE_DROPDOWN = 3
MODAL_FORM_ELEMENT_TYPE_SLIDER = 4
MODAL_FORM_ELEMENT_TYPE_STEP_SLIDER = 5


class FormFeature:
    """
    FormFeature 实现了表单系统在服务器上的主要特性。
    确保 FormFeature 的实现是线程安全的，
    并且仅会对不同线程之间的调用产生互斥作用
    """

    system = None  # type: ServerSystem | None
    storage = None  # type: FormStorage | None
    executor = None  # type: GameCodeExecutor | None
    _sequence = 0  # type: int
    _pending = {}  # type: dict[str, dict[int, FormalWithCallback]]
    _ref = None  # type: FormRefProcesser | None
    _locker = None  # type: threading.RLock | None

    def __init__(
        self, system, storage, executor
    ):  # type: (ServerSystem, FormStorage, GameCodeExecutor) -> None
        """初始化并返回一个新的 FormFeature

        Args:
            system (ServerSystem):
                当前模组的服务端实现
            storage (FormStorage):
                所有表单的存储管理器
            executor (GameCodeExecutor):
                用户代码的执行器
        """
        self.system = system
        self.executor = executor
        self.storage = storage
        self._sequence = 0
        self._pending = {}
        self._ref = FormRefProcesser()
        self._locker = threading.RLock()
        self._dynamic_init()

    def _dynamic_init(self):  # type: () -> None
        """
        _dynamic_init 设置 Ref 语句相关联的函数，
        并同时初始化和设置与表单相关的内建动态函数
        """
        assert self.executor is not None
        assert self.executor.static_builtin is not None
        assert self.executor.static_builtin.manager is not None
        assert self._ref is not None

        manager = self.executor.static_builtin.manager
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["form.list_all_form"] = lambda: manager.ref(self.list_all_form)
        funcs["form.list_long_form_icon_type"] = lambda form_name: manager.ref(
            self.list_long_form_icon_type(form_name)
        )
        funcs["form.list_modal_form_element_type"] = lambda form_name: manager.ref(
            self.list_modal_form_element_type(form_name)
        )
        funcs["form.custom_form_type"] = lambda form_name: self.custom_form_type(
            form_name
        )
        funcs["form.long_form_element_icon_type"] = (
            lambda form_name, index: self.long_form_element_icon_type(form_name, index)
        )
        funcs["form.modal_form_element_type"] = (
            lambda form_name, index: self.modal_form_element_type(form_name, index)
        )
        funcs["form.modal_form_length"] = lambda form_name: self.modal_form_length(
            form_name
        )
        funcs["form.long_form_length"] = lambda form_name: self.long_form_length(
            form_name
        )
        funcs["form.dropdown_length"] = lambda form_name, index: self.dropdown_length(
            form_name, index
        )
        funcs["form.step_slider_length"] = (
            lambda form_name, index: self.step_slider_length(form_name, index)
        )

        with self.executor.get_locker():
            _ = self.executor.set_ref_func(self._ref.ref)
            _ = self.executor.inject_func(funcs)

    def send_modal_form_request(
        self,
        player_id,  # type: str
        form_name,  # type: str
        executor,  # type: str
        dimension,  # type: int
        position,  # type: tuple[float, float, float]
    ):  # type: (...) -> FormFeature
        """
        send_modal_form_request 向指定的玩家打开表单。
        它应该是通过指令调用的，所以您需要提供命令执行上下文

        Args:
            player_id (str):
                目标玩家的 ID
            form_name (str):
                要打开的表单的名称
            executor (str):
                命令执行者
            dimension (int):
                命令执行维度
            position (tuple[float, float, float]):
                命令执行点

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            FormFeature: 返回 FormFeature 本身
        """
        assert self.system is not None
        assert self.storage is not None
        assert self.executor is not None
        assert self._locker is not None

        with self._locker:
            with self.storage.get_locker():
                storage_form = self.storage.get_form(form_name)
                if storage_form is None:
                    raise Exception(
                        "send_modal_form_request: Form {} not found".format(
                            json.dumps(form_name, ensure_ascii=False)
                        )
                    )
                with self.executor.get_locker():
                    formal_with_cb = generate_any_form(
                        storage_form, self.executor, executor, dimension, position
                    )

            self._sequence += 1
            player_forms = self._pending.get(player_id, {})
            player_forms[self._sequence] = formal_with_cb
            self._pending[player_id] = player_forms

            raw = formal_with_cb.formal.marshal()
            if isinstance(formal_with_cb.formal, LongFormalForm):
                raw["type"] = "form"
            elif isinstance(formal_with_cb.formal, PopupFormalForm):
                raw["type"] = "modal"
            elif isinstance(formal_with_cb.formal, ModalFormalForm):
                raw["type"] = "custom_form"

            self.system.NotifyToClient(
                player_id,
                PACKET_NAME_MODAL_FORM_REQUEST,
                ModalFormRequest(self._sequence, raw).marshal(),
            )
            return self

    def on_modal_form_response(
        self, player_id, pk
    ):  # type: (str, ModalFormResponse) -> FormFeature
        """
        on_modal_form_response 在玩家提交表单时被调用，
        这通常意味着玩家以提交的方式响应了表单

        Args:
            player_id (str):
                提交者的 ID
            pk (ModalFormResponse):
                相应的负载

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            FormFeature: 返回 FormFeature 本身
        """
        assert self.executor is not None
        assert self._ref is not None
        assert self._locker is not None

        with self._locker:
            player_forms = self._pending.get(player_id, {})
            formal_with_cb = player_forms.get(pk.form_id, None)
            if formal_with_cb is None:
                raise Exception(
                    "on_modal_form_response: Bad packet (mark 0); packet = {}".format(
                        pk
                    )
                )

            cancel = pk.cancel_reason.value()
            if cancel is not None:
                if cancel not in (
                    MODAL_FORM_CANCEL_REASON_USER_CLOSED,
                    MODAL_FORM_CANCEL_REASON_USER_BUSY,
                ):
                    raise Exception(
                        "on_modal_form_response: Bad packet (mark 2); packet = {}".format(
                            pk
                        )
                    )
                func_to_run = formal_with_cb.oncancel
                when_meet_err = formal_with_cb.oncanerr
                self._ref.response = cancel
            else:
                response = formal_with_cb.validate(pk)
                if response is None:
                    raise Exception(
                        "on_modal_form_response: Bad packet (mark 1); packet = {}".format(
                            pk
                        )
                    )
                func_to_run = formal_with_cb.onsubmit
                when_meet_err = formal_with_cb.onsuberr
                self._ref.response = response

            position = GetEngineCompFactory().CreatePos(player_id).GetPos()
            dimension = (
                GetEngineCompFactory().CreateDimension(player_id).GetEntityDimensionId()
            )
            with self.executor.get_locker():
                try:
                    _ = self.executor.run_code(
                        func_to_run, "", player_id, dimension, position, False
                    )
                except Exception as e:
                    _ = self.executor.variable_run(
                        when_meet_err,
                        "",
                        player_id,
                        dimension,
                        position,
                        {"error": str(e)},
                        False,
                    )
                finally:
                    self._ref.response = None

            return self

    def on_player_leave(self, args):  # type: (dict[str, Any]) -> None
        """on_player_leave 在有玩家离开服务器时被调用

        Args:
            args (dict[str, Any]):
                PlayerIntendLeaveServerEvent 传入的字典参数
        """
        assert self._locker is not None

        with self._locker:
            player_id = args["playerId"]  # type: str
            if player_id in self._pending:
                del self._pending[player_id]

    def list_all_form(self):  # type: () -> dict[str, int]
        """
        list_all_form 列出当前所有的表单及它们的类型

        Returns:
            dict[str, int]:
                当前所有的表单及它们的类型
        """
        assert self.storage is not None

        with self.storage.get_locker():
            return self.storage.form_index()

    def list_long_form_icon_type(self, form_name):  # type: (str) -> list[int]
        """
        list_long_form_icon_type 列出长表单中所有按钮的图标类型

        Args:
            form_name (str): 长表单的名称

        Raises:
            Exception:
                如果目标表单不存在，
                或目标表单不是长表单，
                则抛出相应的错误

        Returns:
            list[int]:
                目标长表单中，
                所有按钮的图标类型
        """
        assert self.storage is not None

        with self.storage.get_locker():
            result = []  # type: list[int]

            form_type = self.storage.form_type(form_name)
            if form_type is None:
                raise Exception(
                    "list_long_form_icon_type: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if form_type != FORM_TYPE_LONG:
                raise Exception(
                    "list_long_form_icon_type: Target form is not a long form"
                )

            storage_form = self.storage.get_form(form_name)
            if storage_form is None or not isinstance(storage_form, LongStorageForm):
                return result

            for i in storage_form.buttons:
                if isinstance(i.icon, LongStorageFormIconPathImage):
                    result.append(LONG_FORM_ICON_TYPE_PATH_IMAGE)
                else:
                    result.append(LONG_FORM_ICON_TYPE_NONE)
            return result

    def list_modal_form_element_type(self, form_name):  # type: (str) -> list[int]
        """
        list_modal_form_element_type 列出模态表单中所有元素的类型

        Args:
            form_name (str): 模态表单的名称

        Raises:
            Exception:
                如果目标表单不存在，
                或目标表单不是模态表单，
                则抛出相应的错误

        Returns:
            list[int]:
                目标模态表单中，
                所有元素的类型
        """
        assert self.storage is not None

        with self.storage.get_locker():
            result = []  # type: list[int]

            form_type = self.storage.form_type(form_name)
            if form_type is None:
                raise Exception(
                    "list_modal_form_element_type: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if form_type != FORM_TYPE_MODAL:
                raise Exception(
                    "list_modal_form_element_type: Target form is not a modal form"
                )

            storage_form = self.storage.get_form(form_name)
            if storage_form is None or not isinstance(storage_form, ModalStorageForm):
                return result

            for i in storage_form.content:
                if isinstance(i, ModalStorageFormElementLabel):
                    result.append(MODAL_FORM_ELEMENT_TYPE_LABEL)
                elif isinstance(i, ModalStorageFormElementInput):
                    result.append(MODAL_FORM_ELEMENT_TYPE_INPUT)
                elif isinstance(i, ModalStorageFormElementToggle):
                    result.append(MODAL_FORM_ELEMENT_TYPE_TOGGLE)
                elif isinstance(i, ModalStorageFormElementDropdown):
                    result.append(MODAL_FORM_ELEMENT_TYPE_DROPDOWN)
                elif isinstance(i, ModalStorageFormElementSlider):
                    result.append(MODAL_FORM_ELEMENT_TYPE_SLIDER)
                elif isinstance(i, ModalStorageFormElementStepSlider):
                    result.append(MODAL_FORM_ELEMENT_TYPE_STEP_SLIDER)
            return result

    def custom_form_type(self, form_name):  # type: (str) -> int
        """custom_form_type 查询一个表单的类型

        Args:
            form_name (str): 欲查询的表单的名称

        Raises:
            Exception:
                如果目标表单不存在，
                则抛出相应的错误

        Returns:
            int:
                目标表单的类型，只可能为下列之一。
                    - FORM_TYPE_LONG: 长表单
                    - FORM_TYPE_POPUP: 信息表单
                    - FORM_TYPE_MODAL: 模态表单
        """
        assert self.storage is not None

        with self.storage.get_locker():
            form_type = self.storage.form_type(form_name)
            if form_type is not None:
                return form_type
            raise Exception(
                "custom_form_type: Form {} not found".format(
                    json.dumps(form_name, ensure_ascii=False)
                )
            )

    def long_form_element_icon_type(self, form_name, index):  # type: (str, int) -> int
        """long_form_element_icon_type 查询长表单中指定按钮的图标类型

        Args:
            form_name (str): 目标长表单的名称
            index (int): 目标按钮在给定长表单中的索引

        Raises:
            Exception:
                如果目标表单不存在，
                或目标表单不是长表单，
                或索引超过范围，
                则抛出相应的错误

        Returns:
            int:
                目标按钮的图标类型，只可能为下列之一。
                    - LONG_FORM_ICON_TYPE_NONE: 该按钮无图标
                    - LONG_FORM_ICON_TYPE_PATH_IMAGE: 该按钮使用材质贴图
        """
        assert self.storage is not None

        with self.storage.get_locker():
            form_type = self.storage.form_type(form_name)
            if form_type is None:
                raise Exception(
                    "long_form_element_icon_type: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if form_type != FORM_TYPE_LONG:
                raise Exception(
                    "long_form_element_icon_type: Target form is not a long form"
                )

            storage_form = self.storage.get_form(form_name)
            if storage_form is None or not isinstance(storage_form, LongStorageForm):
                return 0
            if index < 0 or index >= len(storage_form.buttons):
                raise Exception(
                    "long_form_element_icon_type: Index out of range [{}] with length {}".format(
                        index, len(storage_form.buttons)
                    )
                )

            button = storage_form.buttons[index]
            if isinstance(button.icon, LongStorageFormIconPathImage):
                return LONG_FORM_ICON_TYPE_PATH_IMAGE
            else:
                return LONG_FORM_ICON_TYPE_NONE

    def modal_form_element_type(self, form_name, index):  # type: (str, int) -> int
        """modal_form_element_type 查询模态表单中指定元素的类型

        Args:
            form_name (str): 目标模态表单的名称
            index (int): 目标元素在给定模态表单中的索引

        Raises:
            Exception:
                如果目标表单不存在，
                或目标表单不是模态表单，
                或索引超过范围，
                则抛出相应的错误

        Returns:
            int:
                目标元素的类型，只可能为下列之一。
                    - MODAL_FORM_ELEMENT_TYPE_LABEL: 普通文本
                    - MODAL_FORM_ELEMENT_TYPE_INPUT: 输入框
                    - MODAL_FORM_ELEMENT_TYPE_TOGGLE: 开关
                    - MODAL_FORM_ELEMENT_TYPE_DROPDOWN: 下拉框
                    - MODAL_FORM_ELEMENT_TYPE_SLIDER: 隐式步进滑动条
                    - MODAL_FORM_ELEMENT_TYPE_STEP_SLIDER: 显式步进滑动条
        """
        assert self.storage is not None

        with self.storage.get_locker():
            form_type = self.storage.form_type(form_name)
            if form_type is None:
                raise Exception(
                    "modal_form_element_type: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if form_type != FORM_TYPE_MODAL:
                raise Exception(
                    "modal_form_element_type: Target form is not a modal form"
                )

            storage_form = self.storage.get_form(form_name)
            if storage_form is None or not isinstance(storage_form, ModalStorageForm):
                return -1
            if index < 0 or index >= len(storage_form.content):
                raise Exception(
                    "modal_form_element_type: Index out of range [{}] with length {}".format(
                        index, len(storage_form.content)
                    )
                )

            element = storage_form.content[index]
            if isinstance(element, ModalStorageFormElementLabel):
                return MODAL_FORM_ELEMENT_TYPE_LABEL
            elif isinstance(element, ModalStorageFormElementInput):
                return MODAL_FORM_ELEMENT_TYPE_INPUT
            elif isinstance(element, ModalStorageFormElementToggle):
                return MODAL_FORM_ELEMENT_TYPE_TOGGLE
            elif isinstance(element, ModalStorageFormElementDropdown):
                return MODAL_FORM_ELEMENT_TYPE_DROPDOWN
            elif isinstance(element, ModalStorageFormElementSlider):
                return MODAL_FORM_ELEMENT_TYPE_SLIDER
            elif isinstance(element, ModalStorageFormElementStepSlider):
                return MODAL_FORM_ELEMENT_TYPE_STEP_SLIDER
            raise Exception("unreachable")

    def modal_form_length(self, form_name):  # type: (str) -> int
        """modal_form_length 返回模态表单中元素的数量

        Args:
            form_name (str): 模态表单的名称

        Raises:
            Exception:
                如果目标表单不存在，
                或目标表单不是模态表单，
                则抛出相应的错误

        Returns:
            int: 模态表单中元素的数量
        """
        assert self.storage is not None

        with self.storage.get_locker():
            form_type = self.storage.get_form(form_name)
            if form_type is None:
                raise Exception(
                    "modal_form_length: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if form_type != FORM_TYPE_MODAL:
                raise Exception("modal_form_length: Target form is not a modal form")

            storage_form = self.storage.get_form(form_name)
            if isinstance(storage_form, ModalStorageForm):
                return len(storage_form.content)
            return 0

    def long_form_length(self, form_name):  # type: (str) -> int
        """long_form_length 返回长表单中按钮的数量

        Args:
            form_name (str): 长表单的名称

        Raises:
            Exception:
                如果目标表单不存在，
                或目标表单不是长表单，
                则抛出相应的错误

        Returns:
            int: 长表单中按钮的数量
        """
        assert self.storage is not None

        with self.storage.get_locker():
            form_type = self.storage.get_form(form_name)
            if form_type is None:
                raise Exception(
                    "long_form_length: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if form_type != FORM_TYPE_LONG:
                raise Exception("long_form_length: Target form is not a long form")

            storage_form = self.storage.get_form(form_name)
            if isinstance(storage_form, LongStorageForm):
                return len(storage_form.buttons)
            return 0

    def dropdown_length(self, form_name, index):  # type: (str, int) -> int
        """
        dropdown_length 返回下拉框的选项数量。
        应说明的是，下拉框只在模态表单中存在

        Args:
            form_name (str):
                下拉框所在模态表单的名称
            index (int):
                下拉框在模态表单中的索引

        Raises:
            Exception:
                如果目标表单不存在，
                或目标表单不是模态表单，
                或索引超过范围，
                或目标元素不是下拉框，
                则抛出相应的错误

        Returns:
            int: 下拉框的选项数量
        """
        assert self.storage is not None

        with self.storage.get_locker():
            form_type = self.storage.form_type(form_name)
            if form_type is None:
                raise Exception(
                    "dropdown_length: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if form_type != FORM_TYPE_MODAL:
                raise Exception("dropdown_length: Target form is not a modal form")

            storage_form = self.storage.get_form(form_name)
            if storage_form is None or not isinstance(storage_form, ModalStorageForm):
                return 0
            if index < 0 or index >= len(storage_form.content):
                raise Exception(
                    "dropdown_length: Index out of range [{}] with length {}".format(
                        index, len(storage_form.content)
                    )
                )

            element = storage_form.content[index]
            if not isinstance(element, ModalStorageFormElementDropdown):
                raise Exception(
                    "dropdown_length: Target element is not a dropdown (element={})".format(
                        element
                    )
                )
            return len(element.options)

    def step_slider_length(self, form_name, index):  # type: (str, int) -> int
        """
        step_slider_length 返回显式步进滑块的选项数量。
        应说明的是，显式步进滑块只在模态表单中存在

        Args:
            form_name (str):
                显式步进滑块所在模态表单的名称
            index (int):
                显式步进滑块在模态表单中的索引

        Raises:
            Exception:
                如果目标表单不存在，
                或目标表单不是模态表单，
                或索引超过范围，
                或目标元素不是显式步进滑块，
                则抛出相应的错误

        Returns:
            int: 显式步进滑块的选项数量
        """
        assert self.storage is not None

        with self.storage.get_locker():
            form_type = self.storage.form_type(form_name)
            if form_type is None:
                raise Exception(
                    "step_slider_length: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if form_type != FORM_TYPE_MODAL:
                raise Exception("step_slider_length: Target form is not a modal form")

            storage_form = self.storage.get_form(form_name)
            if storage_form is None or not isinstance(storage_form, ModalStorageForm):
                return 0
            if index < 0 or index >= len(storage_form.content):
                raise Exception(
                    "step_slider_length: Index out of range [{}] with length {}".format(
                        index, len(storage_form.content)
                    )
                )

            element = storage_form.content[index]
            if not isinstance(element, ModalStorageFormElementStepSlider):
                raise Exception(
                    "step_slider_length: Target element is not a step slider (element={})".format(
                        element
                    )
                )
            return len(element.steps)
