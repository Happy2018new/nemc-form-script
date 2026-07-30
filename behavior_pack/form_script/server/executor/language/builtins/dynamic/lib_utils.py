# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable
    from ....executor import GameCodeExecutor

import heapq
import threading
from .const import CONST_ALL_TEXTURES
from ..static.lib_object import BaseManager
from mod.server.extraServerApi import GetEngineCompFactory, GetMinecraftEnum


class GameTickTimer:
    """
    GameTickTimer 是延迟调度实现，
    以用于延迟执行命令或自定义函数
    """

    _seq = 0  # type: int
    _base = 0  # type: int
    _heap = []  # type: list[tuple[int, int, Callable[..., None]]]
    _locker = None  # type: threading.RLock | None

    def __init__(self):
        """
        初始化并返回一个新的 GameTickTimer
        """
        self._seq = 0
        self._base = 0
        self._heap = []
        self._locker = threading.RLock()

    def _consume(self):  # type: () -> list[Callable[..., None]]
        """
        _consume 消费并返回所有到期的回调函数。
        它是一个内部实现细节，不应被外部实现调用

        Returns:
            list[Callable[..., None]]:
                所有到期的并应执行的回调函数
        """
        result = []
        while len(self._heap) > 0 and self._heap[0][0] <= self._base:
            _, _, callback = heapq.heappop(self._heap)
            result.append(callback)
        return result

    def schedule(self, ticks, callback):  # type: (int, Callable[..., None]) -> None
        """
        schedule 安排回调函数 callback 于 ticks 个游戏刻后执行

        Args:
            ticks (int):
                给出的游戏刻数
            callback (Callable[..., None]):
                欲执行的回调函数
        """
        assert self._locker is not None

        if ticks < 0:
            raise Exception("schedule: Can not schedule a delay in the past")
        if ticks == 0:
            callback()
            return

        with self._locker:
            self._seq += 1
            heapq.heappush(self._heap, (self._base + ticks, self._seq, callback))

    def on_tick(self, _):  # type: (dict[str, Any]) -> None
        """
        on_tick 由外部调用者在每个游戏刻调用一次。
        每次调用时，它将试图消费所有到期的回调函数

        Args:
            _ (dict[str, Any]):
                OnSimTickServerEvent 传入的字典参数
        """
        assert self._locker is not None

        with self._locker:
            if len(self._heap) == 0:
                self._seq = 0
                self._base = 0
                return
            self._base += 1
            funcs = self._consume()

        for func in funcs:
            try:
                func()
            except Exception:
                pass


