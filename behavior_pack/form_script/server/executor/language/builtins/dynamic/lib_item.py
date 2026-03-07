# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId
from ..static.lib_object import BaseManager


class Item:
    """
    Item 导出了 Mod SDK 中物品模块的部分接口
    """

    _manager = BaseManager()  # type: BaseManager

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Item

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 item 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["item.GetAllEnchantsInfo"] = lambda: self._manager.ref(
            GetEngineCompFactory().CreateItem(GetLevelId()).GetAllEnchantsInfo()
        )
        funcs["item.GetItemDurability"] = (
            lambda player_id, pos_type, slot_pos: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .GetItemDurability(pos_type, slot_pos)
            )
        )
        funcs["item.GetItemInfoByBlockName"] = (
            lambda block_name, aux_value=0, is_legacy=True: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(GetLevelId())
                .GetItemInfoByBlockName(block_name, aux_value, is_legacy)
            )
        )
        funcs["item.GetItemMaxDurability"] = (
            lambda player_id, pos_type, slot_pos, is_user_data: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .GetItemMaxDurability(pos_type, slot_pos, is_user_data)
            )
        )
        funcs["item.SetItemDurability"] = (
            lambda player_id, pos_type, slot_pos, durability: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .SetItemDurability(pos_type, slot_pos, durability)
            )
        )

        for key, value in funcs.items():
            origin[key] = value
