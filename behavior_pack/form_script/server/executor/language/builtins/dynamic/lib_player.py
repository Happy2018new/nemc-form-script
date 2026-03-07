# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId
from ..static.lib_object import BaseManager


class Player:
    """
    Player 导出了 Mod SDK 中玩家模块的部分接口
    """

    _manager = BaseManager()  # type: BaseManager

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Player

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
        build_func 构建 player 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["player.GetPlayerExp"] = (
            lambda player_id, is_percent=True: self._manager.ref(
                GetEngineCompFactory().CreateExp(player_id).GetPlayerExp(is_percent)
            )
        )
        funcs["player.GetPlayerHunger"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).GetPlayerHunger()
        )
        funcs["player.GetPlayerTotalExp"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreateExp(player_id).GetPlayerTotalExp()
        )
        funcs["player.SetPlayerHunger"] = lambda player_id, value: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).SetPlayerHunger(value)
        )
        funcs["player.SetPlayerPrefixAndSuffixName"] = (
            lambda player_id, prefix, prefix_color, suffix, suffix_color, name_color="": self._manager.ref(
                GetEngineCompFactory()
                .CreateName(player_id)
                .SetPlayerPrefixAndSuffixName(
                    prefix, prefix_color, suffix, suffix_color, name_color
                )
            )
        )
        funcs["player.SetPlayerTotalExp"] = lambda player_id, exp: self._manager.ref(
            GetEngineCompFactory().CreateExp(player_id).SetPlayerTotalExp(exp)
        )
        funcs["player.ChangePlayerDimension"] = (
            lambda player_id, dimension_id, pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreateDimension(player_id)
                .ChangePlayerDimension(dimension_id, self._manager.deref(pos_ptr))
            )
        )
        funcs["player.ChangePlayerFlyState"] = (
            lambda player_id, is_fly, enter_fly=True: self._manager.ref(
                GetEngineCompFactory()
                .CreateFly(player_id)
                .ChangePlayerFlyState(is_fly, enter_fly)
            )
        )
        funcs["player.GetPlayerRespawnPos"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).GetPlayerRespawnPos()
        )
        funcs["player.IsPlayerCanFly"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreateFly(player_id).IsPlayerCanFly()
        )
        funcs["player.IsPlayerFlying"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreateFly(player_id).IsPlayerFlying()
        )
        funcs["player.SetBanPlayerFishing"] = (
            lambda player_id, is_ban: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetBanPlayerFishing(is_ban)
            )
        )
        funcs["player.SetPickUpArea"] = lambda player_id, area: self._manager.ref(
            GetEngineCompFactory()
            .CreatePlayer(player_id)
            .SetPickUpArea(self._manager.deref(area))
        )
        funcs["player.SetPlayerAttackSpeedAmplifier"] = (
            lambda player_id, amplifier: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetPlayerAttackSpeedAmplifier(amplifier)
            )
        )
        funcs["player.SetPlayerMotion"] = lambda entity_id, motion: self._manager.ref(
            GetEngineCompFactory()
            .CreateActorMotion(entity_id)
            .SetPlayerMotion(self._manager.deref(motion))
        )
        funcs["player.SetPlayerRespawnPos"] = (
            lambda player_id, pos_ptr: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetPlayerRespawnPos(self._manager.deref(pos_ptr), dimensionId=0)
            )
        )
        funcs["player.isSneaking"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).isSneaking()
        )
        funcs["player.isSwimming"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).isSwimming()
        )
        funcs["player.AddEnchantToInvItem"] = (
            lambda player_id, slot_pos, enchant_type, level: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .AddEnchantToInvItem(slot_pos, enchant_type, level)
            )
        )
        funcs["player.AddModEnchantToInvItem"] = (
            lambda player_id, slot_pos, mod_enchant_id, level: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .AddModEnchantToInvItem(slot_pos, mod_enchant_id, level)
            )
        )
        funcs["player.ChangePlayerItemTipsAndExtraId"] = (
            lambda player_id, pos_type, slot_pos, custom_tips="", extra_id="": self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .ChangePlayerItemTipsAndExtraId(
                    pos_type, slot_pos, custom_tips, extra_id
                )
            )
        )
        funcs["player.ChangeSelectSlot"] = lambda player_id, slot: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).ChangeSelectSlot(slot)
        )
        funcs["player.GetInvItemEnchantData"] = (
            lambda player_id, slot_pos: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .GetInvItemEnchantData(slot_pos)
            )
        )
        funcs["player.GetInvItemModEnchantData"] = (
            lambda player_id, slot_pos: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .GetInvItemModEnchantData(slot_pos)
            )
        )
        funcs["player.GetPlayerItem"] = (
            lambda player_id, pos_type, slot_type, get_user_data=False: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .GetPlayerItem(pos_type, slot_type, get_user_data)
            )
        )
        funcs["player.GetSelectSlotId"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreateItem(player_id).GetSelectSlotId()
        )
        funcs["player.RemoveEnchantToInvItem"] = (
            lambda player_id, slot_pos, enchant_type: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .RemoveEnchantToInvItem(slot_pos, enchant_type)
            )
        )
        funcs["player.RemoveModEnchantToInvItem"] = (
            lambda player_id, slot_pos, mod_enchant_id: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .RemoveModEnchantToInvItem(slot_pos, mod_enchant_id)
            )
        )
        funcs["player.SetInvItemExchange"] = (
            lambda player_id, pos1, pos2: self._manager.ref(
                GetEngineCompFactory()
                .CreateItem(player_id)
                .SetInvItemExchange(pos1, pos2)
            )
        )
        funcs["player.GetPlayerGameType"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreateGame(GetLevelId()).GetPlayerGameType(player_id)
        )
        funcs["player.SetPlayerGameType"] = (
            lambda player_id, game_type: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetPlayerGameType(game_type)
            )
        )
        funcs["player.GetPlayerAbilities"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).GetPlayerAbilities()
        )
        funcs["player.GetPlayerOperation"] = lambda player_id: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).GetPlayerOperation()
        )
        funcs["player.SetAttackMobsAbility"] = (
            lambda player_id, can_attack: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetAttackMobsAbility(can_attack)
            )
        )
        funcs["player.SetAttackPlayersAbility"] = (
            lambda player_id, can_attack: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetAttackPlayersAbility(can_attack)
            )
        )
        funcs["player.SetBuildAbility"] = (
            lambda player_id, can_build: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetBuildAbility(can_build)
            )
        )
        funcs["player.SetMineAbility"] = lambda player_id, can_mine: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).SetMineAbility(can_mine)
        )
        funcs["player.SetOpenContainersAbility"] = (
            lambda player_id, can_open: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetOpenContainersAbility(can_open)
            )
        )
        funcs["player.SetOperateDoorsAndSwitchesAbility"] = (
            lambda player_id, can_operate: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetOperateDoorsAndSwitchesAbility(can_operate)
            )
        )
        funcs["player.SetOperatorCommandAbility"] = (
            lambda player_id, can_operate: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetOperatorCommandAbility(can_operate)
            )
        )
        funcs["player.SetPermissionLevel"] = lambda player_id, level: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).SetPermissionLevel(level)
        )
        funcs["player.SetPlayerMute"] = lambda player_id, is_mute: self._manager.ref(
            GetEngineCompFactory().CreatePlayer(player_id).SetPlayerMute(is_mute)
        )
        funcs["player.SetTeleportAbility"] = (
            lambda player_id, can_teleport: self._manager.ref(
                GetEngineCompFactory()
                .CreatePlayer(player_id)
                .SetTeleportAbility(can_teleport)
            )
        )

        for key, value in funcs.items():
            origin[key] = value
