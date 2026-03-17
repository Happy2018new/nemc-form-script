# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from mod.server.extraServerApi import ServerSystem

import threading
import json
from mod.server.extraServerApi import GetEngineNamespace, GetEngineSystemName
from ..storage.base import StringWithHash
from ..storage.event import EventFuncData, EventStorage
from ..executor.executor import GameCodeExecutor


class SingleEventProcesser:
    """SingleEventProcesser 是单个事件的处理器"""

    storage = None  # type: EventStorage | None
    executor = None  # type: GameCodeExecutor | None
    event_name = ""  # type: str

    def __init__(
        self, storage, executor, event_name
    ):  # type: (EventStorage, GameCodeExecutor, str) -> None
        """初始化并返回一个新的 SingleEventProcesser

        Args:
            storage (EventStorage):
                所有事件的存储管理器
            executor (GameCodeExecutor):
                用户代码的执行器
            event_name (str):
                该处理器所负责的事件
        """
        self.storage = storage
        self.executor = executor
        self.event_name = event_name

    def callback(self, args=None):  # type: (dict[str, Any] | None) -> None
        """
        callback 是相应事件被触发时调用的回调函数

        Args:
            args (dict[str, Any] | None):
                MC 引擎传入的字典参数。
                默认值为 None
        """
        assert self.storage is not None
        assert self.executor is not None
        assert self.executor.static_builtin is not None
        assert self.executor.static_builtin.manager is not None

        with self.storage.get_locker():
            manager = self.executor.static_builtin.manager

            funcs = self.storage.get_funcs(self.event_name)
            if funcs is None:
                return
            if args is None:
                args = {}

            with self.executor.get_locker():
                for _, func in tuple(funcs.items()):
                    try:
                        _ = self.executor.run_code(
                            code=func.get_func(),
                            variables={"args": manager.ref(args)},
                            require_return=False,
                        )
                    except Exception as e:
                        try:
                            _ = self.executor.run_code(
                                code=func.get_on_error(),
                                variables={
                                    "error": str(e),
                                    "args": manager.ref(args),
                                },
                                require_return=False,
                            )
                        except Exception:
                            pass
                    if args.get("cancel", False):
                        break


