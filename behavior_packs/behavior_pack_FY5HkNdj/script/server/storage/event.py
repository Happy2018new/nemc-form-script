# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import threading
from .base import StringWithHash
from .base import StorageManager
from ...formal.base import Marshaler


EMPTY_STRING_WITH_HASH = StringWithHash()


class EventFuncData(Marshaler):
    """
    EventFuncData 描述一个事件中的单个侦听函数的存储形式。
    它保存了侦听到相应事件时应执行的代码，
    以及在该代码运行出错时应执行的错误处理
    """

    _func = EMPTY_STRING_WITH_HASH
    _onerror = EMPTY_STRING_WITH_HASH

    def __init__(
        self, func=EMPTY_STRING_WITH_HASH, onerror=EMPTY_STRING_WITH_HASH
    ):  # type: (StringWithHash, StringWithHash) -> None
        self._func = func
        self._onerror = onerror

    def get_func(self):  # type: () -> StringWithHash
        """
        get_func 返回相应事件
        发生时，要执行的源代码

        Returns:
            StringWithHash:
                相应的源代码
        """
        return self._func

    def get_on_error(self):  # type: () -> StringWithHash
        """
        get_on_error 返回当事件处理函数执行出错时，
        要执行的用于进行错误处理的源代码

        Returns:
            StringWithHash:
                相应的源代码
        """
        return self._onerror

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal 将该 EventFuncData 编码为其对应 JSON 表示

        Returns:
            dict[str, Any]:
                该 EventFuncData 对应的 JSON 表示
        """
        return {
            "func": self._func.marshal(),
            "onerror": self._onerror.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> EventFuncData
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据置入该 EventFuncData 中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            EventFuncData: 返回 EventFuncData 本身
        """
        self._func = StringWithHash().unmarshal(data["func"])
        self._onerror = StringWithHash().unmarshal(data["onerror"])
        return self


class EventStorage:
    """EventStorage 是所有事件的存储管理器"""

    _event = {}  # type: dict[str, dict[str, EventFuncData]]
    _storage = None  # type: StorageManager | None
    _locker = None  # type: threading.RLock | None

    def __init__(self, storage):  # type: (StorageManager) -> None
        """初始化并返回一个新的事件存储管理器

        Args:
            storage (StorageManager):
                线程安全的底层存储管理器
        """
        self._event = {}
        self._storage = storage
        self._locker = threading.RLock()

    def get_locker(self):  # type: () -> threading.RLock
        """
        get_locker 返回事件存储管理器的可重入锁。
        确保 get_locker 返回的锁只对不同线程之间互斥。
        任何对事件的存储操作都须在锁的上下文内完成

        Returns:
            threading.RLock:
                事件存储管理器的锁
        """
        assert self._locker is not None
        return self._locker

    def event_name(self, func_name):  # type: (str) -> str | None
        """
        event_name 返回给定的事件函数绑定在哪个事件下

        Args:
            func_name (str):
                目标事件函数的名称

        Returns:
            str | None:
                如果目标事件函数存在，则返回对应的事件名；
                否则目标事件函数不存在，那么返回 None
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
        对于返回的索引，键是事件名，
        值是该事件下注册的所有事件函数

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
        func_index 返回所有事件函数的索引。
        对于返回的索引，键是事件函数的名称，
        值是该事件函数注册时对应的事件名

        Returns:
            dict[str, str]:
                所有事件函数的索引
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
                event = {}  # type: dict[str, EventFuncData]
                for k, v in value.items():
                    event[k] = EventFuncData().unmarshal(v)
                self._event[key] = event

            return self

    def get_funcs(self, event_name):  # type: (str) -> dict[str, EventFuncData] | None
        """
        get_funcs 从缓存中获取注册在给定事件下的所有事件函数。
        如果缓存未命中，则从底层存储获取。

        返回的字典不容许进一步修改。
        您只能通过重新构造新的 EventFuncData 实例，
        并通过 save_func 持久化到底层存储

        Args:
            event_name (str): 给定的事件名

        Returns:
            dict[str, EventFuncData] | None:
                如果存在，则返回该事件下的所有事件函数；
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

            event = {}  # type: dict[str, EventFuncData]
            for key, value in data[event_name].items():
                event[key] = EventFuncData().unmarshal(value)
            self._event[event_name] = event

            return self._event[event_name]

    def save_func(
        self, event_name, func_name, real_func
    ):  # type: (str, str, EventFuncData) -> EventStorage
        """
        save_func 将给定的事件函数注册到指定的事件下，
        同时将本次更改同步到底层的持久化存储中

        Args:
            event_name (str):
                目标事件的名称
            func_name (str):
                目标事件函数的名称
            real_func (EventFuncData):
                给定的事件函数

        Returns:
            EventStorage:
                返回 EventStorage 本身
        """
        if self._storage is None:
            return self

        funcs = self._event.get(event_name, {})  # type: dict[str, EventFuncData]
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

    def remove_func(self, func_name):  # type: (str) -> bool
        """
        remove_func 同时从缓存和底层存储中删除指定名称的事件函数。
        即便 func_name 指示的事件函数不存在，remove_func 也不会出错

        Args:
            func_name (str): 欲删除的事件函数的名称

        Returns:
            bool:
                如果在 remove_func 操作后，目标事件下没有剩余的事件函数，
                则 remove_func 将返回 True，否则返回 False
        """
        if self._storage is None:
            return False

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                root = {}  # type: dict[str, Any]

            func_index = root.get("event_func_index", {})  # type: dict[str, str]
            if func_name not in func_index:
                return False

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

        for key, value in list(self._event.items()):
            if func_name in value:
                del value[func_name]
            if len(value) == 0:
                del self._event[key]
                return True
        return False
