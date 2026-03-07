# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable
    from mod.server.extraServerApi import ServerSystem

from mod.server.extraServerApi import (
    GetLevelId,
    GetEngineCompFactory,
    GetPlayerList,
    GetEntityLimit,
    SetEntityLimit,
)
from ..static.lib_object import BaseManager


class World:
    """
    World 导出了 Mod SDK 中世界模块的部分接口
    """

    _manager = BaseManager()  # type: BaseManager
    _system = None  # type: ServerSystem | None

    def __init__(self, manager, system):  # type: (BaseManager, ServerSystem) -> None
        """初始化并返回一个新的 World

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
            system (ServerSystem):
                当前模组的服务端实现
        """
        self._manager = manager
        self._system = system

    def create_projectile_entity(
        self, spawner_id, entity_identifier, param_ptr=None
    ):  # type: (str, str, int | None) -> int
        """create_projectile_entity 创建抛射物（直接发射）

        Args:
            spawner_id (str):
                创建抛射物的 ID
            entity_identifier (str):
                抛射物的命名标识符
            param_ptr (int | None, optional):
                要发射的抛射物的参数。
                应是一个指向映射的指针。
                默认值为 None

        Returns:
            int: 指向创建的抛射物的 ID 的指针
        """
        if param_ptr is None or param_ptr == 0:
            return self._manager.ref(
                GetEngineCompFactory()
                .CreateProjectile(GetLevelId())
                .CreateProjectileEntity(spawner_id, entity_identifier)
            )
        return self._manager.ref(
            GetEngineCompFactory()
            .CreateProjectile(GetLevelId())
            .CreateProjectileEntity(
                spawner_id, entity_identifier, self._manager.deref(param_ptr)
            )
        )

    def destroy_entity(self, entity_id):  # type: (str) -> int
        """destroy_entity 销毁给定的实体

        Args:
            entity_id (str):
                要销毁的实体的 ID

        Returns:
            int:
                指向消耗毁结果（布尔值）的指针
        """
        assert self._system is not None
        return self._manager.ref(self._system.DestroyEntity(entity_id))

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 world 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["world.CanSee"] = (
            lambda from_id, target_id, view_range=8.0, only_solid=True, angle_x=180.0, angle_y=180.0: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(from_id)
                .CanSee(from_id, target_id, view_range, only_solid, angle_x, angle_y)
            )
        )
        funcs["world.CheckBlockToPos"] = (
            lambda from_pos_ptr, to_pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .CheckBlockToPos(
                    self._manager.deref(from_pos_ptr),
                    self._manager.deref(to_pos_ptr),
                    dimension_id,
                )
            )
        )
        funcs["world.CheckChunkState"] = lambda dimension, pos: self._manager.ref(
            GetEngineCompFactory()
            .CreateChunkSource(GetLevelId())
            .CheckChunkState(dimension, self._manager.deref(pos))
        )
        funcs["world.GetAllAreaKeys"] = lambda: self._manager.ref(
            GetEngineCompFactory().CreateChunkSource(GetLevelId()).GetAllAreaKeys()
        )
        funcs["world.GetBiomeInfo"] = lambda biome_name: self._manager.ref(
            GetEngineCompFactory().CreateBiome(GetLevelId()).GetBiomeInfo(biome_name)
        )
        funcs["world.GetBiomeName"] = lambda pos_ptr, dim_id=-1: self._manager.ref(
            GetEngineCompFactory()
            .CreateBiome(GetLevelId())
            .GetBiomeName(self._manager.deref(pos_ptr), dim_id)
        )
        funcs["world.GetBlockLightLevel"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .GetBlockLightLevel(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["world.GetChunkEntites"] = lambda dimension, pos_ptr: self._manager.ref(
            GetEngineCompFactory()
            .CreateChunkSource(GetLevelId())
            .GetChunkEntites(dimension, self._manager.deref(pos_ptr))
        )
        funcs["world.GetChunkMobNum"] = (
            lambda dimension, chunk_pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateChunkSource(GetLevelId())
                .GetChunkMobNum(dimension, self._manager.deref(chunk_pos_ptr))
            )
        )
        funcs["world.GetEntitiesAround"] = (
            lambda entity_id, radius, filters: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(entity_id)
                .GetEntitiesAround(entity_id, radius, self._manager.deref(filters))
            )
        )
        funcs["world.GetEntitiesAroundByType"] = (
            lambda entity_id, radius, entity_type: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(GetLevelId())
                .GetEntitiesAroundByType(entity_id, radius, entity_type)
            )
        )
        funcs["world.GetEntitiesInSquareArea"] = (
            lambda start_pos_ptr, end_pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(GetLevelId())
                .GetEntitiesInSquareArea(
                    None,
                    self._manager.deref(start_pos_ptr),
                    self._manager.deref(end_pos_ptr),
                    dimension_id,
                )
            )
        )
        funcs["world.GetLevelId"] = lambda: self._manager.ref(GetLevelId())
        funcs["world.GetSpawnPosition"] = lambda: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).GetSpawnPosition()
        )
        funcs["world.GetStructureSize"] = lambda structure_name: self._manager.ref(
            GetEngineCompFactory()
            .CreateGame(GetLevelId())
            .GetStructureSize(structure_name)
        )
        funcs["world.IsChunkGenerated"] = (
            lambda dimension_id, chunk_pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateChunkSource(GetLevelId())
                .IsChunkGenerated(dimension_id, self._manager.deref(chunk_pos_ptr))
            )
        )
        funcs["world.IsSlimeChunk"] = (
            lambda dimension_id, chunk_pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateChunkSource(GetLevelId())
                .IsSlimeChunk(dimension_id, self._manager.deref(chunk_pos_ptr))
            )
        )
        funcs["world.LocateStructureFeature"] = (
            lambda feature_type, dimension_id, pos_ptr, use_new_chunks_only=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateFeature(GetLevelId())
                .LocateStructureFeature(
                    feature_type,
                    dimension_id,
                    self._manager.deref(pos_ptr),
                    use_new_chunks_only,
                )
            )
        )
        funcs["world.MayPlace"] = (
            lambda identifier, block_pos_ptr, facing, dimension_id=0: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .MayPlace(
                    identifier, self._manager.deref(block_pos_ptr), facing, dimension_id
                )
            )
        )
        funcs["world.MayPlaceOn"] = (
            lambda player_id, identifier, aux_value, block_pos_ptr, facing: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .MayPlaceOn(
                    identifier, aux_value, self._manager.deref(block_pos_ptr), facing
                )
            )
        )
        funcs["world.PlaceFeature"] = (
            lambda feature_name, dimension_id, pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(GetLevelId())
                .PlaceFeature(feature_name, dimension_id, self._manager.deref(pos_ptr))
            )
        )
        funcs["world.SetMergeSpawnItemRadius"] = lambda radius: self._manager.ref(
            GetEngineCompFactory()
            .CreateGame(GetLevelId())
            .SetMergeSpawnItemRadius(radius)
        )
        funcs["world.CreateExperienceOrb"] = (
            lambda entity_id, exp, position_ptr, is_special: self._manager.ref(
                GetEngineCompFactory()
                .CreateExp(entity_id)
                .CreateExperienceOrb(exp, self._manager.deref(position_ptr), is_special)
            )
        )
        funcs["world.CreateProjectileEntity"] = self.create_projectile_entity
        funcs["world.DestroyEntity"] = self.destroy_entity
        funcs["world.GetDroppedItem"] = (
            lambda item_entity_id, get_user_data=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(GetLevelId())
                .GetDroppedItem(item_entity_id, get_user_data)
            )
        )
        funcs["world.GetPlayerList"] = lambda: self._manager.ref(GetPlayerList())
        funcs["world.IsEntityAlive"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).IsEntityAlive(entity_id)
        )
        funcs["world.KillEntity"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).KillEntity(entity_id)
        )
        funcs["world.GetBlockClip"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .GetBlockClip(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["world.GetBlockCollision"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .GetBlockCollision(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["world.GetBlockNew"] = lambda pos_ptr, dimension_id=-1: self._manager.ref(
            GetEngineCompFactory()
            .CreateBlockInfo(GetLevelId())
            .GetBlockNew(self._manager.deref(pos_ptr), dimension_id)
        )
        funcs["world.GetLiquidBlock"] = (
            lambda pos_ptr, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .GetLiquidBlock(self._manager.deref(pos_ptr), dimension_id)
            )
        )
        funcs["world.GetTopBlockHeight"] = (
            lambda pos_ptr, dimension=0: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .GetTopBlockHeight(self._manager.deref(pos_ptr), dimension)
            )
        )
        funcs["world.GetEntityLimit"] = lambda: self._manager.ref(GetEntityLimit())
        funcs["world.SetEntityLimit"] = lambda num: self._manager.ref(
            SetEntityLimit(num)
        )
        funcs["world.IsRaining"] = lambda: self._manager.ref(
            GetEngineCompFactory().CreateWeather(GetLevelId()).IsRaining()
        )
        funcs["world.IsThunder"] = lambda: self._manager.ref(
            GetEngineCompFactory().CreateWeather(GetLevelId()).IsThunder()
        )
        funcs["world.GetLevelGravity"] = lambda: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).GetLevelGravity()
        )
        funcs["world.GetPistonMaxInteractionCount"] = lambda: self._manager.ref(
            GetEngineCompFactory()
            .CreateGame(GetLevelId())
            .GetPistonMaxInteractionCount()
        )
        funcs["world.SetHurtCD"] = lambda cd_time: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).SetHurtCD(cd_time)
        )
        funcs["world.SetLevelGravity"] = lambda data: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).SetLevelGravity(data)
        )
        funcs["world.SetPistonMaxInteractionCount"] = lambda value: self._manager.ref(
            GetEngineCompFactory()
            .CreateGame(GetLevelId())
            .SetPistonMaxInteractionCount(value)
        )
        funcs["world.SetCommand"] = (
            lambda cmd_str, entity_id, show_output=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateCommand(GetLevelId())
                .SetCommand(cmd_str, entity_id, show_output)
            )
        )

        for key, value in funcs.items():
            origin[key] = value
