# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from ..feature.form import FormFeature
from ..storage.base import StringWithHash
from ..storage.form import FormStorage
from ..storage.form_struct.modal import (
    ModalForm as ModalStorageForm,
    ModalFormElement as ModalStorageFormElement,
    ModalFormElementLabel as ModalStorageFormElementLabel,
    ModalFormElementInput as ModalStorageFormElementInput,
    ModalFormElementToggle as ModalStorageFormElementToggle,
    ModalFormElementDropdown as ModalStorageFormElementDropdown,
    ModalFormElementSlider as ModalStorageFormElementSlider,
    ModalFormElementStepSlider as ModalStorageFormElementStepSlider,
)

SUB_COMMAND_TYPE_APPEND = 1
SUB_COMMAND_TYPE_INSERT = 2
SUB_COMMAND_TYPE_LIST = 3
SUB_COMMAND_TYPE_POP = 4
SUB_COMMAND_TYPE_SUB = 5
SUB_COMMAND_TYPE_TITLE = 6

ELEMENT_RAW_TYPE_LABEL = "label"
ELEMENT_RAW_TYPE_INPUT = "input"
ELEMENT_RAW_TYPE_TOGGLE = "toggle"
ELEMENT_RAW_TYPE_DROPDOWN = "dropdown"
ELEMENT_RAW_TYPE_SLIDER = "slider"
ELEMENT_RAW_TYPE_STEP_SLIDER = "stepslider"

POP_RAW_ACTION_LEFT = "left"
POP_RAW_ACTION_RIGHT = "right"

SUB_RAW_ACTION_KEEP = "keep"
SUB_RAW_ACTION_DISCARD = "discard"


