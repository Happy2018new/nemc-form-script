# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable
    from mod.server.extraServerApi import ServerSystem
    from mod.server.component.gameCompServer import GameComponentServer
    from mod.server.component.commandCompServer import CommandCompServer

import threading
from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId
from .cache import CompileCache
from .language.package.opcode.runner import EMPTY_VARIABLES
from .language.package.opcode.external import GameInteract, BuiltInFunction
from .language.builtins.dynamic.lib_context import Context
from .language.builtins import (
    new_base_manager,
    StaticBuiltInFunction,
    DynamicBuiltInFunction,
)
from ..storage.base import StringWithHash


class GameCodeExecutor:
    """
    GameCodeExecutor 是游戏运行时，所有代码的执行器。
    它保存了相应的命令执行上下文以及所有可能的引用对象
    """

    static_builtin = None  # type: StaticBuiltInFunction | None
    dynamic_builtin = None  # type: DynamicBuiltInFunction | None
    compile_cache = None  # type: CompileCache | None

    _game_interact = None  # type: GameInteract | None
    _built_in_func = None  # type: BuiltInFunction | None

    _game_comp = None  # type: GameComponentServer | None
    _cmd_comp = None  # type: CommandCompServer | None
    _locker = None  # type: threading.RLock | None

    def __init__(self, cache, system):  # type: (CompileCache, ServerSystem) -> None
        """初始化并返回一个新的 GameCodeExecutor

        Args:
            cache (CompileCache):
                代码编译的缓存管理器
            system (ServerSystem):
                当前模组的服务端实现
        """
        manager = new_base_manager()
        self.static_builtin = StaticBuiltInFunction(manager)
        self.dynamic_builtin = DynamicBuiltInFunction(manager, system)
        self.compile_cache = cache

        self._init_game_interact()
        self._init_builtins()

        self._game_comp = GetEngineCompFactory().CreateGame(GetLevelId())
        self._cmd_comp = GetEngineCompFactory().CreateCommand(GetLevelId())
        self._locker = threading.RLock()

    def _init_game_interact(self):  # type: () -> None
        """_init_game_interact 初始化与游戏交互的部分函数"""
        self._game_interact = GameInteract(
            selector=self._selector,
            score=self._score,
            command=self._command,
        )

    def _init_builtins(self):  # type: () -> None
        """_init_builtins 初始化大多数内置函数"""
        assert self.static_builtin is not None
        assert self.dynamic_builtin is not None
        assert self.compile_cache is not None
        self._built_in_func = BuiltInFunction()
        self.static_builtin.build_func(self._built_in_func.static)
        self.dynamic_builtin.build_func(self._built_in_func.dynamic)
        self.compile_cache.build_func(self._built_in_func.dynamic)

    def _selector(self, target):  # type: (str) -> str
        """
        _selector 解析目标选择器为实体名。
        它只能以命令执行者的位置作为参考点选取目标

        Args:
            target (str):
                要解析为实体名的目标选择器

        Raises:
            Exception:
                如果在解析目标选择器前没有设置命令执行者，
                则抛出相应的错误

        Returns:
            str: 目标选择器对应的实体名
        """
        executor = self.execute_context().get_executor()
        if len(executor) == 0:
            raise Exception("_selector: Must set executor before parse a selector")

        entities = (
            GetEngineCompFactory()
            .CreateEntityComponent(executor)
            .GetEntitiesBySelector(target)
        )
        if entities is None or len(entities) == 0:
            return ""

        result = []  # type: list[str]
        for i in entities:
            name = GetEngineCompFactory().CreateName(i).GetName()
            if name is not None:
                result.append(name)
        return ", ".join(result)

    def _score(self, target, objective):  # type: (str, str) -> int
        """
        _score 取得玩家在给定记分板的分数。
        它只能以命令执行者的位置作为参考点选取目标。

        另外，对于边界情况，则将进行下面的处理。
            - 如果被获取分数的对象不是玩家，或该玩家不存在，则返回 0
            - 如果被获取分数的玩家不在目标记分板上，则返回 0
            - 如果被获取分数的玩家存在多个，则返回所有这些分数的求和

        Args:
            target (str):
                要被查询分数的玩家，
                应是一个目标选择器（或通配符）
            scoreboard (str):
                要查询的记分板名

        Raises:
            Exception:
                如果在解析目标选择器前没有设置命令执行者，
                则抛出相应的错误

        Returns:
            int: 目标玩家在给定记分板的分数
        """
        assert self._game_comp is not None

        executor = self.execute_context().get_executor()
        if len(executor) == 0:
            raise Exception("_score: Must set executor before parse a score")
        if len(objective) == 0:
            return 0

        if target.strip() == "*":
            target = "@s"
        resp = (
            GetEngineCompFactory()
            .CreateEntityComponent(executor)
            .GetEntitiesBySelector(target)
        )
        if resp is None or len(resp) == 0:
            return 0
        entities = set(resp)

        result = 0
        for player_with_scores in self._game_comp.GetAllPlayerScoreboardObjects():
            if player_with_scores.get("playerId", "") not in entities:
                continue
            for scores in player_with_scores.get("scoreList", []):
                assert isinstance(scores, dict)
                if scores.get("name", "") == objective:
                    result += scores.get("value", 0)
        return result

    def _command(self, command):  # type: (str) -> int
        """
        _command 在给定命令执行上下文执行游戏命令。

        就目前而言，由于网易接口的限制：
            - 命令执行上下文中的命令执行者必须是实体
            - 命令执行上下文中的命令执行朝向无法被传递
            - 命令执行后只能判定是否执行成功，因此该函数的返回值只可能是 0 或 1

        Args:
            command (str):
                在给定上下文中所需要执行的命令

        Raises:
            Exception:
                如果在执行命令前没有设置命令执行者，
                则抛出相应的错误

        Returns:
            int: 命令的成功次数
        """
        assert self._cmd_comp is not None

        context = self.execute_context()
        selector = context.get_executor()
        if len(selector) == 0:
            raise Exception("_command: Must set executor before running a command")

        dim_name = context.dimension_name()
        position = context.get_position()
        final_cmd = "execute as @s at @s in {} positioned {} {} {} run {}".format(
            dim_name, *position, command
        )

        result = self._cmd_comp.SetCommand(final_cmd, selector, showOutput=False)
        if result is None or not result:
            return 0
        return 1

    def get_locker(self):  # type: () -> threading.RLock
        """
        get_locker 返回代码执行器的可重入锁。
        确保返回的锁只对不同线程之间互斥。
        有责任确保调用其他函数前都占用了该锁

        Returns:
            threading.RLock:
                代码执行器的可重入锁
        """
        assert self._locker is not None
        return self._locker

    def execute_context(self):  # type: () -> Context
        """
        execute_context 返回当前的命令执行上下文

        Returns:
            Context: 当前的命令执行上下文
        """
        assert self.dynamic_builtin is not None
        assert self.dynamic_builtin.context is not None
        return self.dynamic_builtin.context

    def run_code(
        self,
        code,  # type: StringWithHash
        ctx="",  # type: str
        executor="",  # type: str
        dimension=0,  # type: int
        position=(0.0, 0.0, 0.0),  # type: tuple[float, float, float]
        require_return=False,  # type: bool
    ):  # type: (...) -> str | int | float | bool | None
        """
        run_code 在给定的命令执行上下文中执行代码

        Args:
            code (str):
                已取得 MD5 摘要的代码
            ctx (str):
                在代码执行失败时，
                所抛出的错误中要提供的上下文信息
            executor (str, optional):
                命令执行者的 ID。
                默认值为空字符串
            dimension (int, optional):
                命令执行维度。
                默认值为 0
            position (tuple[float, float, float], optional):
                命令执行点。
                默认值为 (0.0, 0.0, 0.0)
            require_return (bool, optional):
                目标代码是否必须返回值。
                如果该参数为真并且没有返回值，则将抛出错误

        Returns:
            str | int | float | bool | None:
                代码执行的结果
        """
        assert self.static_builtin is not None
        assert self.static_builtin.manager is not None
        assert self.compile_cache is not None
        assert self._game_interact is not None
        assert self._built_in_func is not None

        # Backup current context
        frame = self.static_builtin.manager.current()
        context = self.execute_context()
        backup = context.current_context()

        # Update context
        context.set_executor(executor)
        context.set_dimension(dimension)
        context.set_position(*position)

        try:
            # Running the code
            runner = self.compile_cache.get_runner(code)
            result = runner.running(
                require_return=require_return,
                interact=self._game_interact,
                builtins=self._built_in_func,
            )
        except Exception as e:
            if len(ctx) == 0:
                raise e
            raise Exception(str(e) + "\n\n- Context -\n{}".format(ctx))
        finally:
            # Recover context
            self.static_builtin.manager.release_internal(frame)
            context.recover_context(backup)

        # Return result
        return result

    def variable_run(
        self,
        code,  # type: StringWithHash
        ctx="",  # type: str
        executor="",  # type: str
        dimension=0,  # type: int
        position=(0.0, 0.0, 0.0),  # type: tuple[float, float, float]
        variables=EMPTY_VARIABLES,  # type: dict[str, int | bool | float | str]
        require_return=False,  # type: bool
    ):  # type: (...) -> str | int | float | bool | None
        """
        variable_run 在给定的命令执行上下文中执行代码。
        它与 run_code 的区别在于它允许预先设置变量。

        从实现上，它不会在运行代码后清除 variables 中的数据，
        这意味着您可以在代码运行完成后获取所有变量的最终状态

        Args:
            code (str):
                已取得 MD5 摘要的代码
            ctx (str):
                在代码执行失败时，
                所抛出的错误中要提供的上下文信息
            executor (str, optional):
                命令执行者的 ID。
                默认值为空字符串
            dimension (int, optional):
                命令执行维度。
                默认值为 0
            position (tuple[float, float, float], optional):
                命令执行点。
                默认值为 (0.0, 0.0, 0.0)
            variables (dict[str, int | bool | float | str], optional):
                要预先设置的变量。
                默认值为 EMPTY_VARIABLES
            require_return (bool, optional):
                目标代码是否必须返回值。
                如果该参数为真并且没有返回值，则将抛出错误

        Returns:
            str | int | float | bool | None:
                代码执行的结果
        """
        # Prepare
        assert self.static_builtin is not None
        assert self.static_builtin.manager is not None
        assert self.compile_cache is not None
        assert self._game_interact is not None
        assert self._built_in_func is not None

        # Backup current context
        frame = self.static_builtin.manager.current()
        context = self.execute_context()
        backup = context.current_context()

        # Update context
        context.set_executor(executor)
        context.set_dimension(dimension)
        context.set_position(*position)

        try:
            # Running the code
            runner = self.compile_cache.get_runner(code)
            result = runner.debug(
                require_return=require_return,
                variables=variables,
                interact=self._game_interact,
                builtins=self._built_in_func,
            )
        except Exception as e:
            if len(ctx) == 0:
                raise e
            raise Exception(str(e) + "\n\n- Context -\n{}".format(ctx))
        finally:
            # Recover context
            self.static_builtin.manager.release_internal(frame)
            context.recover_context(backup)

        # Return result
        return result

    def set_ref_func(
        self, func
    ):  # type: (Callable[[int], int | bool | float | str]) -> GameCodeExecutor
        """
        set_ref_func 设置游戏交互中
        处理针对表单响应的引用的函数

        Args:
            func (Callable[[int], int | bool | float | str]):
                欲设置的函数

        Returns:
            GameCodeExecutor:
                返回 GameCodeExecutor 本身
        """
        assert self._game_interact is not None
        self._game_interact.ref = func
        return self

    def inject_func(
        self, funcs
    ):  # type: (dict[str, Callable[..., int | bool | float | str]]) -> GameCodeExecutor
        """
        inject_func 将 funcs 中的所有函数注册为动态内置函数

        Args:
            funcs (dict[str, Callable[..., int | bool | float | str]]):
                一系列待注册的动态函数。
                键是函数名，值是函数本身

        Returns:
            GameCodeExecutor:
                返回 GameCodeExecutor 本身
        """
        assert self._built_in_func is not None
        for key, value in funcs.items():
            self._built_in_func.dynamic[key] = value
        return self
