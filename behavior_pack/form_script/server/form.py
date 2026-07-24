# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

from .cmd import CommandHandlers
from .storage.base import StorageManager
from .storage.form import FormStorage
from .storage.function import FunctionStorage
from .storage.event import EventStorage
from .executor.cache import CompileCache
from .executor.executor import GameCodeExecutor
from .feature.form import FormFeature
from .feature.function import FunctionFeature
from .feature.event import EventFeature
from .feature.debug import DebugFeature
from ..packet.packet import (
    PACKET_NAME_MODAL_FORM_RESPONSE,
    PACKET_NAME_CUSTOM_FUNCTION_CALL,
    ModalFormResponse,
    CustomFunctionCall,
)
from mod.server.extraServerApi import (
    GetServerSystemCls,
    GetEngineNamespace,
    GetEngineSystemName,
    GetEngineCompFactory,
    GetHostPlayerId,
    GetLevelId,
)

ServerSystem = GetServerSystemCls()

MESSAGE_GEN_TURORIAL = "生成自定义菜单示例"
COMMAND_OPEN_EDITOR = "/菜单编辑器"

DEFAULT_WAIT_SECONDS = 7
DEFAULT_HELP_MESSAGE = (
    "§r§f[§e自定义菜单 & 服主开发者工具§f] \n"
    + "  §a1. 我不想看教程？ 在聊天栏执行 §b"
    + COMMAND_OPEN_EDITOR
    + " §a以打开简易菜单编辑器！\n"
    + "  §a2. 不会命令方块编辑菜单？ 在聊天栏发送 §b"
    + MESSAGE_GEN_TURORIAL
    + " §a以生成示例命令方块！\n"
    + "  §a3. 生成的命令方块较多，所以请在空地发送以防破坏您的建筑物！"
)


