# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from mod.server.extraServerApi import GetEngineCompFactory
from ..static.lib_object import BaseManager


class Entity:
    """
    Entity 导出了 Mod SDK 中实体模块的部分接口
    """

    _manager = BaseManager()  # type: BaseManager

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Entity

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
        build_func 构建 entity 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["entity.GetEngineType"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEngineType(entity_id).GetEngineType()
        )
        funcs["entity.GetEngineTypeStr"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEngineType(entity_id).GetEngineTypeStr()
        )
        funcs["entity.GetAuxValue"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAuxValue(entity_id).GetAuxValue()
        )
        funcs["entity.ChangeEntityDimension"] = (
            lambda entity_id, dimension_id, pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateDimension(entity_id)
                .ChangeEntityDimension(dimension_id, self._manager.deref(pos_ptr))
            )
        )
        funcs["entity.GetAttrMaxValue"] = lambda entity_id, type: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).GetAttrMaxValue(type)
        )
        funcs["entity.GetAttrValue"] = lambda entity_id, attr_type: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).GetAttrValue(attr_type)
        )
        funcs["entity.GetEntitiesBySelector"] = (
            lambda entity_id, command: self._manager.ref(
                GetEngineCompFactory()
                .CreateEntityComponent(entity_id)
                .GetEntitiesBySelector(command)
            )
        )
        funcs["entity.GetEntityDimensionId"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateDimension(entity_id).GetEntityDimensionId()
        )
        funcs["entity.GetEntityOwner"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateActorOwner(entity_id).GetEntityOwner()
        )
        funcs["entity.GetGravity"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateGravity(entity_id).GetGravity()
        )
        funcs["entity.GetName"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateName(entity_id).GetName()
        )
        funcs["entity.GetPos"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreatePos(entity_id).GetPos()
        )
        funcs["entity.GetRot"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateRot(entity_id).GetRot()
        )
        funcs["entity.GetTypeFamily"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).GetTypeFamily()
        )
        funcs["entity.SetAttrValue"] = (
            lambda entity_id, attr_type, value: self._manager.ref(
                GetEngineCompFactory()
                .CreateAttr(entity_id)
                .SetAttrValue(attr_type, value, setDefault=1)
            )
        )
        funcs["entity.SetEntityOwner"] = lambda entity_id, target_id: self._manager.ref(
            GetEngineCompFactory().CreateActorOwner(entity_id).SetEntityOwner(target_id)
        )
        funcs["entity.SetGravity"] = lambda entity_id, gravity: self._manager.ref(
            GetEngineCompFactory().CreateGravity(entity_id).SetGravity(gravity)
        )
        funcs["entity.SetName"] = lambda entity_id, name: self._manager.ref(
            GetEngineCompFactory().CreateName(entity_id).SetName(name)
        )
        funcs["entity.SetPos"] = lambda entity_id, pos_ptr: self._manager.ref(
            GetEngineCompFactory()
            .CreatePos(entity_id)
            .SetPos(self._manager.deref(pos_ptr))
        )
        funcs["entity.SetRot"] = lambda entity_id, rot_ptr: self._manager.ref(
            GetEngineCompFactory()
            .CreateRot(entity_id)
            .SetRot(self._manager.deref(rot_ptr))
        )
        funcs["entity.GetAttackTarget"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAction(entity_id).GetAttackTarget()
        )
        funcs["entity.GetMotion"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateActorMotion(entity_id).GetMotion()
        )
        funcs["entity.GetOwnerId"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateTame(entity_id).GetOwnerId()
        )
        funcs["entity.ResetAttackTarget"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAction(entity_id).ResetAttackTarget()
        )
        funcs["entity.ResetMotion"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateActorMotion(entity_id).ResetMotion()
        )
        funcs["entity.SetAttackTarget"] = (
            lambda entity_id, target_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateAction(entity_id)
                .SetAttackTarget(target_id)
            )
        )
        funcs["entity.SetMotion"] = lambda entity_id, motion: self._manager.ref(
            GetEngineCompFactory().CreateActorMotion(entity_id).SetMotion(motion)
        )
        funcs["entity.AddEffectToEntity"] = (
            lambda entity_id, effect_name, duration, amplifier, show_particles: self._manager.ref(
                GetEngineCompFactory()
                .CreateEffect(entity_id)
                .AddEffectToEntity(effect_name, duration, amplifier, show_particles)
            )
        )
        funcs["entity.GetAllEffects"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEffect(entity_id).GetAllEffects()
        )
        funcs["entity.HasEffect"] = lambda entity_id, effect_name: self._manager.ref(
            GetEngineCompFactory().CreateEffect(entity_id).HasEffect(effect_name)
        )
        funcs["entity.RemoveEffectFromEntity"] = (
            lambda entity_id, effect_name: self._manager.ref(
                GetEngineCompFactory()
                .CreateEffect(entity_id)
                .RemoveEffectFromEntity(effect_name)
            )
        )
        funcs["entity.GetEntityItem"] = (
            lambda entity_id, pos_type, slot_pos, get_user_data=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(entity_id)
                .GetEntityItem(pos_type, slot_pos, get_user_data)
            )
        )
        funcs["entity.GetEquItemEnchant"] = (
            lambda player_id, slot_pos: self._manager.ref(
                GetEngineCompFactory().CreateItem(player_id).GetEquItemEnchant(slot_pos)
            )
        )
        funcs["entity.GetEquItemModEnchant"] = (
            lambda player_id, slot_pos: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .GetEquItemModEnchant(slot_pos)
            )
        )
        funcs["entity.CleanExtraData"] = lambda entity_id, key: self._manager.ref(
            GetEngineCompFactory().CreateExtraData(entity_id).CleanExtraData(key)
        )
        funcs["entity.GetExtraData"] = lambda entity_id, key: self._manager.ref(
            GetEngineCompFactory().CreateExtraData(entity_id).GetExtraData(key)
        )
        funcs["entity.GetWholeExtraData"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateExtraData(entity_id).GetWholeExtraData()
        )
        funcs["entity.SaveExtraData"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateExtraData(entity_id).SaveExtraData()
        )
        funcs["entity.SetExtraData"] = (
            lambda entity_id, key, val_or_ptr, is_ptr=False, auto_save=True: self._manager.ref(
                GetEngineCompFactory()
                .CreateExtraData(entity_id)
                .SetExtraData(
                    key,
                    val_or_ptr if not is_ptr else self._manager.deref(val_or_ptr),
                    auto_save,
                )
            )
        )
        funcs["entity.AddEntityTag"] = lambda entity_id, tag: self._manager.ref(
            GetEngineCompFactory().CreateTag(entity_id).AddEntityTag(tag)
        )
        funcs["entity.EntityHasTag"] = lambda entity_id, tag: self._manager.ref(
            GetEngineCompFactory().CreateTag(entity_id).EntityHasTag(tag)
        )
        funcs["entity.GetEntityTags"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateTag(entity_id).GetEntityTags()
        )
        funcs["entity.RemoveEntityTag"] = lambda entity_id, tag: self._manager.ref(
            GetEngineCompFactory().CreateTag(entity_id).RemoveEntityTag(tag)
        )
        funcs["entity.GetSourceEntityId"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateBulletAttributes(entity_id).GetSourceEntityId()
        )
        funcs["entity.GetOrbExperience"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateExp(entity_id).GetOrbExperience()
        )
        funcs["entity.SetOrbExperience"] = lambda entity_id, exp: self._manager.ref(
            GetEngineCompFactory().CreateExp(entity_id).SetOrbExperience(exp)
        )

        for key, value in funcs.items():
            origin[key] = value
