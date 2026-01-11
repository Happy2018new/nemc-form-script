# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from ..feature.form import FormFeature
from ..storage.base import StringWithHash
from ..storage.form import FormStorage
from ..storage.form_struct.popup import PopupForm as PopupStorageForm

SUB_COMMAND_TYPE_FIRST_BUTTON = 1
SUB_COMMAND_TYPE_SECOND_BUTTON = 2
SUB_COMMAND_TYPE_CONTENT = 3
SUB_COMMAND_TYPE_TITLE = 4


class EditPopupFormHandler:
    """
    EditPopupFormHandler 是所有 /editpopupform 命令的处理设备
    """

    storage = None  # type: FormStorage | None
    feature = None  # type: FormFeature | None

    def __init__(self, storage, feature):  # type: (FormStorage, FormFeature) -> None
        """初始化并返回一个新的 EditPopupFormHandler

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
        有必要确保它的上层调用者验证了调用的命令是 /editpopupform

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_FIRST_BUTTON:
                args["return_msg_key"] = self.handle_first_button(cmdargs)
            elif variant == SUB_COMMAND_TYPE_SECOND_BUTTON:
                args["return_msg_key"] = self.handle_second_button(cmdargs)
            elif variant == SUB_COMMAND_TYPE_CONTENT:
                args["return_msg_key"] = self.handle_content(cmdargs)
            elif variant == SUB_COMMAND_TYPE_TITLE:
                args["return_msg_key"] = self.handle_title(cmdargs)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

    def handle_first_button(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_first_button 处理 button1 子命令

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
        first_button_code = args[2]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的信息表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, PopupStorageForm):
                raise Exception("commands.editpopupform.formnotmatch")

            real_first_button_code = StringWithHash(first_button_code)
            _ = self.feature.executor.compile_cache.get_runner(real_first_button_code)
            form.button1 = real_first_button_code

            return "commands.editpopupformbutton1.success"

    def handle_second_button(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_second_button 处理 button2 子命令

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
        second_button_code = args[2]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的信息表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, PopupStorageForm):
                raise Exception("commands.editpopupform.formnotmatch")

            real_second_button_code = StringWithHash(second_button_code)
            _ = self.feature.executor.compile_cache.get_runner(real_second_button_code)
            form.button2 = real_second_button_code

            return "commands.editpopupformbutton2.success"

    def handle_content(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_content 处理 content 子命令

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
        content_code = args[2]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的信息表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, PopupStorageForm):
                raise Exception("commands.editpopupform.formnotmatch")

            real_content_code = StringWithHash(content_code)
            _ = self.feature.executor.compile_cache.get_runner(real_content_code)
            form.content = real_content_code

            return "已成功设置信息表单 {} 的内容文本".format(
                json.dumps(form_name, ensure_ascii=False)
            )

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
                    "名为 {} 的信息表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, PopupStorageForm):
                raise Exception("commands.editpopupform.formnotmatch")

            real_title_code = StringWithHash(title_code)
            _ = self.feature.executor.compile_cache.get_runner(real_title_code)
            form.title = real_title_code

            return "已成功设置信息表单 {} 的标题文本".format(
                json.dumps(form_name, ensure_ascii=False)
            )
