# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl

from ..form_type.other.long import LongForm
from ..form_type.other.popup import PopupForm
from ..form_type.modal.modal import ModalForm
from ..form_type.modal.label import Label
from ..form_type.modal.toggle import Toggle
from ..form_type.modal.input import Input
from ..form_type.modal.dropdown import DropDown
from ..form_type.modal.slider import Slider, StepSlider
from ...formal.long import LongFormIconPathImage, LongFormIconURLImage
from ...formal.long import LongForm as LongFormalForm
from ...formal.popup import PopupForm as PopupFormalForm
from ...formal.modal import ModalForm as ModalFormalForm
from ...formal.modal import (
    ModalFormElementLabel,
    ModalFormElementInput,
    ModalFormElementToggle,
    ModalFormElementDropdown,
    ModalFormElementSlider,
    ModalFormElementStepSlider,
)


def parse_json_to_long_form(
    form_data,  # type: dict[str, Any]
    ui_node,  # type: ScreenNode
    control,  # type: BaseUIControl
    callback,  # type: Callable[[dict[str, Any], int], None]
):  # type: (...) -> LongForm
    """
    parse_json_to_long_form 根据给定的 JSON 数据，
    在对应的节点下创建一个新的长表单

    Args:
        form_data (dict[str, Any]): 给定的 JSON 数据
        ui_node (ScreenNode): 长表单所在的屏幕结点
        control (BaseUIControl): 要将长表单挂接在哪个父节点下
        callback (Callable[[dict[str, Any], int], None]):
            在用户点击长表单中的任何一个按钮时，执行的回调函数。
            回调函数的第二个参数，也即 int 参数指示按钮的索引。

    Returns:
        Long: 无论给定的 JSON 数据如何，
              总是创建并返回一个新的长表单
    """
    formal = LongFormalForm().unmarshal(form_data)
    form = (
        LongForm(ui_node, control, callback)
        .set_title_label(formal.title)
        .set_inside_label(formal.content)
    )

    for i in formal.buttons:
        if isinstance(i.icon, LongFormIconPathImage):
            form.push_button(i.text, i.icon.image_path, False)
        elif isinstance(i.icon, LongFormIconURLImage):
            form.push_button(i.text, i.icon.image_url, True)
        else:
            form.push_button(i.text, "", False)

    return form


def parse_json_to_popup_form(
    form_data,  # type: dict[str, Any]
    ui_node,  # type: ScreenNode
    control,  # type: BaseUIControl
    callback,  # type: Callable[[dict[str, Any], bool], None]
):  # type: (...) -> PopupForm
    """
    parse_json_to_popup_form 根据给定的 JSON 数据，
    在对应的节点下创建一个新的信息（消息）表单

    Args:
        form_data (dict[str, Any]): 给定的 JSON 数据
        ui_node (ScreenNode): 信息表单所在的屏幕结点
        control (BaseUIControl): 要将信息表单挂接在哪个父节点下
        callback (Callable[[dict[str, Any], bool], None]):
            当用户点击代表“确定”或代表“取消”按钮时，应当执行的回调函数。
            回调函数的第二个参数，也即 bool 参数用户点击的按钮是否代表“确定”

    Returns:
        Popup: 无论给定的 JSON 数据如何，
              总是创建并返回一个新的信息表单
    """
    formal = PopupFormalForm().unmarshal(form_data)
    return (
        PopupForm(ui_node, control, callback)
        .set_popup_title(formal.title)
        .set_popup_text(formal.content)
        .set_button_text(formal.button1, True)
        .set_button_text(formal.button2, False)
    )


def parse_json_to_modal_form(
    form_data,  # type: dict[str, Any]
    ui_node,  # type: ScreenNode
    control,  # type: BaseUIControl
    callback,  # type: Callable[[dict[str, Any]], None]
):  # type: (...) -> ModalForm
    """
    parse_json_to_modal_form 根据给定的 JSON 数据，
    在对应的节点下创建一个新的模态表单

    Args:
        form_data (dict[str, Any]): 给定的 JSON 数据
        ui_node (ScreenNode): 模态表单所在的屏幕结点
        control (BaseUIControl): 要将模态表单挂接在哪个父节点下
        callback (Callable[[dict[str, Any]], None]):
            当用户点击模态表单的提交按钮时，应当执行的回调函数

    Returns:
        Modal: 无论给定的 JSON 数据如何，
               总是创建并返回一个新的模态表单
    """
    formal = ModalFormalForm().unmarshal(form_data)
    form = ModalForm(ui_node, control, callback)
    form.set_modal_label(formal.title)
    form.set_modal_submit_button("提交")

    for i in formal.content:
        if isinstance(i, ModalFormElementLabel):
            _ = form.push_label(i.text)
        elif isinstance(i, ModalFormElementInput):
            _ = form.push_input(i.text, i.place_holder, i.default)
        elif isinstance(i, ModalFormElementToggle):
            _ = form.push_toggle(i.text, i.default)
        elif isinstance(i, ModalFormElementDropdown):
            _ = form.push_dropdown(i.text, i.options, i.default)
        elif isinstance(i, ModalFormElementStepSlider):
            _ = form.push_step_slider(i.text, i.steps, i.default)
        elif isinstance(i, ModalFormElementSlider):
            default_index = 0  # type: int
            current_value = i.min_val  # type: float
            slider_contents = []  # type: list[str]

            while current_value <= i.max_val:
                slider_contents.append(str(current_value))
                current_value += i.step
            if (i.max_val - i.min_val) % i.step > 0.00001:
                slider_contents.append(str(i.max_val))
            for index, value in enumerate(slider_contents):
                if i.default >= float(value):
                    default_index = index

            _ = form.push_slider(i.text, slider_contents, default_index)

    return form


def pack_modal_form_response(
    modal,
):  # type: (ModalForm) -> list[bool | str | int | float | None]
    """
    pack_modal_form_response 从模态表单获取
    用户的输入，并将这些输入打包到 JSON 列表

    模态表单有多个元素，每个元素都有对应的输入。
    对于每个元素的输入，确保打包规则和结果如下。

    - 将 Label 打包为 None
    - 将 Toggle 打包为布尔值
    - 将 Input 打包为字符串
    - 将 DropDown 打包为整数
    - 将 Slider 打包为浮点数
    - 将 StepSlider 打包为整数

    Args:
        modal (Modal): 目标模态表单

    Returns:
        list[bool | str | int | float | None]:
            打包好的用户输入
    """
    result = []  # type: list[bool | str | int | float | None]

    for i in modal.childs:
        if isinstance(i, Label):
            result.append(None)
        elif isinstance(i, Toggle):
            value = i.get_toggle_state()
            result.append(value if value is not None else False)
        elif isinstance(i, Input):
            value = i.get_edit_text()
            result.append(value if value is not None else "")
        elif isinstance(i, DropDown):
            value = i.get_selected_option()
            result.append(value)
        elif isinstance(i, StepSlider):
            value = i.get_slider_index()
            result.append(value if value is not None else 0)
        elif isinstance(i, Slider):
            index = i.get_slider_index()
            if index is not None:
                value = float(i.slider_contents[index])
                result.append(value)
            else:
                result.append(0.0)
        else:
            result.append(None)

    return result
