# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable, Any

from ..packet.packet import PACKET_NAME_MODAL_FORM_RESPONSE
from mod.server.extraServerApi import (
    GetServerSystemCls,
    GetEngineNamespace,
    GetEngineSystemName,
)

ServerSystem = GetServerSystemCls()


class FormSystem(ServerSystem):

    def __init__(self, namespace, system_name):  # type: (str, str) -> None
        ServerSystem.__init__(self, namespace, system_name)
        self.listen_form_event(
            PACKET_NAME_MODAL_FORM_RESPONSE, self, self.on_modal_form_response
        )

        from ..packet.packet import ModalFormRequest, PACKET_NAME_MODAL_FORM_REQUEST
        from mod.server.extraServerApi import GetEngineCompFactory, GetLevelId

        from ..formal.modal import (
            ModalForm as ModalFormalForm,
            ModalFormElementLabel,
            ModalFormElementInput,
            ModalFormElementToggle,
            ModalFormElementDropdown,
            ModalFormElementSlider,
            ModalFormElementStepSlider,
        )
        from ..formal.long import (
            LongForm as LongFormalForm,
            LongFormElement,
            LongFormIconNone,
            LongFormIconPathImage,
            LongFormIconURLImage,
        )
        from ..formal.popup import PopupForm as PopupFormalForm

        def cb():
            if True:
                formal = ModalFormalForm(
                    "你好",
                    [
                        ModalFormElementLabel("标签"),
                        ModalFormElementLabel(),
                        ModalFormElementInput("输入框1", "", "提示内容"),
                        ModalFormElementInput("输入框2", "", ""),
                        ModalFormElementInput("输入框3", "Hello", ""),
                        ModalFormElementInput("输入框4", "Hello", "提示内容"),
                        ModalFormElementInput("输入框5"),
                        ModalFormElementToggle("开关1", True),
                        ModalFormElementToggle("开关2", False),
                        ModalFormElementToggle("开关3"),
                        ModalFormElementDropdown("下拉框1", ["A", "B"] * 10),
                        ModalFormElementDropdown("下拉框2", ["A"]),
                        ModalFormElementDropdown("下拉框3", ["A", "B", "你好"]),
                        ModalFormElementSlider("滑块1", 0.5, 25, 0.5, 13.5),
                        ModalFormElementSlider("滑块1", 0.5, 25, 0.5),
                        ModalFormElementStepSlider(
                            "滑块3", ["王腾", "240", "花束", "§aHappy"], 3
                        ),
                        ModalFormElementStepSlider(
                            "滑块K", ["王腾", "240", "花束", "§aHappy"] * 10, 21
                        ),
                        ModalFormElementStepSlider(
                            "滑块4", ["王腾", "240", "花束", "§aHappy"], 0
                        ),
                        ModalFormElementStepSlider(
                            "滑块5", ["王腾", "240", "花束", "§aHappy"]
                        ),
                        ModalFormElementStepSlider(
                            "滑块6", ["王腾", "240", "花束", "§aHappy"], 1
                        ),
                    ],
                )
                raw = formal.marshal()
                raw["type"] = "custom_form"
            if False:
                formal = LongFormalForm(
                    "长长长表单单子",
                    "AABBCCkkkk",
                    [
                        LongFormElement("A"),
                        LongFormElement("A", LongFormIconNone()),
                        LongFormElement(
                            "B",
                            LongFormIconPathImage("textures/ui/icon_achievement"),
                        ),
                        LongFormElement(
                            "C",
                            LongFormIconPathImage("textures/ui/anvil_icon"),
                        ),
                        LongFormElement("D"),
                    ]
                    * 10,
                )
                raw = formal.marshal()
                raw["type"] = "form"
            if False:
                formal = PopupFormalForm(
                    ":( | :)", "§bAABBCC§r" * 1000, "确定确定确定", "取消消消"
                )
                raw = formal.marshal()
                raw["type"] = "modal"

            pk = ModalFormRequest(2333, raw)
            self.BroadcastToAllClient(
                PACKET_NAME_MODAL_FORM_REQUEST,
                pk.marshal(),
            )

        game_comp = GetEngineCompFactory().CreateGame(GetLevelId())
        game_comp.AddRepeatedTimer(1, cb)  # type: ignore

    def on_modal_form_response(self, args):  # type: (dict[str, Any]) -> None
        print("on_modal_form_response", args)

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
