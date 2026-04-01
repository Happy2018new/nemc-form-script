# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from mod.server.component.commandCompServer import CommandCompServer
    from mod.server.component.gameCompServer import GameComponentServer
    from mod.server.component.blockInfoCompServer import BlockInfoComponentServer

import math
import json
from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId


class CommandBlockOutputHandler:
    """
    CommandBlockOutputHandler 是所有 /commandblockoutput 命令的处理设备
    """

    _cmd_comp = None  # type: CommandCompServer | None
    _game_comp = None  # type: GameComponentServer | None
    _block_comp = None  # type: BlockInfoComponentServer | None

    def __init__(self):  # type: () -> None
        """
        初始化并返回一个新的 CommandBlockOutputHandler
        """
        self._cmd_comp = GetEngineCompFactory().CreateCommand(GetLevelId())
        self._game_comp = GetEngineCompFactory().CreateGame(GetLevelId())
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
        origin = args["origin"]  # type: dict[str, Any]

        dimension = origin.get("dimension", 0)  # type: int
        entity_id = origin.get("entityId", "")  #  type: str

        try:
            args["return_msg_key"] = self.handle(cmdargs, entity_id, dimension)
        except Exception as e:
            args["return_failed"] = True
            args["return_msg_key"] = str(e)

    def handle(
        self, args, entity_id, dimension
    ):  # type: (list[dict[str, Any]], str, int) -> str
        """handle 处理 commandblockoutput 命令

        Args:
            args (list[dict[str, Any]]):
                用户通过命令行提供的参数列表
            entity_id (str):
                该命令触发时的命令执行者。
                将其置空来代表触发者是命令方块
            dimension (int):
                该命令触发时的命令执行维度

        Raises:
            Exception:
                如果出现错误，则将抛出

        Returns:
            str: 命令执行输出
        """
        # Prepare
        assert self._game_comp is not None
        assert self._block_comp is not None
        position = args[0]["value"]  # type: tuple[float, float, float]

        # Validate executor
        if len(entity_id) == 0:
            raise Exception("commands.commandblockoutput.executorisblock")

        # Get block NBT
        block_pos = (
            int(math.floor(position[0])),
            int(math.floor(position[1])),
            int(math.floor(position[2])),
        )
        block_nbt = self._block_comp.GetBlockEntityData(dimension, block_pos)
        if block_nbt is None:
            raise Exception("({}, {}, {}) 处的方块不是方块实体".format(*block_pos))
        if block_nbt["id"]["__value__"] != "CommandBlock":
            raise Exception("({}, {}, {}) 处的方块不是命令方块".format(*block_pos))

        # Get command output
        last_output = block_nbt["LastOutput"]["__value__"]  # type: str
        if len(last_output) == 0:
            return "({}, {}, {}) 处的命令方块没有输出".format(*block_pos)
        try:
            last_output = last_output.decode(encoding="utf-8", errors="ignore")  # type: ignore
            last_output = str(last_output)
        except Exception:
            pass

        # Format output
        final_output = json.dumps(last_output, ensure_ascii=False)
        final_output = final_output[1:-1]
        final_output = json.dumps(final_output, ensure_ascii=False)
        final_output = final_output[1:-1]
        final_output = final_output.replace("'", "\\\\'")

        # Generate commands
        commands = [
            "customform remove command_block_output",
            "customform add command_block_output long",
            "editlongform command_block_output title \"return '查询命令方块的输出'\"",
            "editlongform command_block_output content \"return '{}'\"".format(
                "({}, {}, {}) 处的命令方块的输出如下。".format(
                    block_pos[0], block_pos[1], block_pos[2]
                )
            ),
            "editlongform command_block_output append divider",
            "editlongform command_block_output append label",
            "editlabel command_block_output 1 label \"return '{}'\"".format(
                final_output
            ),
            "editlongform command_block_output append button",
            "editbutton command_block_output 2 text \"return '关闭'\"",
            "customform show @s ~ ~ ~ @s command_block_output",
            "customform remove command_block_output",
        ]

        # Wrap show function that can show the panel
        def _show():
            assert self._cmd_comp is not None
            for i in commands:
                _ = self._cmd_comp.SetCommand(i, entity_id, False)

        # Add timer and return
        self._game_comp.AddTimer(0.5, _show)  # type: ignore
        return "commands.commandblockoutput.success"
