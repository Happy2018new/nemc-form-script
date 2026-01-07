# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Callable

import json


class GameInteract:
    """
    GameInteract 封装了一系列便捷性函数，方便与游戏进行交互。
    这其中包括解析目标选择器、获取记分板分数，或执行游戏命令等
    """

    selector = None  # type: Callable[[str], str] | None
    score = None  # type: Callable[[str, str], int] | None
    command = None  # type: Callable[[str], int] | None
    ref = None  # type: Callable[[int], int | bool | float | str] | None

    def __init__(
        self,
        selector=None,  # type: Callable[[str], str] | None
        score=None,  # type: Callable[[str, str], int] | None
        command=None,  # type: Callable[[str], int] | None
        ref=None,  # type: Callable[[int], int | bool | float | str] | None
    ):  # type: (...) -> None
        """
        初始化并返回一个新的 GameInteract。

        另外，对于 command 函数，就目前而言，由于网易接口的限制：
            - 命令执行上下文中的命令执行者必须是实体
            - 命令执行上下文中的命令执行朝向无法被传递
            - 命令执行后只能判定是否执行成功，因此该函数的返回值只可能是 0 或 1

        另外，对于 score 函数，应注意的是：
            - 如果被获取分数的对象不是玩家，或该玩家不存在，则该函数应返回 0
            - 如果被获取分数的玩家不在目标记分板上，则该函数应返回 0
            - 如果被获取分数的玩家存在多个，则该函数应返回所有这些分数的求和

        Args:
            selector (Callable[[str], str] | None, optional):
                用于解析目标选择器的实现。其返回值指示目标选择器解析所得的实体名。
                如果不提供，那么总是返回空字符串。默认值为 None
            score (Callable[[str, str], int] | None, optional):
                用于获取记分板分数的实现。其返回值指示对应记分板中相应计分项的分数。
                如果不提供，那么总是返回 0。默认值为 None
            command (Callable[[str], int] | None, optional):
                用于在给定命令执行上下文执行游戏命令的实现。其返回值指示命令的成功次数。
                如果不提供，那么总是返回 0。默认值为 None
            ref (Callable[[int], int | bool | float | str] | None, optional):
                详见本类中 ref_func 函数的注释，本处不再赘述。
                如果不提供，那么总是返回 0。默认值为 None
        """
        self.selector = selector
        self.score = score
        self.command = command
        self.ref = ref

    def _default_selector(self, target):  # type: (str) -> str
        """
        _default_selector 是 self.selector 未提供时所时的占位替代。
        它总是返回一个空字符串，而无论传入的参数如何

        Args:
            target (str):
                需要被解析为实体名的目标选择器

        Returns:
            str:
                目标选择器对应的实体名。
                在本函数中，总是返回空字符串
        """
        _ = target
        return ""

    def _default_score(self, target, scoreboard):  # type: (str, str) -> int
        """
        _default_score 是 self.score 未提供时的占位替代。
        它总是返回 0，而无论传入的参数如何

        Args:
            target (str):
                要被查询分数的玩家，
                应是一个目标选择器（或通配符）
            scoreboard (str):
                要查询的记分板名

        Returns:
            int:
                目标玩家在给定记分板的分数。
                在本函数中，总是返回 0
        """
        _, _ = target, scoreboard
        return 0

    def _default_command(self, command):  # type: (str) -> int
        """
        _default_command 是 self.command 未提供时的占位替代。
        它总是返回 0，而无论传入的参数如何

        Args:
            command (str):
                在给定上下文中所需要执行的命令

        Returns:
            int:
                命令的成功次数。
                在本函数中，总是返回 0
        """
        _ = command
        return 0

    def _default_ref(self, index):  # type: (int) -> int | bool | float | str
        """
        _default_ref 是 self.ref 未提供时的占位替代。
        它总是返回 0，而无论传入的参数如何

        Args:
            index (int):
                指示一个索引值，作用于针对用户表单响应的引用。
                在不同类型的表单中，index 的含义可能不同

        Returns:
            int | bool | float | str:
                对应索引上，用户响应的值。
                在本函数中，总是返回 0
        """
        _ = index
        return 0

    def selector_func(self):  # type: () -> Callable[[str], str]
        """
        selector_func 返回用于解析目标选择器为实体名的函数

        Returns:
            Callable[[str], str]:
                返回相应的函数。
                该函数的参数为目标选择器，
                返回值为对该选择器解析所得的实体名
        """
        if self.selector is None:
            return self._default_selector
        return self.selector

    def score_func(self):  # type: () -> Callable[[str, str], int]
        """
        score_func 返回玩家在给定记分板的分数的函数。

        另外，对于边界情况，则将进行下面的处理。
            - 如果被获取分数的对象不是玩家，或该玩家不存在，则返回 0
            - 如果被获取分数的玩家不在目标记分板上，则返回 0
            - 如果被获取分数的玩家存在多个，则返回所有这些分数的求和

        Returns:
            Callable[[str, str], int]:
                返回相应的函数。
                该函数的参数为目标选择器（或通配符）和记分板名，
                返回值为该玩家在给定记分板的分数
        """
        if self.score is None:
            return self._default_score
        return self.score

    def command_func(self):  # type: () -> Callable[[str], int]
        """
        command_func 返回用于在特定上下文执行命令的函数。

        就目前而言，由于网易接口的限制：
            - 命令执行上下文中的命令执行者必须是实体
            - 命令执行上下文中的命令执行朝向无法被传递

        Returns:
            Callable[[str], int]:
                返回相应的函数。
                该函数的参数为命令字符串，返回值为该命令的成功次数。
                就目前而言，由于网易接口只能判定命令是否成功，
                因此返回值应只可能是 0 或 1
        """
        if self.command is None:
            return self._default_command
        return self.command

    def ref_func(self):  # type: () -> Callable[[int], int | bool | float | str]
        """
        ref_func 返回用于处理引用的函数。
        在本函数中，“引用”指的是针对“用户表单响应”的引用。

        对于模态表单，用户响应是一个列表 S1。
        对于长表单，用户响应是一个索引 S2，指示用户点击了哪个按钮。
        对于信息表单，用户响应是一个布尔值 S3，指示用户点击了“确定”还是“取消”。

        ref_func 返回了一个函数。这个函数需要根据传入的索引值 T，
        返回特定于 T 的，相应的用户响应。下面列出了该函数的运作逻辑。

        对于模态表单：
            - 它将返回 S1[T] 处的值
        对于长表单：
            - 如果 T 为 -1，则应直接返回 S2
            - 否则，返回 T==S2 的运算结果
        对于信息表单：
            - 如果 T 为 -1，则应直接返回 S3
            - 否则，返回 T==int(S3) 的运算结果

        Returns:
            Callable[[int], int | bool | float | str]:
                返回相应的函数
        """
        if self.ref is None:
            return self._default_ref
        return self.ref


