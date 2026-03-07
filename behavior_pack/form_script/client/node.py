# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from .form import FormSystem

from mod.client.extraClientApi import GetScreenNodeCls, GetSystem

ScreenNode = GetScreenNodeCls()


class FormScreenNode(ScreenNode):
    def __init__(
        self, namespace, name, param
    ):  # type: (str, str, dict[str, Any]) -> None
        ScreenNode.__init__(self, namespace, name, param)  # type: ignore

    def Update(self):
        base_system = GetSystem("FormScript", "FormClientSystem")  # type: Any
        form_system = base_system  # type: FormSystem
        form_system.on_update_screen(False)
