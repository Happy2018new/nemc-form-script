# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import threading
from .base import StorageManager
from .form_struct.base import BaseForm
from .form_struct.long import LongForm
from .form_struct.popup import PopupForm
from .form_struct.modal import ModalForm

FORM_TYPE_LONG = 0
FORM_TYPE_POPUP = 1
FORM_TYPE_MODAL = 2


class FormStorage:
    """FormStorage 是所有表单的存储管理器"""

    _form = {}  # type: dict[str, BaseForm]
    _storage = None  # type: StorageManager | None
    _locker = None  # type: threading.RLock | None

    def __init__(self, storage):  # type: (StorageManager) -> None
        """初始化并返回一个新的表单存储管理器

        Args:
            storage (StorageManager):
                线程安全的底层存储管理器
        """
        self._form = {}
        self._storage = storage
        self._locker = threading.RLock()

    def get_locker(self):  # type: () -> threading.RLock
        """
        get_locker 返回表单存储管理器的可重入锁。
        确保 get_locker 返回的锁只对不同线程之间互斥。
        任何对表单的存储操作都须在锁的上下文内完成

        Returns:
            threading.RLock:
                表单存储管理器的锁
        """
        assert self._locker is not None
        return self._locker

    def form_type(self, form_name):  # type: (str) -> int | None
        """
        form_type 返回给定表单的类型

        Args:
            form_name (str):
                欲获取类型的表单的名称

        Returns:
            int | None:
                如果目标表单存在，则返回该表单的类型；
                否则目标表单不存在，那么返回 False
        """
        if self._storage is None:
            return None

        if form_name in self._form:
            form = self._form[form_name]
        else:
            form = self.get_form(form_name)
            if form is None:
                return None

        if isinstance(form, LongForm):
            return FORM_TYPE_LONG
        elif isinstance(form, PopupForm):
            return FORM_TYPE_POPUP
        elif isinstance(form, ModalForm):
            return FORM_TYPE_MODAL

    def form_index(self):  # type: () -> dict[str, int]
        """
        form_index 返回所有表单的索引。
        键是表单的名字，值是表单的类型

        Returns:
            dict[str, int]:
                所有已存储表单的索引
        """
        result = {}  # type: dict[str, int]
        if self._storage is None:
            return result

        for key, value in self._form.items():
            if isinstance(value, LongForm):
                result[key] = FORM_TYPE_LONG
            elif isinstance(value, PopupForm):
                result[key] = FORM_TYPE_POPUP
            elif isinstance(value, ModalForm):
                result[key] = FORM_TYPE_MODAL

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if root is None:
                return result

            assert isinstance(root, dict)
            index = root.get("form_index", {})  # type: dict[str, int]
            for key, value in index.items():
                result[key] = value

            return result

    def load_all(self):  # type: () -> FormStorage
        """
        load_all 从底层存储中加载所有表单到缓存中。
        如果某个表单已命中缓存，则该表单会被跳过

        Returns:
            FormStorage: 返回 FormStorage 本身
        """
        if self._storage is None:
            return self

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                return self

            data = root.get("form_data", {})  # type: dict[str, dict[str, Any]]
            index = root.get("form_index", {})  # type: dict[str, int]

            for key, value in data.items():
                if key in self._form:
                    continue
                form_type = index[key]
                if form_type == FORM_TYPE_LONG:
                    self._form[key] = LongForm().unmarshal(value)
                elif form_type == FORM_TYPE_POPUP:
                    self._form[key] = PopupForm().unmarshal(value)
                elif form_type == FORM_TYPE_MODAL:
                    self._form[key] = ModalForm().unmarshal(value)
            return self

    def get_form(self, form_name):  # type: (str) -> BaseForm | None
        """
        get_form 从缓存中获取指定名称的表单。
        如果缓存未命中，则从底层存储获取。

        另外，返回的表单可以被继续修改，
        并通过 save_form 持久化到底层存储

        Args:
            form_name (str):
                欲获取的表单名称

        Returns:
            BaseForm | None:
                如果目标表单存在，则返回对应的表单；
                否则目标表单不存在，那么返回 None
        """
        if self._storage is None:
            return None
        if form_name in self._form:
            return self._form[form_name]

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                return None

            index = root.get("form_index", {})  # type: dict[str, int]
            if form_name not in index:
                return None

            data = root.get("form_data", {})  # type: dict[str, dict[str, Any]]
            form_data = data[form_name]  # type: dict[str, Any]
            form_type = index[form_name]  # type: int

            if form_type == FORM_TYPE_LONG:
                self._form[form_name] = LongForm().unmarshal(form_data)
            elif form_type == FORM_TYPE_POPUP:
                self._form[form_name] = PopupForm().unmarshal(form_data)
            elif form_type == FORM_TYPE_MODAL:
                self._form[form_name] = ModalForm().unmarshal(form_data)

            return self._form[form_name]

    def save_form(
        self, form_name, real_form=None
    ):  # type: (str, BaseForm | None) -> FormStorage
        """
        save_form 将指定名称的表单
        从缓存持久化到底层存储。

        另，如果 real_form 为 None，
        则直接将位于缓存中的目标表单
        持久化到底层存储

        Args:
            form_name (str):
                欲保存的表单名称
            real_form (BaseForm | None, optional):
                该表单的实际内容。
                默认值为 None

        Returns:
            FormStorage: 返回 FormStorage 本身
        """
        if self._storage is None:
            return self

        if real_form is None and form_name not in self._form:
            return self
        if real_form is not None:
            self._form[form_name] = real_form

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                root = {}  # type: dict[str, Any]
            data = root.get("form_data", {})  # type: dict[str, dict[str, Any]]
            index = root.get("form_index", {})  # type: dict[str, int]

            form_cls = self._form[form_name]
            form_data = form_cls.marshal()
            data[form_name] = form_data
            root["form_data"] = data

            if isinstance(form_cls, LongForm):
                index[form_name] = FORM_TYPE_LONG
            elif isinstance(form_cls, PopupForm):
                index[form_name] = FORM_TYPE_POPUP
            elif isinstance(form_cls, ModalForm):
                index[form_name] = FORM_TYPE_MODAL
            root["form_index"] = index

            _ = manager.SetExtraData("form_system_storage", root)
            return self

    def remove_form(self, form_name):  # type: (str) -> FormStorage
        """
        remove_form 同时从缓存和底层存储中删除指定名称的表单。
        即便 form_name 指示的表单不存在，remove_form 也不会出错

        Args:
            form_name (str):
                欲删除的表单名称

        Returns:
            FormStorage: 返回 FormStorage 本身
        """
        if self._storage is None:
            return self
        if form_name in self._form:
            del self._form[form_name]

        with self._storage.get_locker():
            manager = self._storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                root = {}  # type: dict[str, Any]
            data = root.get("form_data", {})  # type: dict[str, dict[str, Any]]

            index = root.get("form_index", {})  # type: dict[str, int]
            if form_name not in index:
                return self

            del data[form_name]
            del index[form_name]
            root["form_data"] = data
            root["form_index"] = index

            _ = manager.SetExtraData("form_system_storage", root)
            return self
