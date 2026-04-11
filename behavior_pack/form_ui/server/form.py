# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable, Any

from mod.server.extraServerApi import (
    GetServerSystemCls,
    GetEngineNamespace,
    GetEngineSystemName,
    GetEngineCompFactory,
    GetHostPlayerId,
    GetLevelId,
)

ServerSystem = GetServerSystemCls()

COMMAND_OPEN_EDITOR = "/菜单编辑器"
DEFAULT_WAIT_SECONDS = 7
DEFAULT_HELP_MESSAGE = (
    "§r§f[§e网络游戏菜单§f] \n"
    + "  §a• 小提示: 在聊天栏执行 §b"
    + COMMAND_OPEN_EDITOR
    + " §a以打开简易菜单编辑器！"
)


class FormSystem(ServerSystem):
    """
    FormSystem 是表单系统在服务端侧实现的接口
    """

    def __init__(self, namespace, system_name):  # type: (str, str) -> None
        """初始化并返回一个新的 FormSystem

        Args:
            namespace (str):
                该表单模组的命名空间
            system_name (str):
                该表单模组在服务端侧的系统名称
        """
        ServerSystem.__init__(self, namespace, system_name)
        self.listen_engine_event("CommandEvent", self, self.on_command_event)
        self.listen_engine_event(
            "ClientLoadAddonsFinishServerEvent", self, self.on_addon_finish_load
        )

    def on_command_event(self, args):  # type: (dict[str, Any]) -> None
        """
        on_command_event 在玩家通过聊天栏执行命令时被调用

        Args:
            args (dict[str, Any]):
                ServerChatEvent 传入的字典参数
        """
        command = args["command"]  # type: str
        if command.strip() != COMMAND_OPEN_EDITOR:
            return

        entity_id = args["entityId"]  # type: str
        engine_comp, level_id = GetEngineCompFactory(), GetLevelId()
        abilities = engine_comp.CreatePlayer(entity_id).GetPlayerAbilities()
        if not abilities["op"] and GetHostPlayerId() != entity_id:
            return

        _ = engine_comp.CreateCommand(level_id).SetCommand(
            "function form_bootstrap/bootstrap", entity_id, False
        )
        _ = engine_comp.CreateGame(level_id).AddTimer(
            0.5,
            lambda: engine_comp.CreateCommand(level_id).SetCommand(
                "function form_bootstrap/main", entity_id, False
            ),  # type: ignore
        )
        engine_comp.CreateMsg(entity_id).NotifyOneMessage(
            entity_id, "§r§a已尝试打开菜单编辑器"
        )

        args["cancel"] = True

    def on_addon_finish_load(self, args):  # type: (dict[str, Any]) -> None
        """on_addon_finish_load 在玩家的客户端完成初始化时被调用

        Args:
            args (dict[str, Any]):
                ClientLoadAddonsFinishServerEvent 传入的字典参数
        """
        player_id = args["playerId"]  # type: str
        game_comp = GetEngineCompFactory()

        abilities = game_comp.CreatePlayer(player_id).GetPlayerAbilities()
        if not abilities["op"] and GetHostPlayerId() != player_id:
            return

        _ = game_comp.CreateGame(GetLevelId()).AddTimer(
            DEFAULT_WAIT_SECONDS,
            lambda: game_comp.CreateMsg(player_id).NotifyOneMessage(
                player_id, DEFAULT_HELP_MESSAGE
            ),  # type: ignore
        )

    def listen_engine_event(
        self, event_name, instance, callback
    ):  # type: (str, Any, Callable[[dict[str, Any]], None]) -> None
        """listen_engine_event 监听引擎事件

        Args:
            event_name (str): 引擎事件名称
            instance (Any): callback 所在类的实例
            callback (Callable[[dict[str, Any]], None]):
                在监听到事件时，调用的函数
        """
        self.ListenForEvent(
            GetEngineNamespace(),
            GetEngineSystemName(),
            event_name,
            instance,
            callback,  # type: ignore
        )
