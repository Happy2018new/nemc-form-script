# -*- coding: utf-8 -*-

try:
    from hashlib import md5
except Exception:
    import _md5  # type: ignore

    md5 = _md5.new  # type: ignore


def compute_md5(data):  # type: (bytes) -> bytes
    """compute_md5 计算给定数据的 MD5 摘要值

    Args:
        data (bytes): 给定的数据

    Returns:
        bytes: 给定数据的 MD5 摘要值
    """
    result = md5(data).digest()
    return result
