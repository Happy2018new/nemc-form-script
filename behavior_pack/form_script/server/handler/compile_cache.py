# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from ..storage.base import StringWithHash
from ..executor.cache import CompileCache

SUB_COMMAND_TYPE_COMPILE = 1
SUB_COMMAND_TYPE_QUERY = 2
SUB_COMMAND_TYPE_SET = 3


class CompileCacheHandler:
    """
    CompileCacheHandler 是所有 /compilecache 命令的处理设备
    """

    compile_cache = None  # type: CompileCache | None

    def __init__(self, compile_cache):  # type: (CompileCache) -> None
        """
        初始化并返回一个新的 CompileCacheHandler

        Args:
            compile_cache (CompileCache):
                代码编译的缓存管理器
        """
        self.compile_cache = compile_cache

    def on_custom_command_trigger(self, args):  # type: (dict[str, Any]) -> None
        """
        on_custom_command_trigger 在自定义命令被触发时调用。
        有必要确保它的上层调用者验证了调用的命令是 /compilecache

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        variant = args["variant"]  # type: int
        cmdargs = args["args"]  # type: list[dict[str, Any]]

        try:
            if variant == SUB_COMMAND_TYPE_COMPILE:
                args["return_msg_key"] = self.handle_compile(cmdargs)
            elif variant == SUB_COMMAND_TYPE_QUERY:
                args["return_msg_key"] = self.handle_query(cmdargs)
            elif variant == SUB_COMMAND_TYPE_SET:
                args["return_msg_key"] = self.handle_set(cmdargs)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

    def handle_compile(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_compile 处理 compile 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.compile_cache is not None
        code = args[1]["value"]  # type: str

        _ = self.compile_cache.get_runner(StringWithHash(code))
        return "commands.compilecachecompile.success"

    def handle_query(self, _):  # type: (list[dict[str, Any]]) -> str
        """handle_query 处理 query 子命令

        Args:
            _ (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Returns:
            str: 命令执行输出
        """
        assert self.compile_cache is not None

        return "预编译缓存区已存在 {} 个缓存，最多存在 {} 个".format(
            self.compile_cache.get_current_cache_size(),
            self.compile_cache.get_max_cache_size(),
        )

    def handle_set(self, args):  # type: (list[dict[str, Any]]) -> str
        """handle_set 处理 set 子命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self.compile_cache is not None
        size = args[1]["value"]  # type: int

        _ = self.compile_cache.set_max_cache_size(size)
        return "commands.compilecacheset.success"
