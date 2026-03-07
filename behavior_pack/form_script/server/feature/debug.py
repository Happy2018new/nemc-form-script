# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

import time
from .function import FunctionFeature
from ..storage.form import FormStorage
from ..storage.function import FunctionStorage
from ..storage.event import EventStorage
from ..executor.executor import GameCodeExecutor
from ..executor.cache import CompileCache
from ..executor.language.package import CodeParser, CodeRunner


try:
    range = xrange  # type: ignore
except Exception:
    pass


class DebugFeature:
    """
    DebugFeature 实现了开发者调试系统的主要特性。
    确保 DebugFeature 的实现是线程安全的，
    并且仅会对不同线程之间的调用产生互斥作用
    """

    code_executor = None  # type: GameCodeExecutor | None
    form_storage = None  # type: FormStorage | None
    func_storage = None  # type: FunctionStorage | None
    event_storage = None  # type: EventStorage | None
    func_feature = None  # type: FunctionFeature | None
    compile_cache = None  # type: CompileCache | None

    def __init__(
        self,
        code_executor,  # type: GameCodeExecutor
        form_storage,  # type: FormStorage
        func_storage,  # type: FunctionStorage
        event_storage,  # type: EventStorage
        func_feature,  # type: FunctionFeature
        compile_cache,  # type: CompileCache
    ):  # type: (...) -> None
        """初始化并返回一个新的 DebugFeature

        Args:
            code_executor (GameCodeExecutor):
                用户代码的执行器
            form_storage (FormStorage):
                所有表单的存储管理器
            func_storage (FunctionStorage):
                所有自定义函数的存储管理器
            event_storage (EventStorage):
                所有事件的存储管理器
            func_feature (FunctionFeature):
                自定义函数的主要实现
            compile_cache (CompileCache):
                代码编译的缓存管理器
        """
        self.code_executor = code_executor
        self.form_storage = form_storage
        self.func_storage = func_storage
        self.event_storage = event_storage
        self.func_feature = func_feature
        self.compile_cache = compile_cache
        self._dynamic_init()

    def _dynamic_init(self):  # type: () -> None
        """
        _dynamic_init 初始化和设置与
        开发者调试有关的动态内建函数
        """
        assert self.code_executor is not None
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["debug.test_code_compile_time"] = self.test_code_compile_time
        funcs["debug.test_function_call_time"] = self.test_function_call_time
        funcs["debug.collect_compile_garbage"] = self.collect_compile_garbage
        funcs["debug.clean_compile_cache"] = self.clean_compile_cache
        funcs["debug.precompile_all_codes"] = self.precompile_all_codes

        with self.code_executor.get_locker():
            _ = self.code_executor.inject_func(funcs)

    def test_code_compile_time(self, code, repeats):  # type: (str, int) -> float
        """
        test_code_compile_time 测试给定的代码
        在重复编译 repeats 次后将消耗的总时间

        Args:
            code (str):
                被测试的代码
            repeats (int):
                重复编译的次数

        Returns:
            float:
                重复编译这段代码所消耗的总时间
        """
        assert self.compile_cache is not None

        start_time = time.time()
        for _ in range(repeats):
            _ = CodeRunner(CodeParser(code).parse().code_block)
        return time.time() - start_time

    def test_function_call_time(
        self, repeats, func_name, *args
    ):  # type: (int, str, ...) -> float
        """
        test_function_call_time 测试给定的自定义函数
        在重复调用 repeats 次后将消耗的总时间

        Args:
            repeats (int):
                重复调用的次数
            func_name (str):
                被测试的自定义函数的名称

        Returns:
            float:
                重复调用目标自定义
                函数所消耗的总时间
        """
        assert self.func_feature is not None

        start_time = time.time()
        for _ in range(repeats):
            _ = self.func_feature.call(func_name, *args)
        return time.time() - start_time

    def collect_compile_garbage(self):  # type: () -> bool
        """
        collect_compile_garbage 迫使底层
        编译缓存发生一次强制的垃圾回收

        Returns:
            bool: 总是返回 True
        """
        assert self.compile_cache is not None

        _ = self.compile_cache.compact()
        return True

    def clean_compile_cache(self):  # type: () -> bool
        """clean_compile_cache 清空编译缓存中的所有缓存

        Returns:
            bool: 总是返回 True
        """
        assert self.compile_cache is not None

        size = self.compile_cache.get_max_cache_size()
        _ = self.compile_cache.set_max_cache_size(0)
        _ = self.compile_cache.set_max_cache_size(size)

        return True

    def precompile_all_codes(self):  # type: () -> float
        """
        precompile_all_codes 编译已持久化到存档的所有源代码，
        并返回编译所有这些源代码所消耗的总时间

        Returns:
            float: 编译所有这些源代码所消耗的总时间
        """
        assert self.form_storage is not None
        assert self.func_storage is not None
        assert self.event_storage is not None
        assert self.compile_cache is not None

        start_time = time.time()
        _ = self.compile_cache.prepare(
            self.form_storage, self.func_storage, self.event_storage
        )
        return time.time() - start_time
