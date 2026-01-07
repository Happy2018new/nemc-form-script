# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

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
    _pos = (0.0, 0.0, 0.0)  # type: tuple[float, float, float]

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
        self._pos = (0.0, 0.0, 0.0)

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
            raise Exception("set_executor: The given argument must be a str")
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
        if not isinstance(posx, (int, float)):
            raise Exception("set_position: Given posx must be a tuple")
        if not isinstance(posy, (int, float)):
            raise Exception("set_position: Given posy must be a tuple")
        if not isinstance(posz, (int, float)):
            raise Exception("set_position: Given posz must be a tuple")

        self._pos = (float(posx), float(posy), float(posz))
        return True

    def get_position(self):  # type: () -> tuple[float, float, float]
        """
        get_position 返回当前的命令执行点

        Returns:
            tuple[float, float, float]:
                当前命令执行点的坐标
        """
        return self._pos

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
        if not isinstance(dim_id, int):
            raise Exception("set_dimension: Given dimension ID must be an int")

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

        for key, value in funcs.items():
            origin[key] = value