class BuiltInFunction:
    """
    BuiltInFunction 指示外部函数提供者。

    它对本编程语言而言是外部函数提供者，
    但对使用该语言的人则是内建函数。

    BuiltInFunction 保存了一系列外部函数，
    以供用户通过本编程语言进行调用
    """

    static = {}  # type: dict[str, Callable[..., int | bool | float | str]]
    dynamic = {}  # type: dict[str, Callable[..., int | bool | float | str]]

    def __init__(
        self,
        static={},  # type: dict[str, Callable[..., int | bool | float | str]]
        dynamic={},  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """初始化并返回一个新的 BuiltInFunction

        Args:
            static (dict[str, Callable[..., int | bool | float | str]], optional):
                要提供的静态内建函数。
                应确保字典中的内容始终不会变化。
                默认值为空字典
            dynamic (dict[str, Callable[..., int | bool | float | str]], optional):
                要提供的动态内建函数。
                任何不位于 static 中的函数，都应置于本字典中。
                默认值为空字典
        """
        self.static = static if len(static) > 0 else {}
        self.dynamic = dynamic if len(dynamic) > 0 else {}

    def _int(self, value):  # type: (Any) -> int
        """_int 将 value 转换为整数

        Args:
            value (Any): 欲被强制转换的值

        Returns:
            int: value 对应的整数表示
        """
        return int(value)

    def _bool(self, value):  # type: (Any) -> bool
        """_bool 将 value 转换为布尔值

        Args:
            value (Any): 欲被强制转换的值

        Returns:
            bool: value 对应的布尔值表示
        """
        return bool(value)

    def _float(self, value):  # type: (Any) -> float
        """_float 将 value 转换为浮点数

        Args:
            value (Any): 欲被强制转换的值

        Returns:
            float: value 对应的浮点数表示
        """
        return float(value)

    def _str(self, value):  # type: (Any) -> str
        """_str 将 value 转换为字符串

        Args:
            value (Any): 欲被强制转换的值

        Returns:
            str: value 对应的字符串表示
        """
        return str(value)

    def get_func(
        self, func_name
    ):  # type: (str) -> Callable[..., int | bool | float | str]
        """get_func 根据函数名获取对应的内建函数

        Args:
            func_name (str):
                欲获取的函数的名字

        Raises:
            Exception:
                如果目标函数不存在，则抛出错误

        Returns:
            Callable[..., int | bool | float | str]:
                func_name 对应的内建函数
        """
        if func_name == "int":
            return self._int
        if func_name == "bool":
            return self._bool
        if func_name == "float":
            return self._float
        if func_name == "str":
            return self._str

        if func_name in self.static:
            return self.static[func_name]
        if func_name in self.dynamic:
            return self.dynamic[func_name]

        raise Exception(
            "get_func: Unknown function {} is called".format(
                json.dumps(func_name, ensure_ascii=False)
            )
        )
