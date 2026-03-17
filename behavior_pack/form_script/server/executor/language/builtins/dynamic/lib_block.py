# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId
from ..static.lib_object import BaseManager


class Block:
    """
    Block 导出了 Mod SDK 中方块模块的部分接口
    """

    _manager = BaseManager()  # type: BaseManager

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Block

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
        build_func 构建 block 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["block.GetBlockStates"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockState(GetLevelId())
                .GetBlockStates(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.ExecuteCommandBlock"] = (
            lambda pos_ptr, dimension_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockEntity(GetLevelId())
                .ExecuteCommandBlock(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.GetBlockEntityData"] = (
            lambda dimension, pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .GetBlockEntityData(dimension, self._manager.deref(pos_ptr))
            )
        )
        funcs["block.GetBlockTileEntityCustomData"] = (
            lambda player_id, pos_ptr, key, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(player_id)
                .GetBlockTileEntityCustomData(
                    self._manager.deref(pos_ptr), key, dimension_id
                )
            )
        )
        funcs["block.GetBlockTileEntityWholeCustomData"] = (
            lambda player_id, pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(player_id)
                .GetBlockTileEntityWholeCustomData(
                    self._manager.deref(pos_ptr), dimension_id
                )
            )
        )
        funcs["block.GetCommandBlock"] = (
            lambda pos_ptr, dimension_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockEntity(GetLevelId())
                .GetCommandBlock(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.GetFrameItem"] = lambda pos_ptr, dimension_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateBlockEntity(GetLevelId())
            .GetFrameItem(self._manager.deref(pos_ptr), dimension_id)
        )
        funcs["block.GetFrameRotation"] = (
            lambda pos_ptr, dimension_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockEntity(GetLevelId())
                .GetFrameRotation(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.SetCommandBlock"] = (
            lambda pos_ptr, dimension_id, cmd, name, mode, is_conditional, redstone_mode: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockEntity(GetLevelId())
                .SetCommandBlock(
                    self._manager.deref(pos_ptr),
                    dimension_id,
                    cmd,
                    name,
                    mode,
                    is_conditional,
                    redstone_mode,
                )
            )
        )
        funcs["block.SetFrameRotation"] = (
            lambda pos_ptr, dimension_id, rot: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockEntity(GetLevelId())
                .SetFrameRotation(self._manager.deref(pos_ptr), dimension_id, rot)
            )
        )
        funcs["block.GetBrewingStandSlotItem"] = (
            lambda player_id, slot, pos_ptr, dimension_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .GetBrewingStandSlotItem(
                    slot, self._manager.deref(pos_ptr), dimension_id
                )
            )
        )
        funcs["block.GetChestBoxSize"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateChestBlock(GetLevelId())
                .GetChestBoxSize(None, self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.GetChestPairedPosition"] = (
            lambda player_id, pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(player_id)
                .GetChestPairedPosition(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.GetContainerItem"] = (
            lambda pos_ptr, slot_pos, dimension_id=-1, get_user_data=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(GetLevelId())
                .GetContainerItem(
                    self._manager.deref(pos_ptr), slot_pos, dimension_id, get_user_data
                )
            )
        )
        funcs["block.GetContainerSize"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(GetLevelId())
                .GetContainerSize(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.GetEnderChestItem"] = (
            lambda player_id, slot_pos, get_user_data=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .GetEnderChestItem(player_id, slot_pos, get_user_data)
            )
        )
        funcs["block.GetInputSlotItem"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(GetLevelId())
                .GetInputSlotItem(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.GetOutputSlotItem"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(GetLevelId())
                .GetOutputSlotItem(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.SetChestBoxItemExchange"] = (
            lambda player_id, pos_ptr, slot_pos1, slot_pos2: self._manager.ref(
                GetEngineCompFactory()
                .CreateChestBlock(player_id)
                .SetChestBoxItemExchange(
                    player_id, self._manager.deref(pos_ptr), slot_pos1, slot_pos2
                )
            )
        )
        funcs["block.GetBlockPoweredState"] = (
            lambda pos_ptr, dimension_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateRedStone(GetLevelId())
                .GetBlockPoweredState(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.GetStrength"] = lambda pos_ptr, dimension_id=-1: self._manager.ref(
            GetEngineCompFactory()
            .CreateRedStone(GetLevelId())
            .GetStrength(self._manager.deref(pos_ptr), dimension_id)
        )
        funcs["block.GetSignBlockText"] = (
            lambda pos_ptr, dimension_id=-1, side=0: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .GetSignBlockText(self._manager.deref(pos_ptr), dimension_id, side)
            )
        )
        funcs["block.GetSignTextStyle"] = (
            lambda pos_ptr, dimension_id, side=0: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockEntity(GetLevelId())
                .GetSignTextStyle(self._manager.deref(pos_ptr), dimension_id, side)
            )
        )
        funcs["block.SetSignBlockText"] = (
            lambda player_id, pos_ptr, text, dimension_id=-1, side=0: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(player_id)
                .SetSignBlockText(
                    self._manager.deref(pos_ptr), text, dimension_id, side
                )
            )
        )
        funcs["block.SetSignTextStyle"] = (
            lambda pos_ptr, dimension_id, color, lighting, side=0: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockEntity(GetLevelId())
                .SetSignTextStyle(
                    self._manager.deref(pos_ptr), dimension_id, color, lighting, side
                )
            )
        )
        funcs["block.GetBedColor"] = (
            lambda player_id, pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(player_id)
                .GetBedColor(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["block.SetBedColor"] = (
            lambda player_id, pos_ptr, color, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(player_id)
                .SetBedColor(self._manager.deref(pos_ptr), color, dimension_id)
            )
        )

        for key, value in funcs.items():
            origin[key] = value
