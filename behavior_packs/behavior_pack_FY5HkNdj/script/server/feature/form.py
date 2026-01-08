# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from mod.server.extraServerApi import ServerSystem

import json
from mod.server.extraServerApi import GetEngineCompFactory
from ..storage.base import StringWithHash
from ..storage.form import FormStorage, BaseForm as BaseStorageForm
from ..storage.form_struct.long import (
    LongForm as LongStorageForm,
    LongFormIconPathImage as LongStorageFormIconPathImage,
)
from ..storage.form_struct.popup import PopupForm as PopupStorageForm
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
from ...formal.base import BaseForm as BaseFormalForm
from ...formal.long import (
    LongForm as LongFormalForm,
    LongFormElement as LongFormalFormElement,
    LongFormIconPathImage as LongFormalFormIconPathImage,
)
from ...formal.popup import PopupForm as PopupFormalForm
from ...formal.modal import (
    ModalForm as ModalFormalForm,
    ModalFormElementLabel as ModalFormalFormElementLabel,
    ModalFormElementInput as ModalFormalFormElementInput,
    ModalFormElementToggle as ModalFormalFormElementToggle,
    ModalFormElementDropdown as ModalFormalFormElementDropdown,
    ModalFormElementSlider as ModalFormalFormElementSlider,
    ModalFormElementStepSlider as ModalFormalFormElementStepSlider,
)
from ...packet.packet import (
    PACKET_NAME_MODAL_FORM_REQUEST,
    ModalFormRequest,
    ModalFormResponse,
)


EMPTY_BASE_FORM = BaseFormalForm()
EMPTY_STRING_WITH_HASH = StringWithHash()


class FormalWithCallback:
    formal = EMPTY_BASE_FORM
    onsubmit = EMPTY_STRING_WITH_HASH
    oncancel = EMPTY_STRING_WITH_HASH
    onsuberr = EMPTY_STRING_WITH_HASH
    oncanerr = EMPTY_STRING_WITH_HASH

    def __init__(
        self,
        formal,  # type: BaseFormalForm
        onsubmit,  # type: StringWithHash
        oncancel,  # type: StringWithHash
        onsuberr,  # type: StringWithHash
        oncanerr,  # type: StringWithHash
    ):  # type: (...) -> None
        self.formal = formal
        self.onsubmit = onsubmit
        self.oncancel = oncancel
        self.onsuberr = onsuberr
        self.oncancel = oncanerr

    def validate(
        self, pk
    ):  # type: (ModalFormResponse) -> int | bool | list[int | bool | float | str | None] | None
        raw = pk.response_data.value()
        if raw is None:
            return None
        try:
            resp = json.loads(raw)
        except Exception:
            return None

        if isinstance(self.formal, LongFormalForm):
            if isinstance(resp, bool) or not isinstance(resp, int):
                return None
            return resp
        if isinstance(self.formal, PopupFormalForm):
            if not isinstance(resp, bool):
                return None
            return resp
        if isinstance(self.formal, ModalFormalForm):
            if not isinstance(resp, list):
                return None
            if len(self.formal.content) != len(resp):
                return None
            for index, value in enumerate(self.formal.content):
                if isinstance(value, ModalFormalFormElementLabel):
                    if resp[index] is not None:
                        return None
                elif isinstance(value, ModalFormalFormElementInput):
                    if not isinstance(resp[index], str):
                        return None
                elif isinstance(value, ModalFormalFormElementToggle):
                    if not isinstance(resp[index], bool):
                        return None
                elif isinstance(value, ModalFormalFormElementDropdown):
                    val = resp[index]
                    if isinstance(val, bool) or not isinstance(val, int):
                        return None
                    if val < 0 or val >= len(value.options):
                        return None
                elif isinstance(value, ModalFormalFormElementSlider):
                    val = resp[index]
                    if isinstance(val, bool) or not isinstance(val, (int, float)):
                        return None
                    if val < value.min_val or val > value.max_val:
                        return None
                    resp[index] = float(val)
                elif isinstance(value, ModalFormalFormElementStepSlider):
                    val = resp[index]
                    if isinstance(val, bool) or not isinstance(val, int):
                        return None
                    if val < 0 or val >= len(value.steps):
                        return None
            return resp

        return None


