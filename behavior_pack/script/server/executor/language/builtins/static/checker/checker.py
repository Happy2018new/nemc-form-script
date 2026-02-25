# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import types
from .const import SAFE_MODULE, UNSAFE_BUILTINS


def is_string(obj):  # type: (Any) -> bool
    """
    is_string 检查 obj 是否是字符串

    Args:
        obj (Any): 待检查的对象

    Returns:
        bool: 目标对象是否是字符串
    """
    if isinstance(obj, str):
        return True

    try:
        if isinstance(obj, unicode):  # type: ignore
            return True
    except Exception:
        pass

    return False


def check_object(obj):  # type: (Any) -> bool
    """
    check_object 检查 obj 所指示的对象是否是我们允许的存在。
    这用于防止用户代码通过意想不到的手段获取到了不安全的对象

    Args:
        obj (Any): 待检查的对象

    Returns:
        bool: 对象是否安全
    """
    if isinstance(obj, types.ModuleType):
        try:
            module_name = obj.__name__.lower()
            return module_name in SAFE_MODULE
        except Exception:
            return False

    if callable(obj):
        mark = False

        if not hasattr(obj, "__module__"):
            return True
        module_name = getattr(obj, "__module__")
        if not is_string(module_name):
            return False

        if module_name in ("__builtin__", "site"):
            mark = True
        if module_name in ("_sitebuiltins", "builtins", "_io"):
            mark = True
        if not mark:
            return True

        if not hasattr(obj, "__name__"):
            return False
        func_name = getattr(obj, "__name__", "")
        if not is_string(func_name):
            return False

        return func_name.lower() not in UNSAFE_BUILTINS

    return True
