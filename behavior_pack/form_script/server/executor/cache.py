# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

import threading
from .language.package import CodeParser, CodeRunner
from ..storage.base import StringWithHash, StorageManager
from ..storage.form import FormStorage
from ..storage.function import FunctionStorage
from ..storage.event import EventStorage


COMPILE_CACHE_DEFAULT_MAX_SIZE = 2048
COMPILE_CACHE_DEFAULT_COMPACT_RATIO = 0.25


class CompileCache:
    """
    CompileCache 是代码编译的缓存管理器。
    重复编译相同的代码将会命中缓存，从而提升性能
    """

    _cache = {}  # type: dict[bytes, CodeRunner]
    _sequence = []  # type: list[bytes]
    _storage = None  # type: StorageManager | None
    _locker = None  # type: threading.Lock | None
    _max_size = COMPILE_CACHE_DEFAULT_MAX_SIZE  # type: int

    def __init__(self, storage):  # type: (StorageManager) -> None
        """初始化并返回一个新的 CompileCache

        Args:
            storage (StorageManager):
                线程安全的底层存储管理器
        """
        self._cache = {}
        self._sequence = []
        self._storage = storage
        self._locker = threading.Lock()
        self._max_size = COMPILE_CACHE_DEFAULT_MAX_SIZE

        with storage.get_locker():
            manager = storage.get_storage()

            root = manager.GetExtraData("form_system_storage")
            if not isinstance(root, dict):
                root = {}  # type: dict[str, Any]

            if "compile_max_cache" in root:
                self._max_size = root["compile_max_cache"]
            else:
                root["compile_max_cache"] = self._max_size
                _ = manager.SetExtraData("form_system_storage", root)

    def _compact(self, force=False):  # type: (bool) -> CompileCache
        """
        _compact 试图对底层缓存序列进行紧缩以回收内存。
        它将按时间顺序和固定的紧缩比率，将早期的缓存移除

        Args:
            force (bool, optional):
                是否要强制紧缩，即便当前缓存未满。
                默认值为 False

        Returns:
            CompileCache: 返回 CompileCache 本身
        """
        if not force and len(self._cache) <= self._max_size:
            return self

        ratio = COMPILE_CACHE_DEFAULT_COMPACT_RATIO
        length = int(len(self._sequence) * ratio)
        if len(self._sequence) - length > self._max_size:
            length = len(self._sequence) - self._max_size

        for i in self._sequence[:length]:
            del self._cache[i]
        self._sequence = self._sequence[length:]
        return self

    def _compile(self, code):  # type: (StringWithHash) -> CodeRunner
        """
        _compile 根据 code 返回对应的 CodeRunner。
        如果缓存未命中，则将重新编译相应的代码

        Args:
            code (StringWithHash):
                已取得 MD5 摘要的代码

        Raises:
            Exception:
                如果代码编译失败，则抛出相应的错误

        Returns:
            CodeRunner: code 对应的代码运行器
        """
        md5_hash = code.hash()
        if md5_hash in self._cache:
            return self._cache[md5_hash]

        parser = CodeParser(code.string()).parse()
        runner = CodeRunner(parser.code_block)

        self._cache[md5_hash] = runner
        self._sequence.append(md5_hash)
        self._compact()

        return runner

    def get_max_cache_size(self):  # type: () -> int
        """
        get_max_cache_size 返回底层缓存允许的最大容量

        Returns:
            int: 底层缓存允许的最大容量
        """
        assert self._locker is not None

        with self._locker:
            return self._max_size

    def get_current_cache_size(self):  # type: () -> int
        """
        get_current_cache_size 返回底层缓存的已用容量

        Returns:
            int: 底层缓存的已用容量
        """
        assert self._locker is not None

        with self._locker:
            return len(self._cache)

    def set_max_cache_size(self, size):  # type: (int) -> bool
        """
        set_max_cache_size 设置底层缓存允许的最大容量。
        如果给出的新容量小于当前已用部分，则将会垃圾回收

        Args:
            size (int):
                欲设置的最大缓存容量

        Raises:
            Exception:
                如果给出的 size 不是整数，
                或给出的 size 是负数，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        assert self._storage is not None
        assert self._locker is not None

        with self._locker:
            if isinstance(size, bool) or not isinstance(size, int):
                raise Exception(
                    "set_max_cache_size: The given size must be int (size={})".format(
                        size
                    )
                )
            if size < 0:
                raise Exception(
                    "set_max_cache_size: The given size must be non-negative integer (size={})".format(
                        size
                    )
                )

            with self._storage.get_locker():
                manager = self._storage.get_storage()
                root = manager.GetExtraData("form_system_storage")
                if not isinstance(root, dict):
                    root = {}  # type: dict[str, Any]
                root["compile_max_cache"] = size
                _ = manager.SetExtraData("form_system_storage", root)

            self._max_size = size
            _ = self._compact(False)
            return True

    def compact(self):  # type: () -> CompileCache
        """
        compact 试图对底层缓存序列进行紧缩以回收内存。
        它将按时间顺序和固定的紧缩比率，将早期的缓存移除

        Returns:
            CompileCache: 返回 CompileCache 本身
        """
        assert self._locker is not None

        with self._locker:
            return self._compact(True)

    def prepare(
        self, form_storage, func_storage, event_storage
    ):  # type: (FormStorage, FunctionStorage, EventStorage) -> CompileCache
        """
        prepare 编译本模组储存了的所有代码。
        该函数应当只在该模组被初始化时调用

        Args:
            form_storage (FormStorage):
                所有表单的存储管理器
            func_storage (FunctionStorage):
                所有自定义函数的存储管理器
            event_storage (EventStorage):
                所有事件的存储管理器

        Returns:
            CompileCache: 返回 CompileCache 本身
        """
        assert self._locker is not None

        with self._locker:
            form_storage.get_locker().acquire()
            func_storage.get_locker().acquire()
            event_storage.get_locker().acquire()

            try:
                # load all saved things
                _ = form_storage.load_all()
                _ = func_storage.load_all()
                _ = event_storage.load_all()
                # process form objects
                for form_name in form_storage.form_index():
                    form = form_storage.get_form(form_name)
                    if form is None:
                        continue
                    for i in form.all_codes():
                        _ = self._compile(i)
                # process custom functions
                for func_name in func_storage.func_index():
                    func = func_storage.get_func(func_name)
                    if func is not None:
                        _ = self._compile(func)
                # process event functions
                for event_name in event_storage.all_index():
                    funcs = event_storage.get_funcs(event_name)
                    if funcs is None:
                        continue
                    for _, func in funcs.items():
                        _ = self._compile(func.get_func())
                        _ = self._compile(func.get_on_error())
            finally:
                event_storage.get_locker().release()
                func_storage.get_locker().release()
                form_storage.get_locker().release()

            return self

    def get_runner(self, code):  # type: (StringWithHash) -> CodeRunner
        """
        get_runner 根据 code 返回对应的 CodeRunner。
        如果缓存未命中，则给定的代码将会被重新编译

        Args:
            code (StringWithHash):
                已取得 MD5 摘要的代码

        Raises:
            Exception:
                如果代码编译失败，则抛出相应的错误

        Returns:
            CodeRunner: code 对应的代码运行器
        """
        assert self._locker is not None

        with self._locker:
            return self._compile(code)

    def register_cache(self, code):  # type: (str) -> bool
        """
        register_cache 编译给定的代码，并将其注册到缓存系统中。
        如果给定的代码命中了缓存，则该函数的行为将视作无操作

        Args:
            code (str):
                给定的代码

        Returns:
            bool: 总是返回 True
        """
        _ = self.get_runner(StringWithHash(code))
        return True

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 compile 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["compile.get_max_cache_size"] = self.get_max_cache_size
        funcs["compile.get_current_cache_size"] = self.get_current_cache_size
        funcs["compile.set_max_cache_size"] = self.set_max_cache_size
        funcs["compile.register_cache"] = self.register_cache

        for key, value in funcs.items():
            origin[key] = value
