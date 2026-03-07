# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId
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

    def set_mob_knockback(
        self, entity_id, xd=0.1, zd=0.1, power=1.0, height=1.0, height_cap=1.0
    ):  # type: (str, float, float, float, float, float) -> bool
        """
        设置击退的初始速度，需要考虑阻力的影响

        Args:
            entity_id (str): 目标实体的 ID
            xd (float, optional):
                x 轴方向，用来控制角度。
                默认值为 0.1
            zd (float, optional):
                z 轴方向，用来控制角度。
                默认值为 0.1
            power (float, optional):
                用来控制水平方向的初速度。
                默认值为 1.0
            height (float, optional):
                竖直方向的初速度。
                默认值为 1.0
            height_cap (float, optional):
                向上速度阈值，当实体本身已经有向上的速度时需要考虑这个值，
                用来确保最终向上的速度不会超过 height_cap。
                默认值为 1.0

        Returns:
            bool: 总是返回 True
        """
        GetEngineCompFactory().CreateAction(entity_id).SetMobKnockback(
            xd, zd, power, height, height_cap
        )
        return True

    def set_persistence(self, entity_id, is_persistent):  # type: (str, bool) -> bool
        """
        设置实体是否持久化

        Args:
            entity_id (str): 目标实体的 ID
            is_persistent (bool): 目标实体是否持久化

        Returns:
            bool: 总是返回 True
        """
        GetEngineCompFactory().CreatePersistence(entity_id).SetPersistence(
            is_persistent
        )
        return True

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
        funcs["entity.GetEntityDefinitions"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .GetEntityDefinitions()
        )
        funcs["entity.GetEntityNBTTags"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).GetEntityNBTTags()
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
        funcs["entity.GetAllComponentsName"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityComponent(entity_id)
            .GetAllComponentsName()
        )
        funcs["entity.GetAttrMaxValue"] = lambda entity_id, type: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).GetAttrMaxValue(type)
        )
        funcs["entity.GetAttrValue"] = lambda entity_id, attr_type: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).GetAttrValue(attr_type)
        )
        funcs["entity.GetCurrentAirSupply"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateBreath(entity_id).GetCurrentAirSupply()
        )
        funcs["entity.GetDeathTime"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).GetDeathTime()
        )
        funcs["entity.GetEntitiesBySelector"] = (
            lambda entity_id, command: self._manager.ref(
                GetEngineCompFactory()
                .CreateEntityComponent(entity_id)
                .GetEntitiesBySelector(command)
            )
        )
        funcs["entity.GetEntityDamage"] = (
            lambda entity_id, target_entity_id=None: self._manager.ref(
                GetEngineCompFactory()
                .CreateGame(GetLevelId())
                .GetEntityDamage(entity_id, target_entity_id)  # type: ignore
            )
        )
        funcs["entity.GetEntityDimensionId"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateDimension(entity_id).GetEntityDimensionId()
        )
        funcs["entity.GetEntityFallDistance"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .GetEntityFallDistance()
        )
        funcs["entity.GetEntityLinksTag"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .GetEntityLinksTag()
        )
        funcs["entity.GetEntityOwner"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateActorOwner(entity_id).GetEntityOwner()
        )
        funcs["entity.GetFootPos"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreatePos(entity_id).GetFootPos()
        )
        funcs["entity.GetGravity"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateGravity(entity_id).GetGravity()
        )
        funcs["entity.GetMarkVariant"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).GetMarkVariant()
        )
        funcs["entity.GetMaxAirSupply"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateBreath(entity_id).GetMaxAirSupply()
        )
        funcs["entity.GetMobColor"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).GetMobColor()
        )
        funcs["entity.GetMobStrength"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).GetMobStrength()
        )
        funcs["entity.GetMobStrengthMax"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .GetMobStrengthMax()
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
        funcs["entity.GetSize"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateCollisionBox(entity_id).GetSize()
        )
        funcs["entity.GetTradeLevel"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).GetTradeLevel()
        )
        funcs["entity.GetTypeFamily"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).GetTypeFamily()
        )
        funcs["entity.GetUnitBubbleAirSupply"] = lambda: self._manager.ref(
            GetEngineCompFactory().CreateBreath(GetLevelId()).GetUnitBubbleAirSupply()
        )
        funcs["entity.GetVariant"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).GetVariant()
        )
        funcs["entity.HasChest"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).HasChest()
        )
        funcs["entity.HasComponent"] = lambda entity_id, attr_type: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityComponent(entity_id)
            .HasComponent(attr_type)
        )
        funcs["entity.HasSaddle"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).HasSaddle()
        )
        funcs["entity.IsAngry"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsAngry()
        )
        funcs["entity.IsBaby"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsBaby()
        )
        funcs["entity.IsConsumingAirSupply"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateBreath(entity_id).IsConsumingAirSupply()
        )
        funcs["entity.IsIllagerCaptain"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsIllagerCaptain()
        )
        funcs["entity.IsNaturallySpawned"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .IsNaturallySpawned()
        )
        funcs["entity.IsOutOfControl"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsOutOfControl()
        )
        funcs["entity.IsPregnant"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsPregnant()
        )
        funcs["entity.IsSheared"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsSheared()
        )
        funcs["entity.IsSitting"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsSitting()
        )
        funcs["entity.IsTamed"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsTamed()
        )
        funcs["entity.PromoteToIllagerCaptain"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .PromoteToIllagerCaptain()
        )
        funcs["entity.ResetToDefaultValue"] = (
            lambda entity_id, attr_type: self._manager.ref(
                GetEngineCompFactory()
                .CreateAttr(entity_id)
                .ResetToDefaultValue(attr_type)
            )
        )
        funcs["entity.ResetToMaxValue"] = (
            lambda entity_id, attr_type: self._manager.ref(
                GetEngineCompFactory().CreateAttr(entity_id).ResetToMaxValue(attr_type)
            )
        )
        funcs["entity.SetAngry"] = (
            lambda entity_id, is_angry, targer_id="": self._manager.ref(
                GetEngineCompFactory()
                .CreateEntityDefinitions(entity_id)
                .SetAngry(is_angry, targer_id)
            )
        )
        funcs["entity.SetAsAdult"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).SetAsAdult()
        )
        funcs["entity.SetAttrMaxValue"] = (
            lambda entity_id, attr_type, value: self._manager.ref(
                GetEngineCompFactory()
                .CreateAttr(entity_id)
                .SetAttrMaxValue(attr_type, value)
            )
        )
        funcs["entity.SetAttrValue"] = (
            lambda entity_id, attr_type, value, set_default=1: self._manager.ref(
                GetEngineCompFactory()
                .CreateAttr(entity_id)
                .SetAttrValue(attr_type, value, set_default)
            )
        )
        funcs["entity.SetChest"] = lambda entity_id, has_chest: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .SetChest(has_chest)
        )
        funcs["entity.SetCurrentAirSupply"] = lambda entity_id, data: self._manager.ref(
            GetEngineCompFactory().CreateBreath(entity_id).SetCurrentAirSupply(data)
        )
        funcs["entity.SetEntityLookAtPos"] = (
            lambda entity_id, target_pos, min_time, max_time, reject: self._manager.ref(
                GetEngineCompFactory()
                .CreateRot(entity_id)
                .SetEntityLookAtPos(
                    self._manager.deref(target_pos), min_time, max_time, reject
                )
            )
        )
        funcs["entity.SetEntityOwner"] = lambda entity_id, target_id: self._manager.ref(
            GetEngineCompFactory().CreateActorOwner(entity_id).SetEntityOwner(target_id)
        )
        funcs["entity.SetGravity"] = lambda entity_id, gravity: self._manager.ref(
            GetEngineCompFactory().CreateGravity(entity_id).SetGravity(gravity)
        )
        funcs["entity.SetMarkVariant"] = (
            lambda entity_id, variant_type: self._manager.ref(
                GetEngineCompFactory()
                .CreateEntityDefinitions(entity_id)
                .SetMarkVariant(variant_type)
            )
        )
        funcs["entity.SetMaxAirSupply"] = lambda entity_id, data: self._manager.ref(
            GetEngineCompFactory().CreateBreath(entity_id).SetMaxAirSupply(data)
        )
        funcs["entity.SetMobColor"] = lambda entity_id, color_type: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .SetMobColor(color_type)
        )
        funcs["entity.SetMobStrength"] = lambda entity_id, strength: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .SetMobStrength(strength)
        )
        funcs["entity.SetMobStrengthMax"] = (
            lambda entity_id, strength: self._manager.ref(
                GetEngineCompFactory()
                .CreateEntityDefinitions(entity_id)
                .SetMobStrengthMax(strength)
            )
        )
        funcs["entity.SetName"] = lambda entity_id, name: self._manager.ref(
            GetEngineCompFactory().CreateName(entity_id).SetName(name)
        )
        funcs["entity.SetOutOfControl"] = (
            lambda entity_id, is_put_of_control: self._manager.ref(
                GetEngineCompFactory()
                .CreateEntityDefinitions(entity_id)
                .SetOutOfControl(is_put_of_control)
            )
        )
        funcs["entity.SetPersistent"] = lambda entity_id, persistent: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).SetPersistent(persistent)
        )
        funcs["entity.SetPos"] = lambda entity_id, pos_ptr: self._manager.ref(
            GetEngineCompFactory()
            .CreatePos(entity_id)
            .SetPos(self._manager.deref(pos_ptr))
        )
        funcs["entity.SetRecoverTotalAirSupplyTime"] = (
            lambda entity_id, time_sec: self._manager.ref(
                GetEngineCompFactory()
                .CreateBreath(entity_id)
                .SetRecoverTotalAirSupplyTime(time_sec)
            )
        )
        funcs["entity.SetRot"] = lambda entity_id, rot_ptr: self._manager.ref(
            GetEngineCompFactory()
            .CreateRot(entity_id)
            .SetRot(self._manager.deref(rot_ptr))
        )
        funcs["entity.SetSheared"] = lambda entity_id, is_sheared: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .SetSheared(is_sheared)
        )
        funcs["entity.SetSitting"] = (
            lambda entity_id, should_sit_down: self._manager.ref(
                GetEngineCompFactory()
                .CreateEntityDefinitions(entity_id)
                .SetSitting(should_sit_down)
            )
        )
        funcs["entity.SetSize"] = lambda entity_id, size: self._manager.ref(
            GetEngineCompFactory()
            .CreateCollisionBox(entity_id)
            .SetSize(self._manager.deref(size))
        )
        funcs["entity.SetTradeLevel"] = lambda entity_id, holder_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .SetTradeLevel(holder_id)
        )
        funcs["entity.SetVariant"] = lambda entity_id, variant_type: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .SetVariant(variant_type)
        )
        funcs["entity.GetAttackTarget"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAction(entity_id).GetAttackTarget()
        )
        funcs["entity.GetBlockControlAi"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateControlAi(entity_id).GetBlockControlAi()
        )
        funcs["entity.GetComponents"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityEvent(entity_id).GetComponents()
        )
        funcs["entity.GetJumpPower"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateGravity(entity_id).GetJumpPower()
        )
        funcs["entity.GetLeashHolder"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).GetLeashHolder()
        )
        funcs["entity.GetMotion"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateActorMotion(entity_id).GetMotion()
        )
        funcs["entity.GetOwnerId"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateTame(entity_id).GetOwnerId()
        )
        funcs["entity.GetStepHeight"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).GetStepHeight()
        )
        funcs["entity.ImmuneDamage"] = lambda entity_id, immune: self._manager.ref(
            GetEngineCompFactory().CreateHurt(entity_id).ImmuneDamage(immune)
        )
        funcs["entity.IsEating"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsEating()
        )
        funcs["entity.IsEntityOnFire"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).IsEntityOnFire()
        )
        funcs["entity.IsLootDropped"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsLootDropped()
        )
        funcs["entity.IsPersistent"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsPersistent()
        )
        funcs["entity.IsRoaring"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsRoaring()
        )
        funcs["entity.IsStunned"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateEntityDefinitions(entity_id).IsStunned()
        )
        funcs["entity.ResetAttackTarget"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAction(entity_id).ResetAttackTarget()
        )
        funcs["entity.ResetMotion"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateActorMotion(entity_id).ResetMotion()
        )
        funcs["entity.ResetStepHeight"] = lambda entity_id: self._manager.ref(
            GetEngineCompFactory().CreateAttr(entity_id).ResetStepHeight()
        )
        funcs["entity.SetActorCollidable"] = (
            lambda entity_id, is_collidable: self._manager.ref(
                GetEngineCompFactory()
                .CreateActorCollidable(entity_id)
                .SetActorCollidable(is_collidable)
            )
        )
        funcs["entity.SetActorPushable"] = (
            lambda entity_id, is_pushable: self._manager.ref(
                GetEngineCompFactory()
                .CreateActorPushable(entity_id)
                .SetActorPushable(is_pushable)
            )
        )
        funcs["entity.SetAttackTarget"] = (
            lambda entity_id, target_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateAction(entity_id)
                .SetAttackTarget(target_id)
            )
        )
        funcs["entity.SetBlockControlAi"] = (
            lambda entity_id, is_block, freeze_anim=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateControlAi(entity_id)
                .SetBlockControlAi(is_block, freeze_anim)
            )
        )
        funcs["entity.SetEntityOnFire"] = (
            lambda entity_id, seconds, burn_damage=1: self._manager.ref(
                GetEngineCompFactory()
                .CreateAttr(entity_id)
                .SetEntityOnFire(seconds, burn_damage)
            )
        )
        funcs["entity.SetEntityTamed"] = lambda entity_id, player_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateTame(entity_id)
            .SetEntityTamed(player_id, entity_id)
        )
        funcs["entity.SetJumpPower"] = lambda entity_id, jump_power: self._manager.ref(
            GetEngineCompFactory().CreateGravity(entity_id).SetJumpPower(jump_power)
        )
        funcs["entity.SetLeashHolder"] = lambda entity_id, holder_id: self._manager.ref(
            GetEngineCompFactory()
            .CreateEntityDefinitions(entity_id)
            .SetLeashHolder(holder_id)
        )
        funcs["entity.SetLootDropped"] = (
            lambda entity_id, is_loot_dropped: self._manager.ref(
                GetEngineCompFactory()
                .CreateEntityDefinitions(entity_id)
                .SetLootDropped(is_loot_dropped)
            )
        )
        funcs["entity.SetMobKnockback"] = self.set_mob_knockback
        funcs["entity.SetMotion"] = lambda entity_id, motion: self._manager.ref(
            GetEngineCompFactory().CreateActorMotion(entity_id).SetMotion(motion)
        )
        funcs["entity.SetPersistence"] = self.set_persistence
        funcs["entity.SetStepHeight"] = (
            lambda entity_id, step_height: self._manager.ref(
                GetEngineCompFactory().CreateAttr(entity_id).SetStepHeight(step_height)
            )
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
