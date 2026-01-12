# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import threading
from .base import StringWithHash
from .base import StorageManager


class CustomFunction(StringWithHash):
    """CustomFunction 存储了一个自定义函数的原始代码"""

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal 将该 CustomFunction 编码为其对应 JSON 表示

        Returns:
            dict[str, Any]:
                该 CustomFunction 对应的 JSON 表示
        """
        return StringWithHash.marshal(self)

    def unmarshal(self, data):  # type: (Any) -> CustomFunction
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据置入该 CustomFunction 中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            CustomFunction: 返回 CustomFunction 本身
        """
        StringWithHash.unmarshal(self, data)
        return self


class FunctionStorage:
    """FunctionStorage 是所有自定义函数的存储管理器"""

    _func = {}  # type: dict[str, CustomFunction]
    _storage = None  # type: StorageManager | None
    _locker = None  # type: threading.RLock | None

    def __init__(self, storage):  # type: (StorageManager) -> None
        """初始化并返回一个新的自定义函数存储管理器

        Args:
            storage (StorageManager):
                线程安全的底层存储管理器
        """
        self._func = {}
        self._storage = storage
        self._locker = threading.RLock()

    def get_locker(self):  # type: () -> threading.RLock
        """
        get_locker 返回自定义函数的存储管理器的可重入锁。
        确保 get_locker 返回的锁只对不同线程之间互斥。
        任何对自定义函数的存储操作都须在锁的上下文内完成

        Returns:
            threading.RLock:
                自定义函数的存储管理器的锁
        """
        assert self._locker is not None
        return self._locker

    def check_exist(self, func_name):  # type: (str) -> bool
        """
        check_exist 检查给定名称的自定义函数是否存在

        Args:
            func_name (str):
                欲检查的自定义函数的名称

        Returns:
            bool:
                如果目标自定义函数存在，则返回 True；
                否则目标自定义函数不存在，那么返回 False
        """
        if self._storage is None:
            return False
        if func_name in self._func:
            return True
        return self.get_func(func_name) is not None

    def func_index(self):  # type: () -> set[str]
        """
        func_index 返回所有自定义函数的索引

        Returns:
            set[str]:
                所有自定义函数的索引
        """
        if self._storage is None:
            return set()

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if root is None:
                return set()

            assert isinstance(root, dict)
            result = root.get("func_index", {})  # type: dict[str, bool]
            return set(result)

    def load_all(self):  # type: () -> FunctionStorage
        """
        load_all 从底层存储中加载所有自定义函数到缓存中

        Returns:
            FunctionStorage:
                返回 FunctionStorage 本身
        """
        if self._storage is None:
            return self

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                return self
            data = root.get("func_data", {})  # type: dict[str, dict[str, Any]]

            for key, value in data.items():
                self._func[key] = CustomFunction().unmarshal(value)
            return self

    def get_func(self, func_name):  # type: (str) -> CustomFunction | None
        """
        get_func 从缓存中获取指定名称的自定义函数。
        如果缓存未命中，则从底层存储获取。

        返回的自定义函数不容许进一步修改。
        您只能通过重新构造新的 CustomFunction 实例，
        并通过 save_func 持久化到底层存储

        Args:
            func_name (str):
                欲获取的自定义函数的名称

        Returns:
            CustomFunction | None:
                如果目标自定义函数存在，则返回对应的自定义函数；
                否则目标自定义函数不存在，那么返回 None
        """
        if self._storage is None:
            return None
        if func_name in self._func:
            return self._func[func_name]

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                return None

            data = root.get("func_data", {})  # type: dict[str, dict[str, Any]]
            if func_name not in data:
                return None
            func = CustomFunction().unmarshal(data[func_name])

            self._func[func_name] = func
            return func

    def save_func(
        self, func_name, real_func
    ):  # type: (str, CustomFunction) -> FunctionStorage
        """
        save_func 更新指定的自定义函数到缓存，
        并同时将这一更改持久化到底层存储

        Args:
            func_name (str):
                目标自定义函数的名称
            real_func (CustomFunction):
                目标自定义函数的实际内容

        Returns:
            FunctionStorage: 返回 FunctionStorage 本身
        """
        if self._storage is None:
            return self
        self._func[func_name] = real_func

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                root = {}  # type: dict[str, Any]
            data = root.get("func_data", {})  # type: dict[str, dict[str, Any]]
            index = root.get("func_index", {})  # type: dict[str, bool]

            data[func_name] = real_func.marshal()
            index[func_name] = True
            root["func_data"] = data
            root["func_index"] = index

            _ = manager.SetExtraData("form_system_storage", root)
            return self

    def remove_func(self, func_name):  # type: (str) -> FunctionStorage
        """
        remove_func 同时从缓存和底层存储中删除指定名称的自定义函数。
        即便 func_name 指示的自定义函数不存在，remove_func 也不会出错

        Args:
            func_name (str): 欲删除的自定义函数的名称

        Returns:
            FunctionStorage: 返回 FunctionStorage 本身
        """
        if self._storage is None:
            return self
        if func_name in self._func:
            del self._func[func_name]

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                root = {}  # type: dict[str, Any]
            data = root.get("func_data", {})  # type: dict[str, dict[str, Any]]

            index = root.get("func_index", {})  # type: dict[str, bool]
            if func_name not in index:
                return self

            del data[func_name]
            del index[func_name]
            root["func_data"] = data
            root["func_index"] = index

            _ = manager.SetExtraData("form_system_storage", root)
            return self
