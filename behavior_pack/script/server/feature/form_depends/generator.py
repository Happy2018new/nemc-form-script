# -*- coding: utf-8 -*-

from .define import FormalWithCallback
from ...utils import filter_sentence
from ...executor.executor import GameCodeExecutor
from ...storage.form_struct.base import BaseForm as BaseStorageForm
from ...storage.form_struct.long import (
    LongForm as LongStorageForm,
    LongFormIconPathImage as LongStorageFormIconPathImage,
)
from ...storage.form_struct.popup import PopupForm as PopupStorageForm
from ...storage.form_struct.modal import (
    ModalForm as ModalStorageForm,
    ModalFormElementLabel as ModalStorageFormElementLabel,
    ModalFormElementInput as ModalStorageFormElementInput,
    ModalFormElementToggle as ModalStorageFormElementToggle,
    ModalFormElementDropdown as ModalStorageFormElementDropdown,
    ModalFormElementSlider as ModalStorageFormElementSlider,
    ModalFormElementStepSlider as ModalStorageFormElementStepSlider,
)
from ....formal.long import (
    LongForm as LongFormalForm,
    LongFormElement as LongFormalFormElement,
    LongFormIconPathImage as LongFormalFormIconPathImage,
)
from ....formal.popup import PopupForm as PopupFormalForm
from ....formal.modal import (
    ModalForm as ModalFormalForm,
    ModalFormElementLabel as ModalFormalFormElementLabel,
    ModalFormElementInput as ModalFormalFormElementInput,
    ModalFormElementToggle as ModalFormalFormElementToggle,
    ModalFormElementDropdown as ModalFormalFormElementDropdown,
    ModalFormElementSlider as ModalFormalFormElementSlider,
    ModalFormElementStepSlider as ModalFormalFormElementStepSlider,
)


def _generate_long_form(
    form,  # type: LongStorageForm
    runner,  # type: GameCodeExecutor
    executor,  # type: str
    dimension,  # type: int
    position,  # type: tuple[float, float, float]
):  # type: (...) -> FormalWithCallback
    """
    _generate_long_form 根据存储的长表单生成它的形式化表示，并附带相应的回调函数。
    表单的形式化表示是稳定的，而存储形式则提供了生成形式化表示所需的代码。
    应注意的是，相应的代码在运行前需要提供命令执行上下文，因为代码中可能会用到它们

    Args:
        form (LongStorageForm):
            长表单的存储形式
        runner (GameCodeExecutor):
            用于运行代码的执行器
        executor (str):
            命令执行执行者
        dimension (int):
            命令执行维度
        position (tuple[float, float, float]):
            命令执行点

    Raises:
        Exception:
            如果出现错误，则将抛出

    Returns:
        FormalWithCallback:
            长表单的稳定表示，
            并且附带了相应的回调函数
    """
    result = LongFormalForm()

    title = runner.run_code(
        form.title, "Error occurred in title", executor, dimension, position
    )
    if not isinstance(title, str):
        raise Exception(
            "_generate_long_form: The title of long form must be str (title={})".format(
                title
            )
        )
    result.title = filter_sentence(title)

    content = runner.run_code(
        form.content, "Error occurred in content", executor, dimension, position
    )
    if not isinstance(content, str):
        raise Exception(
            "_generate_long_form: The content of long form must be str (content={})".format(
                content
            )
        )
    result.content = filter_sentence(content)

    for index, value in enumerate(form.buttons):
        # prepare
        element = LongFormalFormElement()
        # text
        ctx = "In text of button which indexed in {}".format(index)
        text = runner.run_code(value.text, ctx, executor, dimension, position)
        if not isinstance(text, str):
            raise Exception(
                "_generate_long_form: The text of button which indexed in {} must be str (text={})".format(
                    index, text
                )
            )
        element.text = filter_sentence(text)
        # icon
        if isinstance(value.icon, LongStorageFormIconPathImage):
            ctx = "In image path of button which indexed in {}".format(index)
            image_path = runner.run_code(
                value.icon.image_path, ctx, executor, dimension, position
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
    form,  # type: PopupStorageForm
    runner,  # type: GameCodeExecutor
    executor,  # type: str
    dimension,  # type: int
    position,  # type: tuple[float, float, float]
):  # type: (...) -> FormalWithCallback
    """
    _generate_popup_form 根据存储的信息表单生成它的形式化表示，并附带相应的回调函数。
    表单的形式化表示是稳定的，而存储形式则提供了生成形式化表示所需的代码。
    应注意的是，相应的代码在运行前需要提供命令执行上下文，因为代码中可能会用到它们

    Args:
        form (PopupStorageForm):
            信息表单的存储形式
        runner (GameCodeExecutor):
            用于运行代码的执行器
        executor (str):
            命令执行执行者
        dimension (int):
            命令执行维度
        position (tuple[float, float, float]):
            命令执行点

    Raises:
        Exception:
            如果出现错误，则将抛出

    Returns:
        FormalWithCallback:
            信息表单的稳定表示，
            并且附带了相应的回调函数
    """
    result = PopupFormalForm()

    title = runner.run_code(
        form.title, "Error occurred in title", executor, dimension, position
    )
    if not isinstance(title, str):
        raise Exception(
            "_generate_popup_form: The title of popup form must be str (title={})".format(
                title
            )
        )
    result.title = filter_sentence(title)

    content = runner.run_code(
        form.content, "Error occurred in content", executor, dimension, position
    )
    if not isinstance(content, str):
        raise Exception(
            "_generate_popup_form: The content of popup form must be str (content={})".format(
                content
            )
        )
    result.content = filter_sentence(content)

    button1 = runner.run_code(
        form.button1, "Error occurred in button1", executor, dimension, position
    )
    if not isinstance(button1, str):
        raise Exception(
            "_generate_popup_form: The button1 of popup form must be str (button1={})".format(
                button1
            )
        )
    result.button1 = filter_sentence(button1)

    button2 = runner.run_code(
        form.button2, "Error occurred in button2", executor, dimension, position
    )
    if not isinstance(button2, str):
        raise Exception(
            "_generate_popup_form: The button2 of popup form must be str (button2={})".format(
                button2
            )
        )
    result.button2 = filter_sentence(button2)

    return FormalWithCallback(
        result, form.onsubmit, form.oncancel, form.onsuberr, form.oncanerr
    )