class EditModalFormHandler:
    """
    EditModalFormHandler 是所有 /editmodalform 命令的处理设备
    """

    storage = None  # type: FormStorage | None
    feature = None  # type: FormFeature | None

    def __init__(self, storage, feature):  # type: (FormStorage, FormFeature) -> None
        """初始化并返回一个新的 EditModalFormHandler

        Args:
            storage (FormStorage):
                所有表单的存储管理器
            feature (FormFeature):
                表单系统的主要实现
        """
        self.storage = storage
        self.feature = feature

    def on_custom_command_trigger(self, args):  # type: (dict[str, Any]) -> None
        """
        on_custom_command_trigger 在自定义命令被触发时调用。
        有必要确保它的上层调用者验证了调用的命令是 /editmodalform

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_APPEND:
                args["return_msg_key"] = self.handle_append(cmdargs)
            elif variant == SUB_COMMAND_TYPE_INSERT:
                args["return_msg_key"] = self.handle_insert(cmdargs)
            elif variant == SUB_COMMAND_TYPE_LIST:
                args["return_msg_key"] = self.handle_list(cmdargs)
            elif variant == SUB_COMMAND_TYPE_POP:
                args["return_msg_key"] = self.handle_pop(cmdargs)
            elif variant == SUB_COMMAND_TYPE_SUB:
                args["return_msg_key"] = self.handle_sub(cmdargs)
            elif variant == SUB_COMMAND_TYPE_TITLE:
                args["return_msg_key"] = self.handle_title(cmdargs)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

    def _default_modal_form_element(
        self, element_raw_type
    ):  # type: (str) -> ModalStorageFormElement
        """
        _default_modal_form_element
        根据命令中对模态表单元素的类型枚举，
        返回其对应的模态表单元素的默认形式

        Args:
            element_raw_type (str):
                命令中对模态表单元素的类型枚举

        Returns:
            ModalStorageFormElement:
                对应模态表单元素的默认形式
        """
        if element_raw_type == ELEMENT_RAW_TYPE_LABEL:
            return ModalStorageFormElementLabel(StringWithHash("return ''"))
        elif element_raw_type == ELEMENT_RAW_TYPE_INPUT:
            return ModalStorageFormElementInput(
                StringWithHash("return ''"),
                StringWithHash("return ''"),
                StringWithHash("return ''"),
            )
        elif element_raw_type == ELEMENT_RAW_TYPE_TOGGLE:
            return ModalStorageFormElementToggle(
                StringWithHash("return ''"), StringWithHash("return False")
            )
        elif element_raw_type == ELEMENT_RAW_TYPE_DROPDOWN:
            return ModalStorageFormElementDropdown(
                StringWithHash("return ''"), [], StringWithHash("return 0")
            )
        elif element_raw_type == ELEMENT_RAW_TYPE_SLIDER:
            return ModalStorageFormElementSlider(
                StringWithHash("return ''"),
                StringWithHash("return 0.0"),
                StringWithHash("return 1.0"),
                StringWithHash("return 1.0"),
                StringWithHash("return 0.0"),
            )
        elif element_raw_type == ELEMENT_RAW_TYPE_STEP_SLIDER:
            return ModalStorageFormElementStepSlider(
                StringWithHash("return ''"), [], StringWithHash("return 0")
            )
        raise Exception("unreachable")

    def _modal_form_element_name(self, element_raw_type):  # type: (str) -> str
        """
        _modal_form_element_name 根据命令中对模
        态表单元素的类型枚举，返回该元素对应的名称

        Args:
            element_raw_type (str):
                命令中对模态表单元素的类型枚举

        Returns:
            str: 该模态表单元素的名称
        """
        if element_raw_type == ELEMENT_RAW_TYPE_LABEL:
            return "普通文本"
        elif element_raw_type == ELEMENT_RAW_TYPE_INPUT:
            return "输入框"
        elif element_raw_type == ELEMENT_RAW_TYPE_TOGGLE:
            return "开关"
        elif element_raw_type == ELEMENT_RAW_TYPE_DROPDOWN:
            return "下拉框"
        elif element_raw_type == ELEMENT_RAW_TYPE_SLIDER:
            return "隐式步进滑块"
        elif element_raw_type == ELEMENT_RAW_TYPE_STEP_SLIDER:
            return "显式步进滑块"
        raise Exception("unreachable")

    def handle_append(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_append 处理 append 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.storage is not None

        form_name = args[0]["value"]  # type: str
        element_type = args[2]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editmodalform.formnotmatch")
            form.content.append(
                self._default_modal_form_element(
                    element_type,
                )
            )
            return "已成功向模态表单 {} 添加一个{}".format(
                json.dumps(form_name, ensure_ascii=False),
                self._modal_form_element_name(element_type),
            )

    def handle_insert(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_insert 处理 insert 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.storage is not None

        form_name = args[0]["value"]  # type: str
        index = args[2]["value"]  # type: int
        element_type = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editmodalform.formnotmatch")

            if index < 0 or index > len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            form.content.insert(
                index,
                self._default_modal_form_element(element_type),
            )

            return "已成功向模态表单 {} 插入一个{}".format(
                json.dumps(form_name, ensure_ascii=False),
                self._modal_form_element_name(element_type),
            )

    def handle_list(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_list 处理 list 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.storage is not None
        form_name = args[0]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editmodalform.formnotmatch")

            if len(form.content) == 0:
                return "模态表单 {} 目前没有任何元素".format(
                    json.dumps(form_name, ensure_ascii=False)
                )
            result = "模态表单 {} 目前已存在 {} 个元素: ".format(
                json.dumps(form_name, ensure_ascii=False), len(form.content)
            )
            for i in form.content:
                if isinstance(i, ModalStorageFormElementLabel):
                    result += "\n  - 普通文本"
                elif isinstance(i, ModalStorageFormElementInput):
                    result += "\n  - 输入框"
                elif isinstance(i, ModalStorageFormElementToggle):
                    result += "\n  - 开关"
                elif isinstance(i, ModalStorageFormElementDropdown):
                    result += "\n  - 下拉框"
                elif isinstance(i, ModalStorageFormElementSlider):
                    result += "\n  - 隐式步进滑块"
                elif isinstance(i, ModalStorageFormElementStepSlider):
                    result += "\n  - 显式步进滑块"

            return result

    def handle_pop(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_pop 处理 pop 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.storage is not None

        form_name = args[0]["value"]  # type: str
        pop_action = args[2]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editmodalform.formnotmatch")

            if len(form.content) == 0:
                raise Exception(
                    "模态表单 {} 没有任何元素可供移除".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if pop_action == POP_RAW_ACTION_LEFT:
                _ = form.content.pop(0)
            elif pop_action == POP_RAW_ACTION_RIGHT:
                _ = form.content.pop(-1)

            return "已成功移除模态表单 {} 中的最后一个元素".format(
                json.dumps(form_name, ensure_ascii=False)
            )

    def handle_sub(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_sub 处理 sub 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.storage is not None

        form_name = args[0]["value"]  # type: str
        sub_action = args[2]["value"]  # type: str
        start_index = args[3]["value"]  # type: int
        end_index = args[4]["value"]  # type: int

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editmodalform.formnotmatch")

            if start_index < 0 or start_index > len(form.content):
                raise Exception(
                    "给出的起始索引 {} 超出长度 {}".format(
                        start_index, len(form.content)
                    )
                )
            if end_index < 0 or end_index > len(form.content):
                raise Exception(
                    "给出的结束索引 {} 超出长度 {}".format(end_index, len(form.content))
                )
            if end_index < start_index:
                raise Exception(
                    "给出的结束索引 {} 小于起始索引 {}".format(end_index, start_index)
                )

            if sub_action == SUB_RAW_ACTION_KEEP:
                form.content = form.content[start_index:end_index]
                return "已成功为模态表单 {} 的元素列表执行保留的截取操作".format(
                    json.dumps(form_name, ensure_ascii=False)
                )
            elif sub_action == SUB_RAW_ACTION_DISCARD:
                form.content = form.content[:start_index] + form.content[end_index:]
                return "已成功为模态表单 {} 的元素列表执行丢弃的截取操作".format(
                    json.dumps(form_name, ensure_ascii=False)
                )

            raise Exception("unreachable")

    def handle_title(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_title 处理 title 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.storage is not None
        assert self.feature is not None
        assert self.feature.executor is not None
        assert self.feature.executor.compile_cache is not None

        form_name = args[0]["value"]  # type: str
        title_code = args[2]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editmodalform.formnotmatch")

            real_title_code = StringWithHash(title_code)
            _ = self.feature.executor.compile_cache.get_runner(real_title_code)
            form.title = real_title_code

            return "已成功设置模态表单 {} 的标题文本".format(
                json.dumps(form_name, ensure_ascii=False)
            )