class EventFeature:
    """
    EventFeature 实现了事件侦听系统的主要特性。
    确保 EventFeature 的实现是线程安全的，
    并且仅会对不同线程之间的调用产生互斥作用
    """

    system = None  # type: ServerSystem | None
    storage = None  # type: EventStorage | None
    executor = None  # type: GameCodeExecutor | None
    _handlers = {}  # type: dict[str, SingleEventProcesser]
    _locker = None  # type: threading.RLock | None

    def __init__(
        self, system, storage, executor
    ):  # type: (ServerSystem, EventStorage, GameCodeExecutor) -> None
        """初始化并返回一个新的 EventFeature

        Args:
            system (ServerSystem):
                当前模组的服务端实现
            storage (EventStorage):
                所有事件的存储管理器
            executor (GameCodeExecutor):
                用户代码的执行器
        """
        self.system = system
        self.storage = storage
        self.executor = executor
        self._handlers = {}
        self._locker = threading.RLock()
        self._dynamic_init()

    def _dynamic_init(self):  # type: () -> None
        """
        _dynamic_init 初始化和设置
        与事件侦听有关的动态内建函数
        """
        assert self.executor is not None
        assert self.executor.static_builtin is not None
        assert self.executor.static_builtin.manager is not None

        manager = self.executor.static_builtin.manager
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["event.list"] = lambda event_name="": manager.ref(
            self.list_event(event_name)
        )
        funcs["event.listen"] = self.listen
        funcs["event.destroy"] = self.destroy

        with self.executor.get_locker():
            _ = self.executor.inject_func(funcs)

    def _create_listener(self, event_name):  # type: (str) -> EventFeature
        """
        _create_listener 为给定的事件注册侦听器

        Args:
            event_name (str):
                给定的事件名

        Returns:
            EventFeature: 返回 EventFeature 本身
        """
        assert self.system is not None
        assert self.storage is not None
        assert self.executor is not None

        processer = SingleEventProcesser(self.storage, self.executor, event_name)
        self.system.ListenForEvent(
            GetEngineNamespace(),
            GetEngineSystemName(),
            event_name,
            processer,
            processer.callback,  # type: ignore
            priority=0,
        )
        self._handlers[event_name] = processer

        return self

    def prepare(self):  # type: () -> EventFeature
        """
        prepare 为所有待注册的事件注册相应的侦听器。
        prepare 函数应当只在该模组被初始化时调用

        Returns:
            EventFeature: 返回 EventFeature 本身
        """
        assert self.storage is not None
        assert self._locker is not None

        with self.storage.get_locker():
            with self._locker:
                for event_name in self.storage.all_index():
                    _ = self._create_listener(event_name)
                return self

    def listen(
        self, event_name, func_name, func_code, on_error
    ):  # type: (str, str, str, str) -> bool
        """
        listen 将指定的事件函数注册在给定的事件下

        Args:
            event_name (str):
                目标事件函数所要监听的事件名
            func_name (str):
                目标事件函数的名称
            func_code (str):
                目标事件函数的代码
            on_error (str):
                当目标事件函数执行发生错误时，
                要执行的错误处理代码

        Raises:
            Exception:
                如果给出的名称已被使用，
                或给出的代码存在语法错误，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        assert self.system is not None
        assert self.storage is not None
        assert self.executor is not None
        assert self.executor.compile_cache is not None
        assert self._locker is not None

        with self.storage.get_locker():
            resp = self.storage.event_name(func_name)
            if resp is not None:
                raise Exception(
                    "listen: Function {} is already registered under event {}".format(
                        json.dumps(func_name, ensure_ascii=False),
                        json.dumps(resp, ensure_ascii=False),
                    )
                )

            func = StringWithHash(func_code)
            onerr = StringWithHash(on_error)
            _ = self.executor.compile_cache.get_runner(func)
            _ = self.executor.compile_cache.get_runner(onerr)

            with self._locker:
                if event_name not in self._handlers:
                    _ = self._create_listener(event_name)
                _ = self.storage.save_func(
                    event_name, func_name, EventFuncData(func, onerr)
                )
            return True

    def destroy(self, func_name):  # type: (str) -> bool
        """
        destroy 销毁 func_name 所指示的事件函数。
        这意味着该事件函数将不再侦听对应的事件

        Args:
            func_name (str):
                事件函数的名称

        Raises:
            Exception:
                如果给定的事件函数不存在，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        assert self.system is not None
        assert self.storage is not None
        assert self._locker is not None

        with self.storage.get_locker():
            event_name = self.storage.event_name(func_name)
            if event_name is None:
                raise Exception(
                    "destroy: Function {} not found".format(
                        json.dumps(func_name, ensure_ascii=False)
                    )
                )

            if self.storage.remove_func(func_name):
                with self._locker:
                    processer = self._handlers[event_name]
                    self.system.UnListenForEvent(
                        GetEngineNamespace(),
                        GetEngineSystemName(),
                        event_name,
                        processer,
                        processer.callback,  # type: ignore
                    )
                    del self._handlers[event_name]

            return True

    def list_event(
        self, event_name=""
    ):  # type: (str) -> dict[str, set[str]] | set[str]
        """
        list_event 列出所有事件，
        或列出侦听给定事件的所有事件函数

        Args:
            event_name (str, optional):
                要查询的目标事件名。
                如果为空，则列出所有事件。
                默认值为空字符串

        Returns:
            dict[str, set[str]] | set[str]:
                当 event_name 为空时返回前者，键是事件名，值是所有侦听该事件的事件函数；
                否则，返回后者，指示所有侦听 event_name 事件的事件函数
        """
        assert self.storage is not None
        assert self.executor is not None

        with self.storage.get_locker():
            all_index = self.storage.all_index()
            if len(event_name) == 0:
                return all_index
            return all_index.get(event_name, set())
