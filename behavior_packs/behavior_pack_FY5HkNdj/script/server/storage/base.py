# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from mod.server.component.exDataCompServer import ExDataCompServer

import binascii
import threading
from ..utils import compute_md5
from ...formal.base import Marshaler
from mod.server.extraServerApi import GetLevelId, GetEngineCompFactory

EMPTY_STRING = ""


class StringWithHash(Marshaler):
    """
    StringWithHash 保存了一个字符串，以及它的 MD5 摘要值
    """

    _data = ""
    _md5 = b""

    def __init__(self, data=EMPTY_STRING):  # type: (str) -> None
        """初始化并返回一个新的 StringWithHash

        Args:
            data (str, optional):
                给定的字符串。
                默认值为 EMPTY_STRING
        """
        self._data = data
        self._md5 = (
            compute_md5(data.encode(encoding="utf-8"))
            if data is not EMPTY_STRING
            else b""
        )

    def string(self):  # type: () -> str
        """
        string 返回该 StringWithHash 所保存的字符串

        Returns:
            str:
                该 StringWithHash 所保存的字符串
        """
        return self._data

    def hash(self):  # type: () -> bytes
        """
        hash 返回该 StringWithHash 所保存字符串的 MD5 摘要值

        Returns:
            bytes:
                该 StringWithHash 所保存字符串的 MD5 摘要值
        """
        return self._md5

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal 将该 StringWithHash 编码为其对应 JSON 表示

        Returns:
            dict[str, Any]:
                该 StringWithHash 对应的 JSON 表示
        """
        return {
            "data": self._data,
            "md5": binascii.hexlify(self._md5),
        }

    def unmarshal(self, data):  # type: (Any) -> StringWithHash
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据置入该 StringWithHash 中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            StringWithHash: 返回 StringWithHash 本身
        """
        self._data = data["data"]
        self._md5 = binascii.unhexlify(data["md5"])
        return self


class BaseForm(Marshaler):
    """BaseForm 是数据保存实现中，所有表单的父类"""

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将该 BaseForm 编码为对应的 JSON 表示

        Returns:
            dict[str, Any]: 该 BaseForm 对应的 JSON 表示
        """
        return {}

    def unmarshal(self, data):  # type: (Any) -> BaseForm
        """
        unmarshal 从 JSON 中解码数据，
        并将解码所得的数据置入本实例中

        Args:
            data (Any): 给定的 data 数据。
                        应确保它是一个字典

        Returns:
            BaseForm: 返回 BaseForm 本身
        """
        _ = data
        return self

    def all_codes(self):  # type: () -> list[StringWithHash]
        """
        all_codes 返回该 BaseForm 中存在的所有代码

        Returns:
            list[StringWithHash]:
                该 BaseForm 中存在的所有代码
        """
        return []


class StorageManager:
    """
    StorageManager 是带有锁的，
    保证了线程安全的存储管理器
    """

    _locker = None  # type: threading.Lock | None
    _storage = None  # type: ExDataCompServer | None

    def __init__(self):  # type: () -> None
        """初始化并返回一个新的 StorageManager"""
        self._locker = threading.Lock()
        self._storage = GetEngineCompFactory().CreateExtraData(GetLevelId())

    def get_locker(self):  # type: () -> threading.Lock
        """get_locker 返回存储资源的锁

        Returns:
            threading.Lock: 存储资源的锁
        """
        assert self._locker is not None
        return self._locker

    def get_storage(self):  # type: () -> ExDataCompServer
        """
        get_storage 返回底层的存储资源管理器。

        它的调用者有责任确保在调用该函数前，
        已通过 get_locker 取得并占用了锁

        Returns:
            ExDataCompServer:
                底层的存储资源管理器
        """
        assert self._storage is not None
        return self._storage
