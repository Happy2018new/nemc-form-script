# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from .const import CONST_ALL_TEXTURES
from ..static.lib_object import BaseManager


class Utils:
    """
    Utils 提供了一些辅助性函数
    """

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Utils

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def texture_by_keyword(
        self, keyword="", page_split=True
    ):  # type: (str, bool) -> int
        """
        texture_by_keyword 通过关键词搜索纹理 ID。
        它将返回所有包含 keyword 的材质贴图路径。

        Args:
            keyword (str, optional):
                给定的关键词。
                默认值为空字符串
            page_split (bool, optional):
                是否返回适用于 page_split 的结果。
                默认值为 True

        Returns:
            int: 指向结果映射的指针
        """
        keyword = keyword.strip().lower()

        if page_split:
            result = [
                (i.replace(keyword, "§c{}§8".format(keyword)), i)
                for i in CONST_ALL_TEXTURES
                if keyword in i.lower()
            ]
        else:
            result = [i for i in CONST_ALL_TEXTURES if keyword in i.lower()]

        return self._manager.ref(result)

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 utils 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["utils.texture_by_keyword"] = self.texture_by_keyword

        for key, value in funcs.items():
            origin[key] = value