def _generate_modal_form(
    form,  # type: ModalStorageForm
    runner,  # type: GameCodeExecutor
    executor,  # type: str
    dimension,  # type: int
    position,  # type: tuple[float, float, float]
):  # type: (...) -> FormalWithCallback
    """
    _generate_modal_form 根据存储的模态表单生成它的形式化表示，并附带相应的回调函数。
    表单的形式化表示是稳定的，而存储形式则提供了生成形式化表示所需的代码。
    应注意的是，相应的代码在运行前需要提供命令执行上下文，因为代码中可能会用到它们

    Args:
        form (ModalStorageForm):
            模态表单的存储形式
        runner (GameCodeExecutor):
            用于运行代码的执行器
        executor (str):
            命令执行执行者
        dimension (int):
            命令执行维度
        position (tuple[float, float, float]):
            命令执行点

    Raises:
        Exception:
            如果出现错误，则将抛出

    Returns:
        FormalWithCallback:
            模态表单的稳定表示，
            并且附带了相应的回调函数
    """
    result = ModalFormalForm()

    title = runner.run_code(
        form.title, "Error occurred in title", executor, dimension, position
    )
    if not isinstance(title, str):
        raise Exception(
            "_generate_modal_form: The title of modal form must be str (title={})".format(
                title
            )
        )
    result.title = filter_sentence(title)

    for index, value in enumerate(form.content):
        if isinstance(value, ModalStorageFormElementLabel):
            ctx = "In text of label (index={})".format(index)
            text = runner.run_code(value.text, ctx, executor, dimension, position)
            if not isinstance(text, str):
                raise Exception(
                    "_generate_modal_form: The text of label must be str (index={}, text={})".format(
                        index, text
                    )
                )
            result.content.append(ModalFormalFormElementLabel(filter_sentence(text)))
        elif isinstance(value, ModalStorageFormElementInput):
            # text
            ctx = "In text of input (index={})".format(index)
            text = runner.run_code(value.text, ctx, executor, dimension, position)
            if not isinstance(text, str):
                raise Exception(
                    "_generate_modal_form: The text of input must be str (index={}, text={})".format(
                        index, text
                    )
                )
            # default
            ctx = "In default of input (index={})".format(index)
            default = runner.run_code(value.default, ctx, executor, dimension, position)
            if not isinstance(default, str):
                raise Exception(
                    "_generate_modal_form: The default of input must be str (index={}, default={})".format(
                        index, default
                    )
                )
            # place holder
            ctx = "In place holder of input (index={})".format(index)
            place_holder = runner.run_code(
                value.place_holder, ctx, executor, dimension, position
            )
            if not isinstance(place_holder, str):
                raise Exception(
                    "_generate_modal_form: The place holder of input must be str (index={}, place_holder={})".format(
                        index, place_holder
                    )
                )
            # append
            result.content.append(
                ModalFormalFormElementInput(
                    filter_sentence(text),
                    filter_sentence(default),
                    filter_sentence(place_holder),
                )
            )
        elif isinstance(value, ModalStorageFormElementToggle):
            # text
            ctx = "In text of toggle (index={})".format(index)
            text = runner.run_code(value.text, ctx, executor, dimension, position)
            if not isinstance(text, str):
                raise Exception(
                    "_generate_modal_form: The text of toggle must be str (index={}, text={})".format(
                        index, text
                    )
                )
            # default
            ctx = "In default of toggle (index={})".format(index)
            default = runner.run_code(value.default, ctx, executor, dimension, position)
            if not isinstance(default, bool):
                raise Exception(
                    "_generate_modal_form: The default of toggle must be bool (index={}, default={})".format(
                        index, default
                    )
                )
            # append
            result.content.append(
                ModalFormalFormElementToggle(filter_sentence(text), default)
            )
        elif isinstance(value, ModalStorageFormElementDropdown):
            # prepare
            element = ModalFormalFormElementDropdown()
            # text
            ctx = "In text of dropdown (index={})".format(index)
            text = runner.run_code(value.text, ctx, executor, dimension, position)
            if not isinstance(text, str):
                raise Exception(
                    "_generate_modal_form: The text of dropdown must be str (index={}, text={})".format(
                        index, text
                    )
                )
            element.text = filter_sentence(text)
            # default
            ctx = "In default of dropdown (index={})".format(index)
            default = runner.run_code(value.default, ctx, executor, dimension, position)
            if isinstance(default, bool) or not isinstance(default, int):
                raise Exception(
                    "_generate_modal_form: The default of dropdown must be int (index={}, default={})".format(
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
                ctx = "In option of dropdown (index={}, ind={})".format(index, ind)
                option = runner.run_code(val, ctx, executor, dimension, position)
                if not isinstance(option, str):
                    raise Exception(
                        "_generate_modal_form: The option of dropdown must be str (index={}, ind={}, option={})".format(
                            index, ind, option
                        )
                    )
                element.options.append(filter_sentence(option))
            # append
            result.content.append(element)
        elif isinstance(value, ModalStorageFormElementSlider):
            # text
            ctx = "In text of slider (index={})".format(index)
            text = runner.run_code(value.text, ctx, executor, dimension, position)
            if not isinstance(text, str):
                raise Exception(
                    "_generate_modal_form: The text of slider must be str (index={}, text={})".format(
                        index, text
                    )
                )
            # min value
            ctx = "In min value of slider (index={})".format(index)
            min_val = runner.run_code(value.min_val, ctx, executor, dimension, position)
            if isinstance(min_val, bool) or not isinstance(min_val, (int, float)):
                raise Exception(
                    "_generate_modal_form: The min value of slider must be number (index={}, min_val={})".format(
                        index, min_val
                    )
                )
            # max value
            ctx = "In max value of slider (index={})".format(index)
            max_val = runner.run_code(value.max_val, ctx, executor, dimension, position)
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
            ctx = "In step of slider (index={})".format(index)
            step = runner.run_code(value.step, ctx, executor, dimension, position)
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
            ctx = "In default of slider (index={})".format(index)
            default = runner.run_code(value.default, ctx, executor, dimension, position)
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
                    filter_sentence(text),
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
            ctx = "In text of step slider (index={})".format(index)
            text = runner.run_code(value.text, ctx, executor, dimension, position)
            if not isinstance(text, str):
                raise Exception(
                    "_generate_modal_form: The text of step slider must be str (index={}, text={})".format(
                        index, text
                    )
                )
            element.text = filter_sentence(text)
            # default
            ctx = "In default of step slider (index={})".format(index)
            default = runner.run_code(value.default, ctx, executor, dimension, position)
            if isinstance(default, bool) or not isinstance(default, int):
                raise Exception(
                    "_generate_modal_form: The default of step slider must be int (index={}, default={})".format(
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
                ctx = "In step of step slider (index={}, ind={})".format(index, ind)
                step = runner.run_code(val, ctx, executor, dimension, position)
                if not isinstance(step, str):
                    raise Exception(
                        "_generate_modal_form: The step of step slider must be str (index={}, ind={}, step={})".format(
                            index, ind, step
                        )
                    )
                element.steps.append(filter_sentence(step))
            # append
            result.content.append(element)

    return FormalWithCallback(
        result, form.onsubmit, form.oncancel, form.onsuberr, form.oncanerr
    )


def generate_any_form(
    form,  # type: BaseStorageForm
    runner,  # type: GameCodeExecutor
    executor,  # type: str
    dimension,  # type: int
    position,  # type: tuple[float, float, float]
):  # type: (...) -> FormalWithCallback
    """
    generate_any_form 根据表单的存储型生成它的形式化表示，并附带相应的回调函数。
    表单的形式化表示是稳定的，而存储形式则提供了生成形式化表示所需的代码。
    应注意的是，相应的代码在运行前需要提供命令执行上下文，因为代码中可能会用到它们

    Args:
        form (BaseStorageForm):
            表单的存储形式
        runner (GameCodeExecutor):
            用于运行代码的执行器
        executor (str):
            命令执行执行者
        dimension (int):
            命令执行维度
        position (tuple[float, float, float]):
            命令执行点

    Raises:
        Exception:
            如果出现错误，则将抛出

    Returns:
        FormalWithCallback:
            给定表单的稳定表示，
            并且附带了相应的回调函数
    """
    if isinstance(form, LongStorageForm):
        return _generate_long_form(form, runner, executor, dimension, position)
    if isinstance(form, PopupStorageForm):
        return _generate_popup_form(form, runner, executor, dimension, position)
    if isinstance(form, ModalStorageForm):
        return _generate_modal_form(form, runner, executor, dimension, position)
    raise Exception("unreachable")
