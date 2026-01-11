# -*- coding: utf-8 -*-

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
            self.command_block_output.on_custom_command_trigger(args)
        elif command == "compilecache":
            self.compile_cache.on_custom_command_trigger(args)
        elif command == "customform":
            self.custom_form.on_custom_command_trigger(args)
        elif command == "customfunction":
            self.custom_function.on_custom_command_trigger(args)
        elif command == "editbutton":
            self.edit_button.on_custom_command_trigger(args)
        elif command == "editdropdown":
            self.edit_dropdown.on_custom_command_trigger(args)
        elif command == "editinput":
            self.edit_input.on_custom_command_trigger(args)
        elif command == "editlabel":
            self.edit_label.on_custom_command_trigger(args)
        elif command == "editlongform":
            self.edit_long_form.on_custom_command_trigger(args)
        elif command == "editmodalform":
            self.edit_modal_form.on_custom_command_trigger(args)
        elif command == "editpopupform":
            self.edit_popup_form.on_custom_command_trigger(args)
        elif command == "editslider":
            self.edit_slider.on_custom_command_trigger(args)
        elif command == "editstepslider":
            self.edit_step_slider.on_custom_command_trigger(args)
        elif command == "edittoggle":
            self.edit_toggle.on_custom_command_trigger(args)
        elif command == "systemevent":
            self.system_event.on_custom_command_trigger(args)
