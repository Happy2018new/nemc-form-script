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
    ModalFormElementToggle as ModalStorageFormElementToggle,
)

SUB_COMMAND_TYPE_DEFAULT = 1
SUB_COMMAND_TYPE_TEXT = 2
SUB_COMMAND_TYPE_TOOLTIP = 3


class EditToggleHandler:
    """
    EditToggleHandler 是所有 /edittoggle 命令的处理设备
    """

    storage = None  # type: FormStorage | None
    feature = None  # type: FormFeature | None

    def __init__(self, storage, feature):  # type: (FormStorage, FormFeature) -> None
        """初始化并返回一个新的 EditToggleHandler

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
        有必要确保它的上层调用者验证了调用的命令是 /edittoggle

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_DEFAULT:
                args["return_msg_key"] = self.handle_default(cmdargs)
            elif variant == SUB_COMMAND_TYPE_TEXT:
                args["return_msg_key"] = self.handle_text(cmdargs)
            elif variant == SUB_COMMAND_TYPE_TOOLTIP:
                args["return_msg_key"] = self.handle_tooltip(cmdargs)
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
        state_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.edittoggle.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementToggle):
                raise Exception("commands.edittoggle.elementnotmatch")

            real_state_code = StringWithHash(state_code)
            _ = self.feature.executor.compile_cache.get_runner(real_state_code)
            element.default = real_state_code

            return "commands.edittoggledefault.success"

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
                raise Exception("commands.edittoggle.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementToggle):
                raise Exception("commands.edittoggle.elementnotmatch")

            real_text_code = StringWithHash(text_code)
            _ = self.feature.executor.compile_cache.get_runner(real_text_code)
            element.text = real_text_code

            return "commands.edittoggletext.success"

    def handle_tooltip(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_tooltip 处理 tooltip 子命令

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
        tooltip_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.edittoggle.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementToggle):
                raise Exception("commands.edittoggle.elementnotmatch")

            if len(tooltip_code) == 0:
                element.tooltip = StringWithHash("return ''")
            else:
                real_tooltip_code = StringWithHash(tooltip_code)
                _ = self.feature.executor.compile_cache.get_runner(real_tooltip_code)
                element.tooltip = real_tooltip_code

            return "commands.edittoggletooltip.success"
