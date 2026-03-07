# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from .storage.form import FormStorage
from .storage.function import FunctionStorage
from .storage.event import EventStorage
from .executor.cache import CompileCache
from .feature.form import FormFeature
from .feature.function import FunctionFeature
from .feature.event import EventFeature
from .handler import (
    CommandBlockOutputHandler,
    CompileCacheHandler,
    CustomFormHandler,
    CustomFunctionHandler,
    EditButtonHandler,
    EditDropdownHandler,
    EditInputHandler,
    EditLabelHandler,
    EditLongFormHandler,
    EditModalFormHandler,
    EditPopupFormHandler,
    EditSliderHandler,
    EditStepSliderHandler,
    EditToggleHandler,
    SystemEventHandler,
)


class CommandHandlers:
    """
    CommandHandlers 是所有自定义命令的总处理设备
    """

    command_block_output = None  # type: CommandBlockOutputHandler | None
    compile_cache = None  # type: CompileCacheHandler | None
    custom_form = None  # type: CustomFormHandler | None
    custom_function = None  # type: CustomFunctionHandler | None
    edit_button = None  # type: EditButtonHandler | None
    edit_dropdown = None  # type: EditDropdownHandler | None
    edit_input = None  # type: EditInputHandler | None
    edit_label = None  # type: EditLabelHandler | None
    edit_long_form = None  # type: EditLongFormHandler | None
    edit_modal_form = None  # type: EditModalFormHandler | None
    edit_popup_form = None  # type: EditPopupFormHandler | None
    edit_slider = None  # type: EditSliderHandler | None
    edit_step_slider = None  # type: EditStepSliderHandler | None
    edit_toggle = None  # type: EditToggleHandler | None
    system_event = None  # type: SystemEventHandler | None

    def __init__(
        self,
        compile_cache,  # type: CompileCache
        form_storage,  # type: FormStorage
        func_storage,  # type: FunctionStorage
        event_storage,  # type: EventStorage
        form_feature,  # type: FormFeature
        func_feature,  # type: FunctionFeature
        event_feature,  # type: EventFeature
    ):  # type: (...) -> None
        """初始化并返回一个新的 CommandHandlers

        Args:
            compile_cache (CompileCache):
                代码编译的缓存管理器
            form_storage (FormStorage):
                所有表单的存储管理器
            func_storage (FunctionStorage):
                所有自定义函数的存储管理器
            event_storage (EventStorage):
                所有事件的存储管理器
            form_feature (FormFeature):
                表单系统的主要实现
            func_feature (FunctionFeature):
                自定义函数的主要实现
            event_feature (EventFeature):
                事件侦听系统的主要实现
        """
        self.command_block_output = CommandBlockOutputHandler()
        self.compile_cache = CompileCacheHandler(compile_cache)
        self.custom_form = CustomFormHandler(form_storage, form_feature)
        self.custom_function = CustomFunctionHandler(func_storage, func_feature)
        self.edit_button = EditButtonHandler(form_storage, form_feature)
        self.edit_dropdown = EditDropdownHandler(form_storage, form_feature)
        self.edit_input = EditInputHandler(form_storage, form_feature)
        self.edit_label = EditLabelHandler(form_storage, form_feature)
        self.edit_long_form = EditLongFormHandler(form_storage, form_feature)
        self.edit_modal_form = EditModalFormHandler(form_storage, form_feature)
        self.edit_popup_form = EditPopupFormHandler(form_storage, form_feature)
        self.edit_slider = EditSliderHandler(form_storage, form_feature)
        self.edit_step_slider = EditStepSliderHandler(form_storage, form_feature)
        self.edit_toggle = EditToggleHandler(form_storage, form_feature)
        self.system_event = SystemEventHandler(event_storage, event_feature)

    def on_custom_command_trigger(self, args):  # type: (dict[str, Any]) -> None
        """
        on_custom_command_trigger 在自定义命令被触发时调用

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        command = args["command"]  # type: str
        if command == "commandblockoutput":
            assert self.command_block_output is not None
            self.command_block_output.on_custom_command_trigger(args)
        elif command == "compilecache":
            assert self.compile_cache is not None
            self.compile_cache.on_custom_command_trigger(args)
        elif command == "customform":
            assert self.custom_form is not None
            self.custom_form.on_custom_command_trigger(args)
        elif command == "customfunction":
            assert self.custom_function is not None
            self.custom_function.on_custom_command_trigger(args)
        elif command == "editbutton":
            assert self.edit_button is not None
            self.edit_button.on_custom_command_trigger(args)
        elif command == "editdropdown":
            assert self.edit_dropdown is not None
            self.edit_dropdown.on_custom_command_trigger(args)
        elif command == "editinput":
            assert self.edit_input is not None
            self.edit_input.on_custom_command_trigger(args)
        elif command == "editlabel":
            assert self.edit_label is not None
            self.edit_label.on_custom_command_trigger(args)
        elif command == "editlongform":
            assert self.edit_long_form is not None
            self.edit_long_form.on_custom_command_trigger(args)
        elif command == "editmodalform":
            assert self.edit_modal_form is not None
            self.edit_modal_form.on_custom_command_trigger(args)
        elif command == "editpopupform":
            assert self.edit_popup_form is not None
            self.edit_popup_form.on_custom_command_trigger(args)
        elif command == "editslider":
            assert self.edit_slider is not None
            self.edit_slider.on_custom_command_trigger(args)
        elif command == "editstepslider":
            assert self.edit_step_slider is not None
            self.edit_step_slider.on_custom_command_trigger(args)
        elif command == "edittoggle":
            assert self.edit_toggle is not None
            self.edit_toggle.on_custom_command_trigger(args)
        elif command == "systemevent":
            assert self.system_event is not None
            self.system_event.on_custom_command_trigger(args)
