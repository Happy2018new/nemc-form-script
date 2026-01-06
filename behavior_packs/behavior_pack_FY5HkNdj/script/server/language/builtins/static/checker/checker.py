# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import types
from .const import SAFE_MODULE, UNSAFE_BUILTINS


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
        try:
            module_name = getattr(obj, "__module__")
            if module_name in ("__builtin__", "builtins"):
                name = getattr(obj, "__name__", "").lower()
                return name not in UNSAFE_BUILTINS
        except:
            pass

    return True
