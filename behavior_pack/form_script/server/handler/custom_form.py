# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from ..feature.form import FormFeature
from ..storage.base import StringWithHash
from ..storage.form import (
    FORM_TYPE_LONG as FORM_STORAGE_TYPE_LONG,
    FORM_TYPE_POPUP as FORM_STORAGE_TYPE_POPUP,
    FORM_TYPE_MODAL as FORM_STORAGE_TYPE_MODAL,
    FormStorage,
)
from ..storage.form_struct.long import LongForm as LongStorageForm
from ..storage.form_struct.popup import PopupForm as PopupStorageForm
from ..storage.form_struct.modal import ModalForm as ModalStorageForm

SUB_COMMAND_TYPE_ADD = 1
SUB_COMMAND_TYPE_LIST = 2
SUB_COMMAND_TYPE_ONCANCEL = 3
SUB_COMMAND_TYPE_ONSUBMIT = 4
SUB_COMMAND_TYPE_REMOVE = 5
SUB_COMMAND_TYPE_SAVE = 6
SUB_COMMAND_TYPE_SHOW = 7
SUB_COMMAND_TYPE_CLOSE = 8

FORM_RAW_TYPE_LONG = "long"
FORM_RAW_TYPE_POPUP = "popup"
FORM_RAW_TYPE_MODAL = "modal"


