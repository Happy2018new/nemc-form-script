# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from ..feature.function import FunctionFeature
from ..storage.function import FunctionStorage

SUB_COMMAND_TYPE_ADD = 1
SUB_COMMAND_TYPE_CALL = 2
SUB_COMMAND_TYPE_LIST = 3
SUB_COMMAND_TYPE_REMOVE = 4


class CustomFunctionHandler:
    """
    CustomFunctionHandler 是所有 /customfunction 命令的处理设备
    """

    storage = None  # type: FunctionStorage | None
    feature = None  # type: FunctionFeature | None

    def __init__(
        self, storage, feature
    ):  # type: (FunctionStorage, FunctionFeature) -> None
        """初始化并返回一个新的 CustomFunctionHandler

        Args:
            storage (FunctionStorage):
                所有自定义函数的存储管理器
            feature (FunctionFeature):
                自定义函数系统的主要实现
        """
        self.storage = storage
        self.feature = feature

    def on_custom_command_trigger(self, args):  # type: (dict[str, Any]) -> None
        """
        on_custom_command_trigger 在自定义命令被触发时调用。
        有必要确保它的上层调用者验证了调用的命令是 /customfunction

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
            elif variant == SUB_COMMAND_TYPE_CALL:
                args["return_msg_key"] = self.handle_call(cmdargs, dimension)
            elif variant == SUB_COMMAND_TYPE_LIST:
                args["return_msg_key"] = self.handle_list(cmdargs)
            elif variant == SUB_COMMAND_TYPE_REMOVE:
                args["return_msg_key"] = self.handle_remove(cmdargs)
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
        assert self.feature is not None

        func_name = args[1]["value"]  # type: str
        func_code = args[2]["value"]  # type: str

        if len(func_name) == 0:
            raise Exception("自定义函数的名称不得为空")
        _ = self.feature.register(func_name, func_code)

        return "已成功创建名为 {} 的自定义函数".format(
            json.dumps(func_name, ensure_ascii=False)
        )

    def handle_call(self, args, dimension):  # type: (list[dict[str, Any]], int) -> str
        """handle_call 处理 call 子命令

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
        assert self.feature.executor is not None

        executor = args[1]["value"]  # type: tuple[str, ...] | None
        position = args[2]["value"]  # type: tuple[float, float, float]
        func_name = args[3]["value"]  # type: str

        if executor is None:
            raise Exception("commands.generic.noTargetMatch")
        if len(executor) != 1:
            raise Exception("您最多设置一个命令执行者")

        with self.feature.executor.get_locker():
            context = self.feature.executor.execute_context()
            backup = context.current_context()
            try:
                context.set_executor(executor[0])
                context.set_dimension(dimension)
                context.set_position(*position)
                _ = self.feature.call(func_name)
            finally:
                context.recover_context(backup)

        return "已执行名为 {} 的自定义函数".format(
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
        func_name = args[1]["value"]  # type: str

        resp = self.feature.list_all(func_name)

        if isinstance(resp, set):
            if len(resp) == 0:
                return "当前没有已注册的自定义函数"
            result = "当前已注册了 {} 个自定义函数: ".format(len(resp))
            for i in sorted(list(resp)):
                result += "\n  - {}".format(i)
            return result

        if not resp:
            return "不存在名为 {} 的自定义函数".format(
                json.dumps(func_name, ensure_ascii=False)
            )
        return "已找到名为 {} 的自定义函数".format(
            json.dumps(func_name, ensure_ascii=False)
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
        assert self.feature is not None
        func_name = args[1]["value"]  # type: str

        _ = self.feature.unregister(func_name)
        return "已成功移除名为 {} 的自定义函数".format(
            json.dumps(func_name, ensure_ascii=False)
        )
