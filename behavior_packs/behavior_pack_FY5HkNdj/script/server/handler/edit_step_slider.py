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
    ModalFormElementStepSlider as ModalStorageFormElementStepSlider,
)

SUB_COMMAND_TYPE_APPEND = 1
SUB_COMMAND_TYPE_DEFAULT = 2
SUB_COMMAND_TYPE_INSERT = 3
SUB_COMMAND_TYPE_LIST = 4
SUB_COMMAND_TYPE_POP = 5
SUB_COMMAND_TYPE_SUB = 6
SUB_COMMAND_TYPE_TEXT = 7

POP_RAW_ACTION_LEFT = "left"
POP_RAW_ACTION_RIGHT = "right"

SUB_RAW_ACTION_KEEP = "keep"
SUB_RAW_ACTION_DISCARD = "discard"


class EditStepSliderHandler:
    """
    EditStepSliderHandler 是所有 /editstepslider 命令的处理设备
    """

    storage = None  # type: FormStorage | None
    feature = None  # type: FormFeature | None

    def __init__(self, storage, feature):  # type: (FormStorage, FormFeature) -> None
        """初始化并返回一个新的 EditStepSliderHandler

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
        有必要确保它的上层调用者验证了调用的命令是 /editstepslider

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_APPEND:
                args["return_msg_key"] = self.handle_append(cmdargs)
            elif variant == SUB_COMMAND_TYPE_DEFAULT:
                args["return_msg_key"] = self.handle_default(cmdargs)
            elif variant == SUB_COMMAND_TYPE_INSERT:
                args["return_msg_key"] = self.handle_insert(cmdargs)
            elif variant == SUB_COMMAND_TYPE_LIST:
                args["return_msg_key"] = self.handle_list(cmdargs)
            elif variant == SUB_COMMAND_TYPE_POP:
                args["return_msg_key"] = self.handle_pop(cmdargs)
            elif variant == SUB_COMMAND_TYPE_SUB:
                args["return_msg_key"] = self.handle_sub(cmdargs)
            elif variant == SUB_COMMAND_TYPE_TEXT:
                args["return_msg_key"] = self.handle_text(cmdargs)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

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
        assert self.feature is not None
        assert self.feature.executor is not None
        assert self.feature.executor.compile_cache is not None

        form_name = args[0]["value"]  # type: str
        index = args[1]["value"]  # type: int
        step_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editstepslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementStepSlider):
                raise Exception("commands.editstepslider.elementnotmatch")

            real_step_code = StringWithHash(step_code)
            _ = self.feature.executor.compile_cache.get_runner(real_step_code)
            element.steps.append(real_step_code)

            return "commands.editstepsliderappend.success"

    def handle_default(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_default 处理 default 子命令

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
        index = args[1]["value"]  # type: int
        index_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editstepslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementStepSlider):
                raise Exception("commands.editstepslider.elementnotmatch")

            real_index_code = StringWithHash(index_code)
            _ = self.feature.executor.compile_cache.get_runner(real_index_code)
            element.default = real_index_code

            return "commands.editstepsliderdefault.success"

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
        assert self.feature is not None
        assert self.feature.executor is not None
        assert self.feature.executor.compile_cache is not None

        form_name = args[0]["value"]  # type: str
        index = args[1]["value"]  # type: int
        sub_index = args[3]["value"]  # type: int
        step_code = args[4]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editstepslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementStepSlider):
                raise Exception("commands.editstepslider.elementnotmatch")
            if sub_index < 0 or sub_index > len(element.steps):
                raise Exception(
                    "给出的子索引 {} 超出长度 {}".format(sub_index, len(element.steps))
                )

            real_step_code = StringWithHash(step_code)
            _ = self.feature.executor.compile_cache.get_runner(real_step_code)
            element.steps.insert(sub_index, real_step_code)

            return "commands.editstepsliderinsert.success"

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
        index = args[1]["value"]  # type: int

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editstepslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementStepSlider):
                raise Exception("commands.editstepslider.elementnotmatch")

            return "目标显式步进滑块具有 {} 个选项".format(len(element.steps))

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
        index = args[1]["value"]  # type: int
        pop_action = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editstepslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementStepSlider):
                raise Exception("commands.editstepslider.elementnotmatch")

            if len(element.steps) == 0:
                raise Exception("commands.editstepsliderpop.failed")
            if pop_action == POP_RAW_ACTION_LEFT:
                _ = element.steps.pop(0)
            elif pop_action == POP_RAW_ACTION_RIGHT:
                _ = element.steps.pop(-1)

            return "commands.editstepsliderpop.success"

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
        index = args[1]["value"]  # type: int
        sub_action = args[3]["value"]  # type: str
        start_index = args[4]["value"]  # type: int
        end_index = args[5]["value"]  # type: int

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editstepslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementStepSlider):
                raise Exception("commands.editstepslider.elementnotmatch")

            if start_index < 0 or start_index > len(element.steps):
                raise Exception(
                    "给出的起始索引 {} 超出长度 {}".format(
                        start_index, len(element.steps)
                    )
                )
            if end_index < 0 or end_index > len(element.steps):
                raise Exception(
                    "给出的结束索引 {} 超出长度 {}".format(
                        end_index, len(element.steps)
                    )
                )
            if end_index < start_index:
                raise Exception(
                    "给出的结束索引 {} 小于起始索引 {}".format(end_index, start_index)
                )

            if sub_action == SUB_RAW_ACTION_KEEP:
                element.steps = element.steps[start_index:end_index]
                return "commands.editstepslidersubkeep.success"
            elif sub_action == SUB_RAW_ACTION_DISCARD:
                element.steps = element.steps[:start_index] + element.steps[end_index:]
                return "commands.editstepslidersubdiscard.success"

            raise Exception("unreachable")

    def handle_text(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_text 处理 text 子命令

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
        index = args[1]["value"]  # type: int
        text_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editstepslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementStepSlider):
                raise Exception("commands.editstepslider.elementnotmatch")

            real_text_code = StringWithHash(text_code)
            _ = self.feature.executor.compile_cache.get_runner(real_text_code)
            element.text = real_text_code

            return "commands.editstepslidertext.success"
