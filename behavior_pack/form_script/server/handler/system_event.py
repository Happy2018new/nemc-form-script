# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from ..feature.event import EventFeature
from ..storage.event import EventStorage

SUB_COMMAND_TYPE_DESTROY = 1
SUB_COMMAND_TYPE_LIST = 2
SUB_COMMAND_TYPE_LISTEN = 3
SUB_COMMAND_TYPE_QUERY = 4


class SystemEventHandler:
    """
    SystemEventHandler 是所有 /systemevent 命令的处理设备
    """

    storage = None  # type: EventStorage | None
    feature = None  # type: EventFeature | None

    def __init__(self, storage, feature):  # type: (EventStorage, EventFeature) -> None
        """初始化并返回一个新的 SystemEventHandler

        Args:
            storage (EventStorage):
                所有事件的存储管理器
            feature (EventFeature):
                事件侦听系统的主要实现
        """
        self.storage = storage
        self.feature = feature

    def on_custom_command_trigger(self, args):  # type: (dict[str, Any]) -> None
        """
        on_custom_command_trigger 在自定义命令被触发时调用。
        有必要确保它的上层调用者验证了调用的命令是 /systemevent

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_DESTROY:
                args["return_msg_key"] = self.handle_destroy(cmdargs)
            elif variant == SUB_COMMAND_TYPE_LIST:
                args["return_msg_key"] = self.handle_list(cmdargs)
            elif variant == SUB_COMMAND_TYPE_LISTEN:
                args["return_msg_key"] = self.handle_listen(cmdargs)
            elif variant == SUB_COMMAND_TYPE_QUERY:
                args["return_msg_key"] = self.handle_query(cmdargs)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

    def handle_destroy(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_destroy 处理 destroy 子命令

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
        func_name = args[1]["value"]  # type: str

        _ = self.feature.destroy(func_name)
        return "已成功移除名为 {} 的事件函数".format(
            json.dumps(func_name, ensure_ascii=False)
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
        event_name = args[1]["value"]  # type: str

        resp = self.feature.list_event(event_name)
        if isinstance(resp, set):
            if len(resp) == 0:
                return "没有任何事件函数侦听了目标事件"
            else:
                result = "共有 {} 个事件函数侦听了目标事件: ".format(len(resp))
                for i in sorted(list(resp)):
                    result += "\n  - {}".format(i)
                return result

        if len(resp) == 0:
            return "当前没有侦听任何事件"
        else:
            result = "当前侦听了 {} 个事件: ".format(len(resp))
            for i in sorted(list(resp.items()), key=lambda x: x[0]):
                result += "\n  - 事件 {} ({} 个)".format(i[0], len(i[1]))
                for j in sorted(list(i[1])):
                    result += "\n    - {}".format(j)
            return result

    def handle_listen(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_listen 处理 listen 子命令

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

        event_name = args[1]["value"]  # type: str
        func_name = args[2]["value"]  # type: str
        func_code = args[3]["value"]  # type: str
        on_code_err = args[4]["value"]  # type: str

        if len(event_name) == 0:
            raise Exception("欲侦听的事件名不得为空")
        if len(func_name) == 0:
            raise Exception("事件函数的名称不得为空")
        _ = self.feature.listen(event_name, func_name, func_code, on_code_err)

        return "已成功将事件函数 {} 侦听在事件 {} 上".format(
            json.dumps(func_name, ensure_ascii=False),
            json.dumps(event_name, ensure_ascii=False),
        )

    def handle_query(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_query 处理 query 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Returns:
            str: 命令执行输出
        """
        assert self.storage is not None
        func_name = args[1]["value"]  # type: str

        with self.storage.get_locker():
            event_name = self.storage.event_name(func_name)
            if event_name is None:
                return "名为 {} 的事件函数不存在".format(
                    json.dumps(func_name, ensure_ascii=False)
                )
            return "名为 {} 的事件函数侦听在事件 {} 上".format(
                json.dumps(func_name, ensure_ascii=False),
                json.dumps(event_name, ensure_ascii=False),
            )