class Utils:
    """
    Utils 提供了一些辅助性函数
    """

    _manager = BaseManager()  # type: BaseManager
    _timer = None  # type: GameTickTimer | None
    _callback = None  # type: Callable[[str, dict[str, Any] | tuple], None] | None
    _executor = None  # type: GameCodeExecutor | None

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Utils

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager
        self._timer = GameTickTimer()
        self._callback = None
        self._executor = None

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

    def add_ench(
        self, entity_id, pos_type, slot_pos, ench_id, ench_level
    ):  # type: (str, int, int, int, int) -> bool
        """
        add_ench 向实体中特定位置的物品添加原版附魔。
        如果目标附魔魔咒已经存在，则它仅设置附魔等级

        Args:
            entity_id (str):
                目标实体的 ID
            pos_type (int):
                ItemPosType 枚举值
            slot_pos (int):
                物品所在的槽位
            ench_id (int):
                欲添加的附魔 ID
            ench_level (int):
                欲设置的附魔等级

        Returns:
            bool:
                如果操作成功，则返回 True；
                否则操作失败，那么返回 False
        """
        engine_comp = GetEngineCompFactory()
        item_comp = engine_comp.CreateItem(entity_id)
        const_enum = GetMinecraftEnum()

        entity_type = engine_comp.CreateEngineType(entity_id).GetEngineType()
        if entity_type is None:
            return False
        is_player = entity_type == const_enum.EntityType.Player

        if is_player:
            item = item_comp.GetPlayerItem(pos_type, slot_pos, True)
        else:
            item = item_comp.GetEntityItem(pos_type, slot_pos, True)
        if item is None:
            return False

        user_data = item["userData"]
        if user_data is None:
            user_data = {}
        ench_data = user_data.get("ench", [])  # type: list[dict[str, dict[str, Any]]]

        hit_ench = False
        for index, value in enumerate(ench_data):
            if value["id"]["__value__"] == ench_id:
                hit_ench = True
                ench_data[index]["lvl"]["__value__"] = ench_level
                break
        if not hit_ench:
            ench_data.append(
                {
                    "id": {"__type__": 2, "__value__": ench_id},
                    "lvl": {"__type__": 2, "__value__": ench_level},
                    "modEnchant": {"__type__": 8, "__value__": ""},
                }
            )

        user_data["ench"] = ench_data
        item["userData"] = user_data
        if "enchantData" in item:
            del item["enchantData"]

        if is_player and pos_type == const_enum.ItemPosType.INVENTORY:
            _ = item_comp.SetInvItemNum(slot_pos, 0)
            return item_comp.SpawnItemToPlayerInv(item, entity_id, slot_pos)
        else:
            return item_comp.SetEntityItem(pos_type, item, slot_pos)

    def del_ench(
        self, entity_id, pos_type, slot_pos, ench_id
    ):  # type: (str, int, int, int) -> bool
        """
        del_ench 将一个附魔魔咒从实体中特定位置的物品中移除

        Args:
            entity_id (str):
                目标实体的 ID
            pos_type (int):
                ItemPosType 枚举值
            slot_pos (int):
                物品所在的槽位
            ench_id (int):
                要移除的附魔 ID

        Returns:
            bool:
                如果魔咒存在，并且操作成功，则返回 True；
                否则操作失败，那么返回 False
        """
        engine_comp = GetEngineCompFactory()
        item_comp = engine_comp.CreateItem(entity_id)
        const_enum = GetMinecraftEnum()

        entity_type = engine_comp.CreateEngineType(entity_id).GetEngineType()
        if entity_type is None:
            return False
        is_player = entity_type == const_enum.EntityType.Player

        if is_player:
            item = item_comp.GetPlayerItem(pos_type, slot_pos, True)
        else:
            item = item_comp.GetEntityItem(pos_type, slot_pos, True)
        if item is None:
            return False

        user_data = item["userData"]
        if user_data is None:
            user_data = {}
        ench_data = user_data.get("ench", [])  # type: list[dict[str, dict[str, Any]]]

        for index, value in enumerate(ench_data):
            if value["id"]["__value__"] == ench_id:
                del ench_data[index]
                break
        else:
            return False

        user_data["ench"] = ench_data
        item["userData"] = user_data
        if "enchantData" in item:
            del item["enchantData"]
        if len(ench_data) == 0 and "ench" in user_data:
            del user_data["ench"]

        if is_player and pos_type == const_enum.ItemPosType.INVENTORY:
            _ = item_comp.SetInvItemNum(slot_pos, 0)
            return item_comp.SpawnItemToPlayerInv(item, entity_id, slot_pos)
        else:
            return item_comp.SetEntityItem(pos_type, item, slot_pos)

    def async_run_func(self, delay, func_name, *args):  # type: (int, str, ...) -> bool
        """
        async_run_func 以异步的方式延迟执行自定义函数

        Args:
            delay (int):
                延迟的游戏刻数
            func_name (str):
                要调用的自定义函数名称

        Returns:
            bool: 总是返回 True
        """
        assert self._timer is not None
        assert self._executor is not None

        ctx = self._executor.execute_context()
        eid = ctx.get_executor()

        def callback():
            assert self._callback is not None
            backup = ctx.current_context()

            try:
                ctx.fast_set(eid, False)
            except Exception:
                pass
            try:
                self._callback(func_name, args)
            finally:
                ctx.recover_context(backup)

        self._timer.schedule(delay, callback)
        return True

    def async_run_cmd(self, delay, command):  # type: (int, str) -> bool
        """
        async_run_cmd 以异步的方式延迟执行命令


        Args:
            delay (int):
                延迟的游戏刻数
            command (str):
                要执行的命令

        Returns:
            bool: 总是返回 True
        """
        assert self._timer is not None
        assert self._executor is not None

        ctx = self._executor.execute_context()
        eid = ctx.get_executor()

        def callback():
            assert self._executor is not None
            assert self._executor._game_interact is not None

            backup = ctx.current_context()
            interact = self._executor._game_interact

            try:
                ctx.fast_set(eid, False)
            except Exception:
                pass
            try:
                _ = interact.command_func()(command)
            finally:
                ctx.recover_context(backup)

        self._timer.schedule(delay, callback)
        return True

    def dynamic_register(
        self, callback, executor
    ):  # type: (Callable[[str, dict[str, Any] | tuple], None], GameCodeExecutor) -> None
        """
        dynamic_register 向底层动态地注册实现，
        于是依赖库可以调用环路引用上已实现的接口

        Args:
            callback (Callable[[str, dict[str, Any] | tuple], None]):
                用于回调执行自定义函数的实现
            executor (GameCodeExecutor):
                用户代码的执行器
        """
        self._callback = callback
        self._executor = executor

    def get_timer(self):  # type: () -> GameTickTimer
        """
        get_timer 返回 Utils 的内部延迟调度器

        Returns:
            GameTickTimer: 延迟调度器
        """
        assert self._timer is not None
        return self._timer

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
        funcs["utils.add_ench"] = self.add_ench
        funcs["utils.del_ench"] = self.del_ench
        funcs["utils.async_run_func"], funcs["gofn"] = (
            self.async_run_func,
            self.async_run_func,
        )
        funcs["utils.async_run_cmd"], funcs["gocmd"] = (
            self.async_run_cmd,
            self.async_run_cmd,
        )

        for key, value in funcs.items():
            origin[key] = value
