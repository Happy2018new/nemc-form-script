# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from ..feature.form import FormFeature
from ..storage.base import StringWithHash
from ..storage.form import FormStorage
from ..storage.form_struct.long import (
    LongForm as LongStorageForm,
    LongFormElement as LongStorageFormElement,
    LongFormIconPathImage as LongStorageFormIconPathImage,
)

SUB_COMMAND_TYPE_APPEND = 1
SUB_COMMAND_TYPE_CONTENT = 2
SUB_COMMAND_TYPE_INSERT = 3
SUB_COMMAND_TYPE_LIST = 4
SUB_COMMAND_TYPE_POP = 5
SUB_COMMAND_TYPE_SUB = 6
SUB_COMMAND_TYPE_TITLE = 7

POP_RAW_ACTION_LEFT = "left"
POP_RAW_ACTION_RIGHT = "right"

SUB_RAW_ACTION_KEEP = "keep"
SUB_RAW_ACTION_DISCARD = "discard"


class EditLongFormHandler:
    """
    EditLongFormHandler 是所有 /editlongform 命令的处理设备
    """

    storage = None  # type: FormStorage | None
    feature = None  # type: FormFeature | None

    def __init__(self, storage, feature):  # type: (FormStorage, FormFeature) -> None
        """初始化并返回一个新的 EditLongFormHandler

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
        有必要确保它的上层调用者验证了调用的命令是 /editlongform

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_APPEND:
                args["return_msg_key"] = self.handle_append(cmdargs)
            elif variant == SUB_COMMAND_TYPE_CONTENT:
                args["return_msg_key"] = self.handle_content(cmdargs)
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

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的长表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, LongStorageForm):
                raise Exception("commands.editlongformappend.failed")
            form.buttons.append(LongStorageFormElement(StringWithHash("return ''")))
            return "已成功向长表单 {} 追加一个按钮".format(
                json.dumps(form_name, ensure_ascii=False)
            )

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
                    "名为 {} 的长表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, LongStorageForm):
                raise Exception("commands.editlongformcontent.failed")

            real_content_code = StringWithHash(content_code)
            _ = self.feature.executor.compile_cache.get_runner(real_content_code)
            form.content = real_content_code

            return "已成功设置长表单 {} 的内容文本".format(
                json.dumps(form_name, ensure_ascii=False)
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

        with self.storage.get_locker():
            form = self.storage.get_form(form_name)
            if form is None:
                raise Exception(
                    "名为 {} 的长表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, LongStorageForm):
                raise Exception("commands.editlongforminsert.failed")

            if index < 0 or index > len(form.buttons):
                raise Exception(
                    "给出的索引 {} 超出长度 {}".format(index, len(form.buttons))
                )
            form.buttons.insert(
                index, LongStorageFormElement(StringWithHash("return ''"))
            )

            return "已成功向长表单 {} 插入按钮".format(
                json.dumps(form_name, ensure_ascii=False)
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
                    "名为 {} 的长表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, LongStorageForm):
                raise Exception("commands.editlongformlist.failed")

            if len(form.buttons) == 0:
                return "长表单 {} 目前没有任何按钮".format(
                    json.dumps(form_name, ensure_ascii=False)
                )
            result = "长表单 {} 目前已存在 {} 个按钮: ".format(
                json.dumps(form_name, ensure_ascii=False), len(form.buttons)
            )
            for i in form.buttons:
                if isinstance(i.icon, LongStorageFormIconPathImage):
                    result += "\n  - 使用材质贴图"
                else:
                    result += "\n  - 无图标"

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
                    "名为 {} 的长表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, LongStorageForm):
                raise Exception("commands.editlongformpop.failed")

            if len(form.buttons) == 0:
                raise Exception(
                    "长表单 {} 没有任何按钮可供移除".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if pop_action == POP_RAW_ACTION_LEFT:
                _ = form.buttons.pop(0)
            elif pop_action == POP_RAW_ACTION_RIGHT:
                _ = form.buttons.pop(-1)

            return "已成功移除长表单 {} 中的最后一个按钮".format(
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
                    "名为 {} 的长表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, LongStorageForm):
                raise Exception("commands.editlongformsub.failed")

            if start_index < 0 or start_index > len(form.buttons):
                raise Exception(
                    "给出的起始索引 {} 超出长度 {}".format(
                        start_index, len(form.buttons)
                    )
                )
            if end_index < 0 or end_index > len(form.buttons):
                raise Exception(
                    "给出的结束索引 {} 超出长度 {}".format(end_index, len(form.buttons))
                )
            if end_index < start_index:
                raise Exception(
                    "给出的结束索引 {} 小于起始索引 {}".format(end_index, start_index)
                )

            if sub_action == SUB_RAW_ACTION_KEEP:
                form.buttons = form.buttons[start_index:end_index]
                return "已成功为长表单 {} 的按钮执行保留的截取操作".format(
                    json.dumps(form_name, ensure_ascii=False)
                )
            elif sub_action == SUB_RAW_ACTION_DISCARD:
                form.buttons = form.buttons[:start_index] + form.buttons[end_index:]
                return "已成功为长表单 {} 的按钮执行丢弃的截取操作".format(
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
                    "名为 {} 的长表单不存在".format(
                        json.dumps(form_name, ensure_ascii=False)
                    )
                )
            if not isinstance(form, LongStorageForm):
                raise Exception("commands.editlongformtitle.failed")

            real_title_code = StringWithHash(title_code)
            _ = self.feature.executor.compile_cache.get_runner(real_title_code)
            form.title = real_title_code

            return "已成功设置长表单 {} 的标题文本".format(
                json.dumps(form_name, ensure_ascii=False)
            )
