# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId
from ..static.lib_object import BaseManager


class Context:
    """
    Context 保存了命令执行上下文，
    并提供了访问和修改这些信息的函数
    """

    _manager = BaseManager()  # type: BaseManager
    _executor = ""  # type: str
    _dim_id = 0  # type: int
    _dim_name = ""  # type: str
    _position = (0.0, 0.0, 0.0)  # type: tuple[float, float, float]

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的命令执行上下文管理器

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager
        self._executor = ""
        self._dim_id = 0
        self._dim_name = "overworld"
        self._position = (0.0, 0.0, 0.0)

    def set_executor(self, executor):  # type: (str) -> bool
        """set_executor 设置命令的执行者

        Args:
            executor (str):
                命令执行者的 ID

        Raises:
            Exception:
                如果给定的参数的类型不正确，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        if not isinstance(executor, str):
            raise Exception("set_executor: The given argument must be str")
        self._executor = executor
        return True

    def get_executor(self):  # type: () -> str
        """
        get_executor 返回当前命令执行者的 ID

        Returns:
            str: 当前命令执行者的 ID
        """
        return self._executor

    def set_position(self, posx, posy, posz):  # type: (float, float, float) -> bool
        """set_position 设置命令执行点

        Args:
            posx (float): 命令执行点的 X 坐标
            posy (float): 命令执行点的 Y 坐标
            posz (float): 命令执行点的 Z 坐标

        Raises:
            Exception:
                如果给定的参数的类型不正确，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        if isinstance(posx, bool) or not isinstance(posx, (int, float)):
            raise Exception("set_position: Given posx must be tuple")
        if isinstance(posy, bool) or not isinstance(posy, (int, float)):
            raise Exception("set_position: Given posy must be tuple")
        if isinstance(posz, bool) or not isinstance(posz, (int, float)):
            raise Exception("set_position: Given posz must be tuple")

        self._position = (float(posx), float(posy), float(posz))
        return True

    def get_position(self):  # type: () -> tuple[float, float, float]
        """
        get_position 返回当前的命令执行点

        Returns:
            tuple[float, float, float]:
                当前命令执行点的坐标
        """
        return self._position

    def set_dimension(self, dim_id):  # type: (int) -> bool
        """set_dimension 设置命令执行维度

        Args:
            dim_id (int): 维度 ID

        Raises:
            Exception:
                如果给定的参数的类型不正确，
                则抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        if isinstance(dim_id, bool) or not isinstance(dim_id, int):
            raise Exception("set_dimension: Given dimension ID must be int")

        if dim_id == 0:
            self._dim_name = "overworld"
        elif dim_id == 1:
            self._dim_name = "nether"
        elif dim_id == 2:
            self._dim_name = "the_end"
        else:
            self._dim_name = "dm{}".format(dim_id)

        self._dim_id = dim_id
        return True

    def get_dimension(self):  # type: () -> int
        """
        get_dimension 返回当前的命令执行维度的 ID

        Returns:
            int: 当前命令执行维度的 ID
        """
        return self._dim_id

    def dimension_name(self):  # type: () -> str
        """
        dimension_name 返回 self.get_dimension 对应的字符串表示。
        确保返回的字符串可以用于 execute 命令的维度参数

        Returns:
            str: 当前命令执行维度的名称
        """
        return self._dim_name

    def fast_set(
        self, selector_or_entity_id, is_selector=True
    ):  # type: (str, bool) -> bool
        """
        fast_set 将命令执行上下文切换到指定的实体。
        这不仅改变了命令执行者，还改变了其他所有上下文。

        如果 is_selector 为真，则将提供的字符串视作目标选择器，
        并试图将该目标选择器对应的唯一实体作为新的命令执行上下文。

        解析目标选择器时，将尝试以原有的命令执行者作为参考点。
        如果当前环境没有指定，则以存档本身作为参考点

        Args:
            selector_or_entity_id (str):
                目标选择器或目标实体的 ID
            is_selector (bool, optional):
                提供的字符串是否指示目标选择器。
                默认值为 True

        Raises:
            Exception:
                如果给定的实体不存在，
                或匹配到的实体超过一个，
                则将抛出相应的错误

        Returns:
            bool: 总是返回 True
        """
        if not is_selector:
            entity_id = selector_or_entity_id
        else:
            if len(self._executor) == 0:
                entity_comp = GetEngineCompFactory().CreateEntityComponent(GetLevelId())
            else:
                entity_comp = GetEngineCompFactory().CreateEntityComponent(
                    self._executor
                )
            entities = entity_comp.GetEntitiesBySelector(selector_or_entity_id)
            if entities is None:
                raise Exception("fast_set: No target is matched")
            if len(entities) != 1:
                raise Exception(
                    "fast_set: Only can match one entity, but got {}".format(entities)
                )
            entity_id = entities[0]

        self.set_executor(entity_id)
        self.set_position(*GetEngineCompFactory().CreatePos(entity_id).GetFootPos())
        self.set_dimension(
            GetEngineCompFactory().CreateDimension(entity_id).GetEntityDimensionId()
        )

        return True

    def current_context(
        self,
    ):  # type: () -> tuple[str, int, tuple[float, float, float]]
        """
        current_context 返回当前的命令执行上下文。
        它用于在递归调用时保存当前的上下文信息，以便之后恢复。
        有责任确保 current_context 的调用者总是来自于内部实现（如代码执行器）

        Returns:
            tuple[str, int, tuple[float, float, float]]:
                当前的命令执行上下文
        """
        return (self._executor, self._dim_id, self._position)

    def recover_context(
        self, last
    ):  # type: (tuple[str, int, tuple[float, float, float]]) -> None
        """
        recover_context 恢复 last 所指示的命令执行上下文。
        它用于在递归的上下文调用之间恢复此前通过 current_context 获得的上下文。
        有责任确保 recover_context 的调用者总是来自于内部实现（如代码执行器）

        Args:
            last (tuple[str, int, tuple[float, float, float]]):
                欲恢复的命令执行上下文
        """
        self._executor = last[0]
        self.set_dimension(last[1])
        self._position = last[2]

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 command 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["command.set_executor"] = self.set_executor
        funcs["command.get_executor"] = self.get_executor
        funcs["command.set_position"] = self.set_position
        funcs["command.get_position"] = lambda: self._manager.ref(self.get_position())
        funcs["command.set_dimension"] = self.set_dimension
        funcs["command.get_dimension"] = self.get_dimension
        funcs["command.dimension_name"] = self.dimension_name
        funcs["command.fast_set"] = self.fast_set

        for key, value in funcs.items():
            origin[key] = value
