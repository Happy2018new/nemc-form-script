# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from mod.server.component.blockInfoCompServer import BlockInfoComponentServer

from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId


class CommandBlockOutputHandler:
    """
    CommandBlockOutputHandler 是所有 /commandblockoutput 命令的处理设备
    """

    _block_comp = None  # type: BlockInfoComponentServer | None

    def __init__(self):  # type: () -> None
        """
        初始化并返回一个新的 CommandBlockOutputHandler
        """
        self._block_comp = GetEngineCompFactory().CreateBlockInfo(GetLevelId())

    def on_custom_command_trigger(self, args):  # type: (dict[str, Any]) -> None
        """
        on_custom_command_trigger 在自定义命令被触发时调用。
        有必要确保它的上层调用者验证了调用的命令是 /commandblockoutput

        Args:
            args (dict[str, Any]):
                CustomCommandTriggerServerEvent 传入的字典参数
        """
        cmdargs = args["args"]  # type: list[dict[str, Any]]
        dimension = args["origin"]["dimension"]  # type: int

        try:
            args["return_msg_key"] = self.handle(cmdargs, dimension)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

    def handle(self, args, dimension):  # type: (list[dict[str, Any]], int) -> str
        """handle 处理 commandblockoutput 命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        assert self._block_comp is not None
        position = args[0]["value"]  # type: tuple[float, float, float]

        block_pos = (int(position[0]), int(position[1]), int(position[2]))
        block_nbt = self._block_comp.GetBlockEntityData(dimension, block_pos)
        if block_nbt is None:
            raise Exception("({}, {}, {}) 处的方块不是方块实体".format(*block_pos))
        if block_nbt["id"]["__value__"] != "CommandBlock":
            raise Exception("({}, {}, {}) 处的方块不是命令方块".format(*block_pos))

        last_output = block_nbt["LastOutput"]["__value__"]  # type: str
        if len(last_output) == 0:
            return "({}, {}, {}) 处的命令方块没有输出".format(*block_pos)
        last_output = "\n".join(["  " + i for i in last_output.split("\n")])
        return "({}, {}, {}) 处的命令方块的输出为: \n{}".format(*block_pos, last_output)
