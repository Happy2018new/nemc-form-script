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
    ModalFormElementLabel as ModalStorageFormElementLabel,
)

SUB_COMMAND_TYPE_LABEL = 1


class EditLabelHandler:
    """
    EditLabelHandler 是所有 /editlabel 命令的处理设备
    """

    storage = None  # type: FormStorage | None
    feature = None  # type: FormFeature | None

    def __init__(self, storage, feature):  # type: (FormStorage, FormFeature) -> None
        """初始化并返回一个新的 EditLabelHandler

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
        有必要确保它的上层调用者验证了调用的命令是 /editlabel

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_LABEL:
                args["return_msg_key"] = self.handle_label(cmdargs)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

    def handle_label(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_label 处理 label 子命令

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
        label_code = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的模态表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, ModalStorageForm):
                raise Exception("commands.editlabel.formnotmatch")

            if index < 0 or index >= len(form.content):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.content))
                )
            element = form.content[index]
            if not isinstance(element, ModalStorageFormElementLabel):
                raise Exception("commands.editlabel.elementnotmatch")

            real_label_code = StringWithHash(label_code)
            _ = self.feature.executor.compile_cache.get_runner(real_label_code)
            element.text = real_label_code

            return "commands.editlabel.success"