class FormSystem(ServerSystem):
    """
    FormSystem 是表单系统在服务端侧实现的接口
    """

    storage_manager = None  # type: StorageManager | None
    form_storage = None  # type: FormStorage | None
    func_storage = None  # type: FunctionStorage | None
    event_storage = None  # type: EventStorage | None
    compile_cache = None  # type: CompileCache | None
    executor = None  # type: GameCodeExecutor | None
    form_feature = None  # type: FormFeature | None
    func_feature = None  # type: FunctionFeature | None
    event_feature = None  # type: EventFeature | None
    debug_feature = None  # type: DebugFeature | None
    cmd_handlers = None  # type: CommandHandlers | None

    def __init__(self, namespace, system_name):  # type: (str, str) -> None
        """初始化并返回一个新的 FormSystem

        Args:
            namespace (str):
                该表单模组的命名空间
            system_name (str):
                该表单模组在服务端侧的系统名称
        """
        ServerSystem.__init__(self, namespace, system_name)
        self._start_init()
        self._set_callback()
        self._finalise_init()

        self.listen_engine_event("ServerChatEvent", self, self.on_server_chat_event)
        self.listen_engine_event("CommandEvent", self, self.on_command_event)
        self.listen_engine_event(
            "CustomCommandTriggerServerEvent", self, self.on_custom_command_trigger
        )
        self.listen_engine_event(
            "ClientLoadAddonsFinishServerEvent", self, self.on_addon_finish_load
        )
        self.listen_engine_event(
            "PlayerIntendLeaveServerEvent", self, self.on_player_leave
        )

        self.listen_form_event(
            PACKET_NAME_MODAL_FORM_RESPONSE, self, self.on_modal_form_response
        )
        self.listen_form_event(
            PACKET_NAME_CUSTOM_FUNCTION_CALL, self, self.on_custom_function_call
        )

        game_comp = GetEngineCompFactory().CreateGame(GetLevelId())
        game_comp.AddRepeatedTimer(1, self.auto_collect_garbage)  # type: ignore

    def _start_init(self):  # type: () -> None
        """
        _start_init 开始初始化本模组在服务端上的各个类。
        _start_init 的调用者应确保此函数只会被调用一次
        """
        self.storage_manager = StorageManager()
        self.form_storage = FormStorage(self.storage_manager)
        self.func_storage = FunctionStorage(self.storage_manager)
        self.event_storage = EventStorage(self.storage_manager)

        self.compile_cache = CompileCache(self.storage_manager)
        self.executor = GameCodeExecutor(self.compile_cache, self)
        self.form_feature = FormFeature(self, self.form_storage, self.executor)
        self.func_feature = FunctionFeature(self, self.func_storage, self.executor)
        self.event_feature = EventFeature(self, self.event_storage, self.executor)
        self.debug_feature = DebugFeature(
            self.executor,
            self.form_storage,
            self.func_storage,
            self.event_storage,
            self.func_feature,
            self.compile_cache,
        )

        self.cmd_handlers = CommandHandlers(
            self.compile_cache,
            self.form_storage,
            self.func_storage,
            self.event_storage,
            self.form_feature,
            self.func_feature,
            self.event_feature,
        )

    def _set_callback(self):  # type: () -> None
        """
        _set_callback 向底层注册一个回调函数，
        以便于基于回调函数工作的实现可以调用它
        """
        assert self.executor is not None
        assert self.func_feature is not None
        self.executor.set_callback(self.func_feature.callback)

    def _finalise_init(self):  # type: () -> None
        """
        _finalise_init 终结了本模组在服务端侧的初始化，
        它预编译所有存储的用户代码，同时侦听用户注册的所有引擎事件。
        有责任确保 _finalise_init 在 _start_init 之后调用
        """
        assert self.compile_cache is not None
        assert self.form_storage is not None
        assert self.func_storage is not None
        assert self.event_storage is not None
        assert self.event_feature is not None
        _ = self.compile_cache.prepare(
            self.form_storage, self.func_storage, self.event_storage
        )
        _ = self.event_feature.prepare()

    def auto_collect_garbage(self):  # type: () -> None
        """
        auto_collect_garbage 每秒会被调用一次，
        以自动回收那些已解除固定而仍未回收的指针
        """
        assert self.executor is not None
        assert self.executor.static_builtin is not None
        assert self.executor.static_builtin.manager is not None

        with self.executor.get_locker():
            _ = self.executor.static_builtin.manager.release_internal(set())

    def on_server_chat_event(self, args):  # type: (dict[str, Any]) -> None
        """
        on_server_chat_event 在玩家发送聊天消息时被调用

        Args:
            args (dict[str, Any]):
                ServerChatEvent 传入的字典参数
        """
        player_id = args["playerId"]  # type: str
        message = args["message"]  # type: str

        engine_comp, level_id = GetEngineCompFactory(), GetLevelId()
        abilities = engine_comp.CreatePlayer(player_id).GetPlayerAbilities()
        if not abilities["op"] and GetHostPlayerId() != player_id:
            return
        if message != MESSAGE_GEN_TURORIAL:
            return

        _ = engine_comp.CreateGame(level_id).PlaceStructure(
            None,
            engine_comp.CreatePos(player_id).GetFootPos(),
            "custom_form:samples",
            engine_comp.CreateDimension(player_id).GetEntityDimensionId(),
        )
        _ = engine_comp.CreateCommand(level_id).SetCommand(
            "playsound random.toast @s ~ ~ ~ 1.00 1.00 1.00", player_id, False
        )
        engine_comp.CreateMsg(player_id).NotifyOneMessage(
            player_id, "§r§a已尝试生成自定义菜单示例"
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

    def on_custom_command_trigger(self, args):  # type: (dict[str, Any]) -> None
        """
        on_custom_command_trigger 在自定义命令被触发时调用

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        assert self.cmd_handlers is not None
        self.cmd_handlers.on_custom_command_trigger(args)

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

    def on_player_leave(self, args):  # type: (dict[str, Any]) -> None
        """on_player_leave 在有玩家离开服务器时被调用

        Args:
            args (dict[str, Any]):
                PlayerIntendLeaveServerEvent 传入的字典参数
        """
        assert self.form_feature is not None
        _ = self.form_feature.on_player_leave(args)

    def on_modal_form_response(self, args):  # type: (dict[str, Any]) -> None
        """
        on_modal_form_response 处理来自客户端的表单响应

        Args:
            args (dict[str, Any]):
                数据包 ModalFormResponse 的负载
        """
        assert self.form_feature is not None
        _ = self.form_feature.on_modal_form_response(
            args["__id__"],
            ModalFormResponse().unmarshal(args),
        )

    def on_custom_function_call(self, args):  # type: (dict[str, Any]) -> None
        """
        on_custom_function_call 处理
        来自客户端的自定义函数调用请求

        Args:
            args (dict[str, Any]):
                数据包 CustomFunctionCall 的负载
        """
        assert self.func_feature is not None
        _ = self.func_feature.on_custom_function_call(
            args["__id__"],
            CustomFunctionCall().unmarshal(args),
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

    def listen_form_event(
        self, event_name, instance, callback
    ):  # type: (str, Any, Callable[[dict[str, Any]], None]) -> None
        """listen_form_event 监听本系统，也即表单系统的事件

        Args:
            event_name (str): 要监听的事件名
            instance (Any): callback 所在类的实例
            callback (Callable[[dict[str, Any]], None]):
                在监听到事件时，调用的函数
        """
        self.ListenForEvent("FormScript", "FormClientSystem", event_name, instance, callback)  # type: ignore