class FormRefProcesser:
    response = None  # type: int | bool | list[int | bool | float | str | None] | None

    def __init__(self):  # type: () -> None
        self.response = None

    def ref(self, index):  # type: (int) -> int | bool | float | str
        if self.response is None:
            raise Exception(
                "ref: Ref statement can only used under form response environment"
            )

        if isinstance(self.response, (int, bool)):
            if index == -1:
                return self.response
            return index == int(self.response)

        if index >= len(self.response):
            raise Exception(
                "ref: Ref index out of range [{}] with length {}".format(
                    index, len(self.response)
                )
            )
        value = self.response[index]
        if value is None:
            raise Exception(
                "ref: Can not reference a null value (index={})".format(index)
            )

        return value


class FormFeature:
    server = None  # type: ServerSystem | None
    storage = None  # type: FormStorage | None
    executor = None  # type: GameCodeExecutor | None
    _sequence = 0  # type: int
    _pending = {}  # type: dict[str, dict[int, FormalWithCallback]]
    _ref = None  # type: FormRefProcesser | None

    def __init__(
        self, server, storage, executor
    ):  # type: (ServerSystem, FormStorage, GameCodeExecutor) -> None
        self.server = server
        self.executor = executor
        self.storage = storage
        self._sequence = 0
        self._pending = {}
        self._ref = FormRefProcesser()

    def _generate_long_form(
        self,
        form,  # type: LongStorageForm
        executor,  # type: str
        dimension,  # type: int
        position,  # type: tuple[float, float, float]
    ):  # type: (...) -> FormalWithCallback
        assert self.executor is not None
        result = LongFormalForm()

        title = self.executor.run_code(form.title, executor, dimension, position, True)
        if not isinstance(title, str):
            raise Exception(
                "_generate_long_form: The title of long form must be str (title={})".format(
                    title
                )
            )
        result.title = title

        content = self.executor.run_code(
            form.content, executor, dimension, position, True
        )
        if not isinstance(content, str):
            raise Exception(
                "_generate_long_form: The content of long form must be str (content={})".format(
                    content
                )
            )
        result.content = content

        for index, value in enumerate(form.buttons):
            # prepare
            element = LongFormalFormElement()
            # text
            text = self.executor.run_code(
                value.text, executor, dimension, position, True
            )
            if not isinstance(text, str):
                raise Exception(
                    "_generate_long_form: The text of button which indexed in {} must be str (text={})".format(
                        index, text
                    )
                )
            element.text = text
            # icon
            if isinstance(value.icon, LongStorageFormIconPathImage):
                image_path = self.executor.run_code(
                    value.icon.image_path, executor, dimension, position, True
                )
                if not isinstance(image_path, str):
                    raise Exception(
                        "_generate_long_form: The image path of button which indexed in {} must be str (image_path={})".format(
                            index, image_path
                        )
                    )
                element.icon = LongFormalFormIconPathImage(image_path)
            # append
            result.buttons.append(element)

        return FormalWithCallback(
            result, form.onsubmit, form.oncancel, form.onsuberr, form.oncanerr
        )

    def _generate_popup_form(
        self,
        form,  # type: PopupStorageForm
        executor,  # type: str
        dimension,  # type: int
        position,  # type: tuple[float, float, float]
    ):  # type: (...) -> FormalWithCallback
        assert self.executor is not None
        result = PopupFormalForm()

        title = self.executor.run_code(form.title, executor, dimension, position, True)
        if not isinstance(title, str):
            raise Exception(
                "_generate_popup_form: The title of popup form must be str (title={})".format(
                    title
                )
            )
        result.title = title

        content = self.executor.run_code(
            form.content, executor, dimension, position, True
        )
        if not isinstance(content, str):
            raise Exception(
                "_generate_popup_form: The content of popup form must be str (content={})".format(
                    content
                )
            )
        result.content = content

        button1 = self.executor.run_code(
            form.button1, executor, dimension, position, True
        )
        if not isinstance(button1, str):
            raise Exception(
                "_generate_popup_form: The button1 of popup form must be str (button1={})".format(
                    button1
                )
            )
        result.button1 = button1

        button2 = self.executor.run_code(
            form.button2, executor, dimension, position, True
        )
        if not isinstance(button2, str):
            raise Exception(
                "_generate_popup_form: The button2 of popup form must be str (button2={})".format(
                    button2
                )
            )
        result.button2 = button2

        return FormalWithCallback(
            result, form.onsubmit, form.oncancel, form.onsuberr, form.oncanerr
        )

    def _generate_modal_form(
        self,
        form,  # type: ModalStorageForm
        executor,  # type: str
        dimension,  # type: int
        position,  # type: tuple[float, float, float]
    ):  # type: (...) -> FormalWithCallback
        assert self.executor is not None
        result = ModalFormalForm()

        title = self.executor.run_code(form.title, executor, dimension, position, True)
        if not isinstance(title, str):
            raise Exception(
                "_generate_modal_form: The title of modal form must be str (title={})".format(
                    title
                )
            )
        result.title = title

        for index, value in enumerate(form.content):
            if isinstance(value, ModalStorageFormElementLabel):
                text = self.executor.run_code(
                    value.text, executor, dimension, position, True
                )
                if not isinstance(text, str):
                    raise Exception(
                        "_generate_modal_form: The text of label must be str (index={}, text={})".format(
                            index, text
                        )
                    )
                result.content.append(ModalFormalFormElementLabel(text))
            elif isinstance(value, ModalStorageFormElementInput):
                # text
                text = self.executor.run_code(
                    value.text, executor, dimension, position, True
                )
                if not isinstance(text, str):
                    raise Exception(
                        "_generate_modal_form: The text of input must be str (index={}, text={})".format(
                            index, text
                        )
                    )
                # place holder
                place_holder = self.executor.run_code(
                    value.place_holder, executor, dimension, position, True
                )
                if not isinstance(place_holder, str):
                    raise Exception(
                        "_generate_modal_form: The place holder of input must be str (index={}, place_holder={})".format(
                            index, place_holder
                        )
                    )
                # default
                default = self.executor.run_code(
                    value.default, executor, dimension, position, True
                )
                if not isinstance(default, str):
                    raise Exception(
                        "_generate_modal_form: The default of input must be str (index={}, default={})".format(
                            index, default
                        )
                    )
                # append
                result.content.append(
                    ModalFormalFormElementInput(text, place_holder, default)
                )
            elif isinstance(value, ModalStorageFormElementToggle):
                # text
                text = self.executor.run_code(
                    value.text, executor, dimension, position, True
                )
                if not isinstance(text, str):
                    raise Exception(
                        "_generate_modal_form: The text of toggle must be str (index={}, text={})".format(
                            index, text
                        )
                    )
                # default
                default = self.executor.run_code(
                    value.default, executor, dimension, position, True
                )
                if not isinstance(default, bool):
                    raise Exception(
                        "_generate_modal_form: The default of toggle must be bool (index={}, default={})".format(
                            index, default
                        )
                    )
                # append
                result.content.append(ModalFormalFormElementToggle(text, default))
            elif isinstance(value, ModalStorageFormElementDropdown):
                # prepare
                element = ModalFormalFormElementDropdown()
                # text
                text = self.executor.run_code(
                    value.text, executor, dimension, position, True
                )
                if not isinstance(text, str):
                    raise Exception(
                        "_generate_modal_form: The text of dropdown must be str (index={}, text={})".format(
                            index, text
                        )
                    )
                element.text = text
                # default
                default = self.executor.run_code(
                    value.default, executor, dimension, position, True
                )
                if isinstance(default, bool) or not isinstance(default, int):
                    raise Exception(
                        "_generate_modal_form: The default of dropdown must be integer (index={}, default={})".format(
                            index, default
                        )
                    )
                if default < 0 or default >= len(value.options):
                    raise Exception(
                        "_generate_modal_form: The default of dropdown is index out of range [{}] with length {} (index={})".format(
                            default, len(value.options), index
                        )
                    )
                element.default = default
                # options
                if len(value.options) == 0:
                    raise Exception(
                        "_generate_modal_form: The options of dropdown can not be empty (index={})".format(
                            index
                        )
                    )
                for ind, val in enumerate(value.options):
                    option = self.executor.run_code(
                        val, executor, dimension, position, True
                    )
                    if not isinstance(option, str):
                        raise Exception(
                            "_generate_modal_form: The option of dropdown must be str (index={}, ind={}, option={})".format(
                                index, ind, option
                            )
                        )
                    element.options.append(option)
                # append
                result.content.append(element)
            elif isinstance(value, ModalStorageFormElementSlider):
                # text
                text = self.executor.run_code(
                    value.text, executor, dimension, position, True
                )
                if not isinstance(text, str):
                    raise Exception(
                        "_generate_modal_form: The text of slider must be str (index={}, text={})".format(
                            index, text
                        )
                    )
                # min value
                min_val = self.executor.run_code(
                    value.min_val, executor, dimension, position, True
                )
                if isinstance(min_val, bool) or not isinstance(min_val, (int, float)):
                    raise Exception(
                        "_generate_modal_form: The min value of slider must be number (index={}, min_val={})".format(
                            index, min_val
                        )
                    )
                # max value
                max_val = self.executor.run_code(
                    value.max_val, executor, dimension, position, True
                )
                if isinstance(max_val, bool) or not isinstance(max_val, (int, float)):
                    raise Exception(
                        "_generate_modal_form: The max value of slider must be number (index={}, max_val={})".format(
                            index, max_val
                        )
                    )
                if max_val <= min_val:
                    raise Exception(
                        "_generate_modal_form: The max value of slider must greater than the min value (index={}, min_val={}, max_val={})".format(
                            index, min_val, max_val
                        )
                    )
                # step
                step = self.executor.run_code(
                    value.step, executor, dimension, position, True
                )
                if isinstance(step, bool) or not isinstance(step, (int, float)):
                    raise Exception(
                        "_generate_modal_form: The step of slider must be number (index={}, step={})".format(
                            index, step
                        )
                    )
                if step <= 0:
                    raise Exception(
                        "_generate_modal_form: The step of slider mut be a positive number (index={}, step={})".format(
                            index, step
                        )
                    )
                # default
                default = self.executor.run_code(
                    value.default, executor, dimension, position, True
                )
                if isinstance(default, bool) or not isinstance(default, (int, float)):
                    raise Exception(
                        "_generate_modal_form: The default of slider must be number (index={}, default={})".format(
                            index, default
                        )
                    )
                if default < min_val or default > max_val:
                    raise Exception(
                        "_generate_modal_form: The default of slider can not be less than the min value or more than the max value (index={}, min_val={}, max_val={}, default={})".format(
                            index, min_val, max_val, default
                        )
                    )
                # append
                result.content.append(
                    ModalFormalFormElementSlider(
                        text,
                        float(min_val),
                        float(max_val),
                        float(step),
                        float(default),
                    )
                )
            elif isinstance(value, ModalStorageFormElementStepSlider):
                # prepare
                element = ModalFormalFormElementStepSlider()
                # text
                text = self.executor.run_code(
                    value.text, executor, dimension, position, True
                )
                if not isinstance(text, str):
                    raise Exception(
                        "_generate_modal_form: The text of step slider must be str (index={}, text={})".format(
                            index, text
                        )
                    )
                element.text = text
                # default
                default = self.executor.run_code(
                    value.default, executor, dimension, position, True
                )
                if isinstance(default, bool) or not isinstance(default, int):
                    raise Exception(
                        "_generate_modal_form: The default of step slider must be integer (index={}, default={})".format(
                            index, default
                        )
                    )
                if default < 0 or default >= len(value.steps):
                    raise Exception(
                        "_generate_modal_form: The default of step slider is index out of range [{}] with length {} (index={})".format(
                            default, len(value.steps), index
                        )
                    )
                element.default = default
                # steps
                if len(value.steps) <= 1:
                    raise Exception(
                        "_generate_modal_form: At least provide two elements for step slider (index={})".format(
                            index
                        )
                    )
                for ind, val in enumerate(value.steps):
                    step = self.executor.run_code(
                        val, executor, dimension, position, True
                    )
                    if not isinstance(step, str):
                        raise Exception(
                            "_generate_modal_form: The step of step slider must be str (index={}, ind={}, step={})".format(
                                index, ind, step
                            )
                        )
                    element.steps.append(step)
                # append
                result.content.append(element)

        return FormalWithCallback(
            result, form.onsubmit, form.oncancel, form.onsuberr, form.oncanerr
        )

    def _generate_any_form(
        self,
        form,  # type: BaseStorageForm
        executor,  # type: str
        dimension,  # type: int
        position,  # type: tuple[float, float, float]
    ):  # type: (...) -> FormalWithCallback
        if isinstance(form, LongStorageForm):
            return self._generate_long_form(form, executor, dimension, position)
        if isinstance(form, PopupStorageForm):
            return self._generate_popup_form(form, executor, dimension, position)
        if isinstance(form, ModalStorageForm):
            return self._generate_modal_form(form, executor, dimension, position)
        raise Exception("unreachable")

    def send_modal_form_request(
        self,
        player_id,  # type: str
        form_name,  # type: str
        executor,  # type: str
        dimension,  # type: int
        position,  # type: tuple[float, float, float]
    ):  # type: (...) -> FormFeature
        assert self.server is not None
        assert self.storage is not None
        assert self.executor is not None

        with self.executor.get_locker():
            storage_form = self.storage.get_form(form_name)
            if storage_form is None:
                raise Exception(
                    "send_modal_form_request: Form {} not found".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )

            formal_with_cb = self._generate_any_form(
                storage_form, executor, dimension, position
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

            self.server.NotifyToClient(
                player_id,
                PACKET_NAME_MODAL_FORM_REQUEST,
                ModalFormRequest(self._sequence, raw).marshal(),
            )
            return self

    # def on_player_leave
    # dump from and helpful func (built-in func)

    def on_modal_form_response(
        self, player_id, pk
    ):  # type: (str, ModalFormResponse) -> FormFeature
        assert self.executor is not None
        assert self._ref is not None

        with self.executor.get_locker():
            player_forms = self._pending.get(player_id, {})
            formal_with_cb = player_forms.get(pk.form_id, None)
            if formal_with_cb is None:
                raise Exception("on_modal_form_response: Bad packet (mark 0)")

            cancel = pk.cancel_reason.value()
            if cancel is not None:
                func_to_run = formal_with_cb.oncancel
                when_meet_err = formal_with_cb.oncanerr
                self._ref.response = cancel
            else:
                response = formal_with_cb.validate(pk)
                if response is None:
                    raise Exception("on_modal_form_response: Bad packet (mark 1)")
                func_to_run = formal_with_cb.onsubmit
                when_meet_err = formal_with_cb.onsuberr
                self._ref.response = response

            position = GetEngineCompFactory().CreatePos(player_id).GetPos()
            dimension = (
                GetEngineCompFactory().CreateDimension(player_id).GetEntityDimensionId()
            )
            try:
                _ = self.executor.run_code(
                    func_to_run, player_id, dimension, position, False
                )
            except Exception as e:
                _ = self.executor.variable_run(
                    when_meet_err,
                    player_id,
                    dimension,
                    position,
                    {"error": str(e)},
                    False,
                )
            finally:
                self._ref.response = None

            return self
