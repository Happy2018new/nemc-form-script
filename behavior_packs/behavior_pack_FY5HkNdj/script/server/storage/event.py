# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import threading
from .function import CustomFunction
from .base import StorageManager


class EventStorage:
    """EventStorage 是所有事件的存储管理器"""

    _event = {}  # type: dict[str, dict[str, CustomFunction]]
    _storage = None  # type: StorageManager | None
    _locker = None  # type: threading.Lock | None

    def __init__(self, storage):  # type: (StorageManager) -> None
        """初始化并返回一个新的事件存储管理器

        Args:
            storage (StorageManager):
                线程安全的底层存储管理器
        """
        self._event = {}
        self._storage = storage
        self._locker = threading.Lock()

    def get_locker(self):  # type: () -> threading.Lock
        """
        get_locker 返回事件存储管理器的锁。
        任何对事件的存储操作都须在锁的上下文内完成

        Returns:
            threading.Lock:
                事件存储管理器的锁
        """
        assert self._locker is not None
        return self._locker

    def event_name(self, func_name):  # type: (str) -> str | None
        """
        event_name 返回给定函数绑定在哪个事件下

        Args:
            func_name (str):
                目标函数名

        Returns:
            str | None:
                如果目标函数存在，则返回对应的事件名；
                否则目标函数不存在，那么返回 None
        """
        if self._storage is None:
            return None
        index = self.func_index()
        if func_name in index:
            return index[func_name]
        return None

    def all_index(self):  # type: () -> dict[str, set[str]]
        """
        all_index 返回所有事件的索引。
        键是事件名，值是该事件下注册的所有函数

        Returns:
            dict[str, set[str]]:
                所有事件的索引
        """
        if self._storage is None:
            return {}

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if root is None:
                return {}

            assert isinstance(root, dict)
            result = root.get("event_all_index", {})  # type: dict[str, dict[str, bool]]
            return {key: set(value) for key, value in result.items()}

    def func_index(self):  # type: () -> dict[str, str]
        """
        func_index 返回所有函数的索引。
        键是自定义函数的名称，
        值是该自定义函数注册时对应的事件名

        Returns:
            dict[str, str]: 所有函数的索引
        """
        if self._storage is None:
            return {}

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if root is None:
                return {}

            assert isinstance(root, dict)
            return root.get("event_func_index", {})

    def load_all(self):  # type: () -> EventStorage
        """
        load_all 从底层存储中加载所有已注册的事件到缓存中

        Returns:
            EventStorage:
                返回 EventStorage 本身
        """
        if self._storage is None:
            return self

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                return self
            data = root.get(
                "event_data", {}
            )  # type: dict[str, dict[str, dict[str, Any]]]

            for key, value in data.items():
                event = {}  # type: dict[str, CustomFunction]
                for k, v in value.items():
                    event[k] = CustomFunction().unmarshal(v)
                self._event[key] = event

            return self

    def get_event(self, event_name):  # type: (str) -> dict[str, CustomFunction] | None
        """
        get_event 从缓存中获取注册在给定事件下的所有函数。
        如果缓存未命中，则从底层存储获取。

        返回的字典不容许进一步修改。
        您只能通过重新构造新的 CustomFunction 实例，
        并通过 save_func 持久化到底层存储

        Args:
            event_name (str): 给定的事件名

        Returns:
            dict[str, CustomFunction] | None:
                如果存在，则返回该事件下的所有函数；
                否则不存在，那么返回 None
        """
        if self._storage is None:
            return None
        if event_name in self._event:
            return self._event[event_name]

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                return None

            data = root.get(
                "event_data", {}
            )  # type: dict[str, dict[str, dict[str, Any]]]
            if event_name not in data:
                return None

            event = {}  # type: dict[str, CustomFunction]
            for key, value in data[event_name].items():
                event[key] = CustomFunction().unmarshal(value)
            self._event[event_name] = event

            return self._event[event_name]

    def save_func(
        self, event_name, func_name, real_func
    ):  # type: (str, str, CustomFunction) -> EventStorage
        """
        save_func 将给定的自定义函数注册到指定的事件下，
        同时将本次更改同步到底层的持久化存储中

        Args:
            event_name (str):
                目标事件名
            func_name (str):
                目标函数名
            real_func (CustomFunction):
                给定的自定义函数

        Returns:
            EventStorage:
                返回 EventStorage 本身
        """
        if self._storage is None:
            return self

        funcs = self._event.get(event_name, {})  # type: dict[str, CustomFunction]
        funcs[func_name] = real_func
        self._event[event_name] = funcs

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                root = {}  # type: dict[str, Any]

            func_index = root.get("event_func_index", {})  # type: dict[str, str]
            func_index[func_name] = event_name
            root["event_func_index"] = func_index

            all_index = root.get(
                "event_all_index", {}
            )  # type: dict[str, dict[str, bool]]
            index = all_index.get(event_name, {})  # type: dict[str, bool]
            index[func_name] = True
            all_index[event_name] = index
            root["event_all_index"] = all_index

            data = root.get(
                "event_data", {}
            )  # type: dict[str, dict[str, dict[str, Any]]]
            event = data.get(event_name, {})  # type: dict[str, dict[str, Any]]
            event[func_name] = real_func.marshal()
            data[event_name] = event
            root["event_data"] = data

            _ = manager.SetExtraData("form_system_storage", root)
            return self

    def remove_func(self, func_name):  # type: (str) -> str | None
        """
        remove_func 同时从缓存和底层存储中删除指定名称的自定义函数。
        即便 func_name 指示的自定义函数不存在，remove_func 也不会出错

        Args:
            func_name (str): 欲删除的自定义函数的名称

        Returns:
            str | None:
                如果该函数所在的事件在 remove_func 调用后没有剩余的函数，
                则返回该 func_name 对应事件的名称；否则，那么返回 None
        """
        if self._storage is None:
            return None

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                root = {}  # type: dict[str, Any]

            func_index = root.get("event_func_index", {})  # type: dict[str, str]
            if func_name not in func_index:
                return None

            data = root.get(
                "event_data", {}
            )  # type: dict[str, dict[str, dict[str, Any]]]
            all_index = root.get(
                "event_all_index", {}
            )  # type: dict[str, dict[str, bool]]

            for key, value in list(data.items()):
                if func_name in value:
                    del value[func_name]
                if len(value) == 0:
                    del data[key]
            for key, value in list(all_index.items()):
                if func_name in value:
                    del value[func_name]
                if len(value) == 0:
                    del all_index[key]
            del func_index[func_name]

            root["event_data"] = data
            root["event_all_index"] = all_index
            root["event_func_index"] = func_index

            _ = manager.SetExtraData("form_system_storage", root)

        result = None
        for key, value in list(self._event.items()):
            if func_name in value:
                del value[func_name]
            if len(value) == 0:
                del self._event[key]
                result = key
        return result
