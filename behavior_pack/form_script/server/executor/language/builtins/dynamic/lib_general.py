# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable
    from mod.server.extraServerApi import ServerSystem

from mod.server.extraServerApi import (
    GetEngineNamespace,
    GetEngineSystemName,
    GetMinecraftVersion,
    GetPlatform,
    GetHostPlayerId,
    GetServerTickTime,
)
from ..static.lib_object import BaseManager


class General:
    """
    General 导出了 Mod SDK 中通用模块的部分接口
    """

    _manager = BaseManager()  # type: BaseManager
    _system = None  # type: ServerSystem | None

    def __init__(self, manager, system):  # type: (BaseManager, ServerSystem) -> None
        """初始化并返回一个新的 General

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
            system (ServerSystem):
                当前模组的服务端实现
        """
        self._manager = manager
        self._system = system

    def broadcast_event(self, event_name, event_data_ptr):  # type: (str, int) -> bool
        """broadcast_event 在本地服务端广播事件

        Args:
            event_name (str):
                要广播的事件的名称
            event_data_ptr (int):
                事件负载的指针

        Returns:
            bool: 总是返回 True
        """
        assert self._system is not None
        self._system.BroadcastEvent(event_name, self._manager.deref(event_data_ptr))
        return True

    def broadcast_to_all_client(
        self, event_name, event_data_ptr
    ):  # type: (str, int) -> bool
        """broadcast_to_all_client 广播事件到所有客户端

        Args:
            event_name (str):
                要广播的事件的名称
            event_data_ptr (int):
                事件负载的指针

        Returns:
            bool: 总是返回 True
        """
        assert self._system is not None
        self._system.BroadcastToAllClient(
            event_name, self._manager.deref(event_data_ptr)
        )
        return True

    def notify_to_client(
        self, target_id, event_name, event_data_ptr
    ):  # type: (str, str, int) -> bool
        """notify_to_client 发送事件到指定客户端

        Args:
            target_id (str):
                接收者（玩家）的 ID
            event_name (str):
                事件的名称
            event_data_ptr (int):
                事件负载的指针

        Returns:
            bool: 总是返回 True
        """
        assert self._system is not None
        self._system.NotifyToClient(
            target_id, event_name, self._manager.deref(event_data_ptr)
        )
        return True

    def notify_to_multi_clients(
        self, multiple_id_ptr, event_name, event_data_ptr
    ):  # type: (int, str, int) -> bool
        """notify_to_multi_clients 发送事件到多个客户端

        Args:
            multiple_id_ptr (int):
                多个接收者（玩家）的 ID。
                应是一个指向列表的指针
            event_name (str):
                事件的名称
            event_data_ptr (int):
                事件负载的指针

        Returns:
            bool: 总是返回 True
        """
        assert self._system is not None
        self._system.NotifyToMultiClients(
            self._manager.deref(multiple_id_ptr),
            event_name,
            self._manager.deref(event_data_ptr),
        )
        return True

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 general 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["general.BroadcastEvent"] = self.broadcast_event
        funcs["general.BroadcastToAllClient"] = self.broadcast_to_all_client
        funcs["general.GetEngineNamespace"] = lambda: self._manager.ref(
            GetEngineNamespace()
        )
        funcs["general.GetEngineSystemName"] = lambda: self._manager.ref(
            GetEngineSystemName()
        )
        funcs["general.NotifyToClient"] = self.notify_to_client
        funcs["general.NotifyToMultiClients"] = self.notify_to_multi_clients
        funcs["general.GetMinecraftVersion"] = lambda: self._manager.ref(
            GetMinecraftVersion()
        )
        funcs["general.GetPlatform"] = lambda: self._manager.ref(GetPlatform())
        funcs["general.GetHostPlayerId"] = lambda: self._manager.ref(GetHostPlayerId())
        funcs["general.GetServerTickTime"] = lambda: self._manager.ref(
            GetServerTickTime()
        )

        for key, value in funcs.items():
            origin[key] = value
