# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable
    from mod.server.extraServerApi import ServerSystem

import json
from ..executor.executor import GameCodeExecutor
from ..storage.function import CustomFunction, FunctionStorage


class FunctionFeature:
    """
    FunctionFeature 实现了自定义函数系统的主要特性。
    确保 FunctionFeature 的实现是线程安全的，
    并且仅会对不同线程之间的调用产生互斥作用
    """

    system = None  # type: ServerSystem | None
    storage = None  # type: FunctionStorage | None
    executor = None  # type: GameCodeExecutor | None

    def __init__(
        self, system, storage, executor
    ):  # type: (ServerSystem, FunctionStorage, GameCodeExecutor) -> None
        """初始化并返回一个新的 FunctionFeature

        Args:
            system (ServerSystem):
                当前模组的服务端实现
            storage (FunctionStorage):
                所有自定义函数的存储管理器
            executor (GameCodeExecutor):
                用户代码的执行器
        """
        self.system = system
        self.storage = storage
        self.executor = executor
        self._dynamic_init()

    def _dynamic_init(self):  # type: () -> None
        """
        _dynamic_init 初始化和设置与
        自定义函数有关的动态内建函数
        """
        assert self.executor is not None
        assert self.executor.static_builtin is not None
        assert self.executor.static_builtin.manager is not None

        manager = self.executor.static_builtin.manager
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["function.list"] = lambda: manager.ref(self.list_all())
        funcs["function.register"] = lambda func_name, func_code: self.register(
            func_name, func_code
        )
        funcs["function.unregister"] = lambda func_name: self.unregister(func_name)
        funcs["function.call"] = lambda func_name, *args: self.call(func_name, *args)
        funcs["function.try"] = lambda func_name, *args: self.try_call(func_name, *args)

        with self.executor.get_locker():
            _ = self.executor.inject_func(funcs)

    def register(self, func_name, func_code):  # type: (str, str) -> bool
        """register 注册一个新的自定义函数

        Args:
            func_name (str):
                欲注册的自定义函数的名称
            func_code (str):
                该自定义函数的源代码

        Raises:
            Exception:
                如果给定的名称已被使用，
                或给出的代码存在语法错误，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        assert self.storage is not None
        assert self.executor is not None
        assert self.executor.compile_cache is not None

        with self.storage.get_locker():
            if self.storage.check_exist(func_name):
                raise Exception(
                    "register: Function {} is already registered".format(
                        json.dumps(func_name, ensure_ascii=False)
                    )
                )

            real_func = CustomFunction(func_code)
            _ = self.executor.compile_cache.get_runner(real_func)
            _ = self.storage.save_func(func_name, real_func)

            return True

    def unregister(self, func_name):  # type: (str) -> bool
        """unregister 从底层存储移除一个自定义函数

        Args:
            func_name (str):
                欲移除的自定义函数的名称

        Raises:
            Exception:
                如果目标自定义函数不存在，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        assert self.storage is not None

        with self.storage.get_locker():
            if not self.storage.check_exist(func_name):
                raise Exception(
                    "unregister: Function {} not found".format(
                        json.dumps(func_name, ensure_ascii=False)
                    )
                )
            _ = self.storage.remove_func(func_name)
            return True

    def list_all(self, func_name=""):  # type: (str) -> set[str] | bool
        """
        list_all 列出所有已注册的自定义函数，
        或查询某个指定的自定义函数是否存在

        Args:
            func_name (str, optional):
                要查询的自定义函数的名称。
                将其置空将得到所有自定义函数的名称。
                默认值为空字符串

        Returns:
            set[str] | bool:
                如果 func_name 为空，则返回前者，指示当前已注册的所有函数；
                否则 func_name 非空，那么返回后者，指示给定的函数是否存在
        """
        assert self.storage is not None

        with self.storage.get_locker():
            if len(func_name) == 0:
                return self.storage.func_index()
            return self.storage.check_exist(func_name)

    def call(self, func_name, *args):  # type: (str, ...) -> int | bool | float | str
        """
        call 调用 func_name 指示的自定义函数，
        并将 *args 指示的参数传入到该函数中

        Args:
            func_name (str):
                欲调用的自定义函数的名称

        Raises:
            Exception:
                如果目标自定义函数不存在，
                或执行自定义函数时发生错误，
                则抛出相应的错误

        Returns:
            int | bool | float | str:
                自定义函数的返回值
        """
        assert self.storage is not None
        assert self.executor is not None
        assert self.executor.static_builtin is not None
        assert self.executor.static_builtin.manager is not None

        with self.storage.get_locker():
            func = self.storage.get_func(func_name)
            if func is None:
                raise Exception(
                    "call: Function {} not found".format(
                        json.dumps(func_name, ensure_ascii=False)
                    )
                )

        with self.executor.get_locker():
            context = self.executor.execute_context()
            if len(args) == 0:
                return self.executor.run_code(
                    func,
                    "",
                    context.get_executor(),
                    context.get_dimension(),
                    context.get_position(),
                    True,
                )  # type: ignore
            else:
                return self.executor.variable_run(
                    func,
                    "",
                    context.get_executor(),
                    context.get_dimension(),
                    context.get_position(),
                    {"args": self.executor.static_builtin.manager.ref(args)},
                    True,
                )  # type: ignore

    def try_call(self, func_name, *args):  # type: (str, ...) -> int
        """
        try_call 调用 func_name 指示的自定义函数，
        并将 *args 指示的参数传入到该函数中。

        它与 call 的区别在于，它将返回一个指向二元组的引用。
        其中，第一项指示自定义函数的返回值，第二项指示错误信息。

        这意味着如果自定义函数在执行过程若未出错，则错误信息为空；
        否则，错误信息（字符串）非空，并且元组的第一项为 0

        Args:
            func_name (str):
                欲调用的自定义函数的名称

        Raises:
            Exception:
                如果目标自定义函数不存在，
                则抛出相应的错误

        Returns:
            int: 目标元组的指针
        """
        assert self.executor is not None
        assert self.executor.static_builtin is not None
        assert self.executor.static_builtin.manager is not None

        manager = self.executor.static_builtin.manager
        try:
            result = (self.call(func_name, *args), "")
            with self.executor.get_locker():
                return manager.ref(result)
        except Exception as e:
            err = str(e)
            if len(err) == 0:
                err = "Unknown empty error"
            with self.executor.get_locker():
                return manager.ref((0, err))