class CustomFormHandler:
    """
    CustomFormHandler 是所有 /customform 命令的处理设备
    """

    storage = None  # type: FormStorage | None
    feature = None  # type: FormFeature | None

    def __init__(self, storage, feature):  # type: (FormStorage, FormFeature) -> None
        """初始化并返回一个新的 CustomFormHandler

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
        有必要确保它的上层调用者验证了调用的命令是 /customform

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]
        dimension = args["origin"]["dimension"]  # type: int

        try:
            if variant == SUB_COMMAND_TYPE_ADD:
                args["return_msg_key"] = self.handle_add(cmdargs)
            elif variant == SUB_COMMAND_TYPE_LIST:
                args["return_msg_key"] = self.handle_list(cmdargs)
            elif variant == SUB_COMMAND_TYPE_ONCANCEL:
                args["return_msg_key"] = self.handle_on_cancel(cmdargs)
            elif variant == SUB_COMMAND_TYPE_ONSUBMIT:
                args["return_msg_key"] = self.handle_on_submit(cmdargs)
            elif variant == SUB_COMMAND_TYPE_REMOVE:
                args["return_msg_key"] = self.handle_remove(cmdargs)
            elif variant == SUB_COMMAND_TYPE_SAVE:
                args["return_msg_key"] = self.handle_save(cmdargs)
            elif variant == SUB_COMMAND_TYPE_SHOW:
                args["return_msg_key"] = self.handle_show(cmdargs, dimension)
            elif variant == SUB_COMMAND_TYPE_CLOSE:
                args["return_msg_key"] = self.handle_close(cmdargs)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

    def handle_add(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_add 处理 add 子命令

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

        form_name = args[1]["value"]  # type: str
        form_type = args[2]["value"]  # type: str

        with self.storage.get_locker():
            if len(form_name) == 0:
                raise Exception("表单名称不得为空")
            if self.storage.form_type(form_name) is not None:
                raise Exception(
                    "名为 {} 的表单已经存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )

            if form_type == FORM_RAW_TYPE_LONG:
                real_form = LongStorageForm(
                    StringWithHash("return ''"),
                    StringWithHash("return ''"),
                    [],
                    StringWithHash(""),
                    StringWithHash(""),
                    StringWithHash(""),
                    StringWithHash(""),
                )
                _ = self.storage.cache_form(form_name, real_form)
            elif form_type == FORM_RAW_TYPE_POPUP:
                real_form = PopupStorageForm(
                    StringWithHash("return ''"),
                    StringWithHash("return ''"),
                    StringWithHash("return ''"),
                    StringWithHash("return ''"),
                    StringWithHash(""),
                    StringWithHash(""),
                    StringWithHash(""),
                    StringWithHash(""),
                )
                _ = self.storage.cache_form(form_name, real_form)
            elif form_type == FORM_RAW_TYPE_MODAL:
                real_form = ModalStorageForm(
                    StringWithHash("return ''"),
                    [],
                    StringWithHash(""),
                    StringWithHash(""),
                    StringWithHash(""),
                    StringWithHash(""),
                )
                _ = self.storage.cache_form(form_name, real_form)

            return "已成功创建名为 {} 的表单".format(
                json.dumps(form_name, ensure_ascii=False)
            )

    def handle_list(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_list 处理 list 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Returns:
            str: 命令执行输出
        """
        assert self.feature is not None
        form_name = args[1]["value"]  # type: str

        resp = self.feature.list_form(form_name)
        if resp is None:
            return "没有找到名为 {} 的表单".format(
                json.dumps(form_name, ensure_ascii=False)
            )

        if isinstance(resp, dict):
            if len(resp) == 0:
                return "当前没有已注册的表单"
            result = "当前已注册了 {} 个表单: ".format(len(resp))
            for key, value in sorted(list(resp.items()), key=lambda x: x[0]):
                result += "\n  - {}: ".format(key)
                if value == FORM_STORAGE_TYPE_LONG:
                    result += "长表单"
                elif value == FORM_STORAGE_TYPE_POPUP:
                    result += "信息表单"
                elif value == FORM_STORAGE_TYPE_MODAL:
                    result += "模态表单"
            return result

        result = "名为 {} 的表单的类型为".format(
            json.dumps(form_name, ensure_ascii=False)
        )
        if resp == FORM_STORAGE_TYPE_LONG:
            result += "长表单"
        elif resp == FORM_STORAGE_TYPE_POPUP:
            result += "信息表单"
        elif resp == FORM_STORAGE_TYPE_MODAL:
            result += "模态表单"
        return result

    def handle_on_cancel(self, args):  # type: (list[dict[str, Any]]) -> str
        """
        handle_on_cancel 处理 oncancel 子命令

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

        name = args[1]["value"]  # type: str
        code = args[2]["value"]  # type: str
        onerror = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(name)
            if form is None:
                raise Exception(
                    "名为 {} 的表单不存在".format(json.dumps(name, ensure_ascii=False))
                )

            real_code = StringWithHash(code)
            real_onerror = StringWithHash(onerror)
            _ = self.feature.executor.compile_cache.get_runner(real_code)
            _ = self.feature.executor.compile_cache.get_runner(real_onerror)

            if isinstance(form, LongStorageForm):
                form.oncancel = real_code
                form.oncanerr = real_onerror
            elif isinstance(form, PopupStorageForm):
                form.oncancel = real_code
                form.oncanerr = real_onerror
            elif isinstance(form, ModalStorageForm):
                form.oncancel = real_code
                form.oncanerr = real_onerror

            return "已成功为表单 {} 设置当其被玩家关闭时应执行的代码".format(
                json.dumps(name, ensure_ascii=False)
            )

    def handle_on_submit(self, args):  # type: (list[dict[str, Any]]) -> str
        """
        handle_on_submit 处理 onsubmit 子命令

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

        name = args[1]["value"]  # type: str
        code = args[2]["value"]  # type: str
        onerror = args[3]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.get_form(name)
            if form is None:
                raise Exception(
                    "名为 {} 的表单不存在".format(json.dumps(name, ensure_ascii=False))
                )

            real_code = StringWithHash(code)
            real_onerror = StringWithHash(onerror)
            _ = self.feature.executor.compile_cache.get_runner(real_code)
            _ = self.feature.executor.compile_cache.get_runner(real_onerror)

            if isinstance(form, LongStorageForm):
                form.onsubmit = real_code
                form.onsuberr = real_onerror
            elif isinstance(form, PopupStorageForm):
                form.onsubmit = real_code
                form.onsuberr = real_onerror
            elif isinstance(form, ModalStorageForm):
                form.onsubmit = real_code
                form.onsuberr = real_onerror

            return "已成功为表单 {} 设置当其被玩家提交时应执行的代码".format(
                json.dumps(name, ensure_ascii=False)
            )

    def handle_remove(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_remove 处理 remove 子命令

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
        form_name = args[1]["value"]  # type: str

        with self.storage.get_locker():
            if self.storage.form_type(form_name) is None:
                raise Exception(
                    "名为 {} 的表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            _ = self.storage.remove_form(form_name)
            return "已成功移除名为 {} 的表单".format(
                json.dumps(form_name, ensure_ascii=False)
            )

    def handle_save(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_save 处理 save 子命令

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
        form_name = args[1]["value"]  # type: str

        with self.storage.get_locker():
            form = self.storage.form_type(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            _ = self.storage.save_form(form_name)
            return "已成功将 {} 保存到磁盘".format(
                json.dumps(form_name, ensure_ascii=False)
            )

    def handle_show(self, args, dimension):  # type: (list[dict[str, Any]], int) -> str
        """handle_show 处理 show 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表
            dimension (int):
                在生成表单时需要执行代码，
                而执行代码需要指定命令执行上下文，
                因此该字段的用途是指定命令执行维度

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.feature is not None

        executor = args[1]["value"]  # type: tuple[str, ...] | None
        position = args[2]["value"]  # type: tuple[float, float, float]
        player = args[3]["value"]  # type: tuple[str, ...] | None
        name = args[4]["value"]  # type: str

        if executor is None or player is None:
            raise Exception("commands.generic.noTargetMatch")
        if len(executor) != 1:
            raise Exception("您最多设置一个命令执行者")
        _ = self.feature.send_modal_form_request(
            list(player), name, executor[0], dimension, position
        )

        return "commands.customformshow.success"

    def handle_close(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_close 处理 close 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.feature is not None
        player = args[1]["value"]  # type: tuple[str, ...] | None

        if player is None:
            raise Exception("commands.generic.noTargetMatch")
        _ = self.feature.force_close_all_forms(list(player))

        return "commands.customformclose.success"
