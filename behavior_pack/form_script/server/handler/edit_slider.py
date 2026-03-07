# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from ..feature.form import FormFeature
from ..storage.base import StringWithHash
from ..storage.form import FormStorage
from ..storage.form_struct.modal import (
    ModalForm as ModalStorageForm,
    ModalFormElementSlider as ModalStorageFormElementSlider,
)

SUB_COMMAND_TYPE_DEFAULT = 1
SUB_COMMAND_TYPE_MIN = 2
SUB_COMMAND_TYPE_MAX = 3
SUB_COMMAND_TYPE_STEP = 4
SUB_COMMAND_TYPE_TEXT = 5


class EditSliderHandler:
    """
    EditSliderHandler 是所有 /editslider 命令的处理设备
    """

    storage = None  # type: FormStorage | None
    feature = None  # type: FormFeature | None

    def __init__(self, storage, feature):  # type: (FormStorage, FormFeature) -> None
        """初始化并返回一个新的 EditSliderHandler

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
        有必要确保它的上层调用者验证了调用的命令是 /editslider

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_DEFAULT:
                args["return_msg_key"] = self.handle_default(cmdargs)
            elif variant == SUB_COMMAND_TYPE_MIN:
                args["return_msg_key"] = self.handle_min(cmdargs)
            elif variant == SUB_COMMAND_TYPE_MAX:
                args["return_msg_key"] = self.handle_max(cmdargs)
            elif variant == SUB_COMMAND_TYPE_STEP:
                args["return_msg_key"] = self.handle_step(cmdargs)
            elif variant == SUB_COMMAND_TYPE_TEXT:
                args["return_msg_key"] = self.handle_text(cmdargs)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

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
        default_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementSlider):
                raise Exception("commands.editslider.elementnotmatch")

            real_default_code = StringWithHash(default_code)
            _ = self.feature.executor.compile_cache.get_runner(real_default_code)
            element.default = real_default_code

            return "commands.editsliderdefault.success"

    def handle_min(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_min 处理 min 子命令

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
        min_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementSlider):
                raise Exception("commands.editslider.elementnotmatch")

            real_min_code = StringWithHash(min_code)
            _ = self.feature.executor.compile_cache.get_runner(real_min_code)
            element.min_val = real_min_code

            return "commands.editslidermin.success"

    def handle_max(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_max 处理 max 子命令

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
        max_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementSlider):
                raise Exception("commands.editslider.elementnotmatch")

            real_max_code = StringWithHash(max_code)
            _ = self.feature.executor.compile_cache.get_runner(real_max_code)
            element.max_val = real_max_code

            return "commands.editslidermax.success"

    def handle_step(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_step 处理 step 子命令

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
                raise Exception("commands.editslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementSlider):
                raise Exception("commands.editslider.elementnotmatch")

            real_step_code = StringWithHash(step_code)
            _ = self.feature.executor.compile_cache.get_runner(real_step_code)
            element.step = real_step_code

            return "commands.editsliderstep.success"

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
                raise Exception("commands.editslider.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementSlider):
                raise Exception("commands.editslider.elementnotmatch")

            real_text_code = StringWithHash(text_code)
            _ = self.feature.executor.compile_cache.get_runner(real_text_code)
            element.text = real_text_code

            return "commands.editslidertext.success"
