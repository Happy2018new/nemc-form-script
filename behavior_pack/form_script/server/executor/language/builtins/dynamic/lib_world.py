# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from mod.server.extraServerApi import ServerSystem

from mod.server.extraServerApi import (
    GetLevelId,
    GetEngineCompFactory,
    GetPlayerList,
    GetEntityLimit,
    SetEntityLimit,
    GetEngineActor,
    getEntitiesOrBlockFromRay,
)
from ..static.lib_object import BaseManager


class World:
    """
    World 导出了 Mod SDK 中世界模块的部分接口
    """

    _manager = BaseManager()  # type: BaseManager
    _system = None  # type: ServerSystem | None
    _callback = None  # type: Callable[[str, dict[str, Any]], None] | None

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
        self._callback = None

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
                指向消毁结果（布尔值）的指针
        """
        assert self._system is not None
        return self._manager.ref(self._system.DestroyEntity(entity_id))

    def create_engine_entity_by_type_str(
        self,
        engine_type_str,
        pos_ptr,
        rot_ptr,
        dimension_id,
        is_npc=False,
        is_global=False,
    ):  # type: (str, int, int, int, bool, bool) -> int
        """create_engine_entity_by_type_str 创建指定 ID 的实体

        Args:
            engine_type_str (str):
                欲创建的实体的 ID
            pos_ptr (int):
                目标实体应生成的位置。
                应是一个指向元组的指针
            rot_ptr (int):
                生成的实体所视方向的偏航角和俯仰角。
                应是一个指向元组的指针
            dimension_id (int):
                目标实体应生成的维度 ID
            is_npc (bool, optional):
                所生成的实体是否是 NPC。
                默认值为 False
            is_global (bool):
                是否创建为全局实体。
                默认值为 False

        Returns:
            int:
                如果成功，返回一个指向字符串的指针，代表该实体的 ID；
                否则失败，那么返回一个指向 None 的指针
        """
        assert self._system is not None
        return self._manager.ref(
            self._system.CreateEngineEntityByTypeStr(
                engine_type_str,
                self._manager.deref(pos_ptr),
                self._manager.deref(rot_ptr),
                dimension_id,
                is_npc,
                is_global,
            )
        )

    def set_callback(
        self, callback
    ):  # type: (Callable[[str, dict[str, Any]], None]) -> None
        """
        set_callback 向底层注册一个回调函数，
        以便于基于回调函数工作的实现可以调用

        Args:
            callback (Callable[[str, dict[str, Any]], None]):
                欲注册的回调函数实现
        """
        self._callback = callback

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
        funcs["world.CheckChunkState"] = lambda dimension, pos_ptr: self._manager.ref(
            GetEngineCompFactory()
            .CreateChunkSource(GetLevelId())
            .CheckChunkState(dimension, self._manager.deref(pos_ptr))
        )
        funcs["world.CreateExplosion"] = (
            lambda pos_ptr, radius, fire, breaks, source_id, player_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateExplosion(GetLevelId())
                .CreateExplosion(
                    self._manager.deref(pos_ptr),
                    radius,
                    fire,
                    breaks,
                    source_id,
                    player_id,
                )
            )
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
        funcs["world.GetChunkMaxPos"] = lambda chunk_pos_ptr: self._manager.ref(
            GetEngineCompFactory()
            .CreateChunkSource(GetLevelId())
            .GetChunkMaxPos(self._manager.deref(chunk_pos_ptr))
        )
        funcs["world.GetChunkMinPos"] = lambda chunk_pos_ptr: self._manager.ref(
            GetEngineCompFactory()
            .CreateChunkSource(GetLevelId())
            .GetChunkMinPos(self._manager.deref(chunk_pos_ptr))
        )
        funcs["world.GetChunkMobNum"] = (
            lambda dimension, chunk_pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateChunkSource(GetLevelId())
                .GetChunkMobNum(dimension, self._manager.deref(chunk_pos_ptr))
            )
        )
        funcs["world.GetEntitiesAround"] = (
            lambda entity_id, radius, filters_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(entity_id)
                .GetEntitiesAround(entity_id, radius, self._manager.deref(filters_ptr))
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
        funcs["world.GetLoadedChunks"] = lambda dimension: self._manager.ref(
            GetEngineCompFactory()
            .CreateChunkSource(GetLevelId())
            .GetLoadedChunks(dimension)
        )
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
        funcs["world.LocateNeteaseFeatureRule"] = (
            lambda rule_name, dimension_id, pos_ptr, must_be_in_new_chunk=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateFeature(GetLevelId())
                .LocateNeteaseFeatureRule(
                    rule_name,
                    dimension_id,
                    self._manager.deref(pos_ptr),
                    must_be_in_new_chunk,
                )
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
        funcs["world.MirrorDimension"] = lambda from_id, to_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateDimension(GetLevelId())
            .MirrorDimension(from_id, to_id)
        )
        funcs["world.PlaceFeature"] = (
            lambda feature_name, dimension_id, pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(GetLevelId())
                .PlaceFeature(feature_name, dimension_id, self._manager.deref(pos_ptr))
            )
        )
        funcs["world.PlaceNeteaseLargeFeature"] = (
            lambda pool_name, dimension_id, pos_ptr, rotation, max_depth: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(GetLevelId())
                .PlaceNeteaseLargeFeature(
                    pool_name,
                    dimension_id,
                    self._manager.deref(pos_ptr),
                    rotation,
                    max_depth,
                )
            )
        )
        funcs["world.SetBiomeByPos"] = (
            lambda pos_ptr, biome_name, dim_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateBiome(GetLevelId())
                .SetBiomeByPos(self._manager.deref(pos_ptr), biome_name, dim_id)
            )
        )
        funcs["world.SetBiomeByPosList"] = (
            lambda pos_list_ptr, biome_name, dim_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateBiome(GetLevelId())
                .SetBiomeByPosList(
                    self._manager.deref(pos_list_ptr), biome_name, dim_id
                )
            )
        )
        funcs["world.SetBiomeByVolume"] = (
            lambda min_pos_ptr, max_pos_ptr, biome_name, dim_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateBiome(GetLevelId())
                .SetBiomeByVolume(
                    self._manager.deref(min_pos_ptr),
                    self._manager.deref(max_pos_ptr),
                    biome_name,
                    dim_id,
                )
            )
        )
        funcs["world.SetBiomeInfo"] = (
            lambda biome_name, snow_accumulation_ptr, temperature, downfall, is_rain: self._manager.ref(
                GetEngineCompFactory()
                .CreateBiome(GetLevelId())
                .SetBiomeInfo(
                    biome_name,
                    self._manager.deref(snow_accumulation_ptr),
                    temperature,
                    downfall,
                    is_rain,
                )
            )
        )
        funcs["world.SetMergeSpawnItemRadius"] = lambda radius: self._manager.ref(
            GetEngineCompFactory()
            .CreateGame(GetLevelId())
            .SetMergeSpawnItemRadius(radius)
        )
        funcs["world.CreateEngineEntityByTypeStr"] = (
            self.create_engine_entity_by_type_str
        )
        funcs["world.CreateEntityAOI"] = (
            lambda dimension, name, aabb_ptr, func_name: self._manager.ref(
                GetEngineCompFactory()
                .CreateDimension(GetLevelId())
                .CreateEntityAOI(
                    dimension,
                    name,
                    self._manager.deref(aabb_ptr),
                    lambda args: self._callback(func_name, args),  # type: ignore
                )
            )
        )
        funcs["world.CreateExperienceOrb"] = (
            lambda entity_id, exp, position_ptr, is_special: self._manager.ref(
                GetEngineCompFactory()
                .CreateExp(entity_id)
                .CreateExperienceOrb(exp, self._manager.deref(position_ptr), is_special)
            )
        )
        funcs["world.CreateProjectileEntity"] = self.create_projectile_entity
        funcs["world.DeleteEntityAOI"] = lambda dimension, name: self._manager.ref(
            GetEngineCompFactory()
            .CreateDimension(GetLevelId())
            .DeleteEntityAOI(dimension, name)
        )
        funcs["world.DestroyEntity"] = self.destroy_entity
        funcs["world.GetDroppedItem"] = (
            lambda item_entity_id, get_user_data=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(GetLevelId())
                .GetDroppedItem(item_entity_id, get_user_data)
            )
        )
        funcs["world.GetEngineActor"] = lambda: self._manager.ref(GetEngineActor())
        funcs["world.GetPlayerList"] = lambda: self._manager.ref(GetPlayerList())
        funcs["world.IsEntityAlive"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).IsEntityAlive(entity_id)
        )
        funcs["world.KillEntity"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).KillEntity(entity_id)
        )
        funcs["world.SpawnResources"] = (
            lambda identifier, pos_ptr, aux, probability=1.0, bonus_loot_level=0, dimension_id=-1, allow_randomness=True, spawn_orb=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .SpawnResources(
                    identifier,
                    self._manager.deref(pos_ptr),
                    aux,
                    probability,
                    bonus_loot_level,
                    dimension_id,
                    allow_randomness,
                    spawn_orb,
                )
            )
        )
        funcs["world.SpawnResourcesSilkTouched"] = (
            lambda identifier, pos_ptr, aux, dimension_id=-1: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlockInfo(GetLevelId())
                .SpawnResourcesSilkTouched(
                    identifier, self._manager.deref(pos_ptr), aux, dimension_id
                )
            )
        )
        funcs["world.getEntitiesOrBlockFromRay"] = (
            lambda dimension_id, pos_ptr, rot_ptr, distance=16, is_through=False, filter_type=1: self._manager.ref(
                getEntitiesOrBlockFromRay(
                    dimension_id,
                    self._manager.deref(pos_ptr),
                    self._manager.deref(rot_ptr),
                    distance,
                    is_through,
                    filter_type,  # type: ignore
                )
            )
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
        funcs["world.RegisterBlockPatterns"] = (
            lambda pattern_ptr, defines_ptr, result_actor_name: self._manager.ref(
                GetEngineCompFactory()
                .CreateBlock(GetLevelId())
                .RegisterBlockPatterns(
                    self._manager.deref(pattern_ptr),
                    self._manager.deref(defines_ptr),
                    result_actor_name,
                )
            )
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
