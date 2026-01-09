# -*- coding: utf-8 -*-

"""
NEMC Form Script

Open source in: https://github.com/Happy2018new/nemc-form-script
"""

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from .client.form import FormSystem

from mod.common.mod import Mod
from mod.client.extraClientApi import (
    RegisterSystem as RegisterClientSystem,
    GetSystem as GetClientSystem,
)
from mod.server.extraServerApi import (
    RegisterSystem as RegisterServerSystem,
)


@Mod.Binding(name="FormScript", version="0.0.1")  # type: ignore
class FormScript(object):

    def __init__(self):
        pass

    @Mod.InitServer()  # type: ignore
    def FormScriptServerInit(self):
        RegisterServerSystem(
            "FormScript", "FormServerSystem", "script.server.main.FormSystem"
        )

    @Mod.DestroyServer()  # type: ignore
    def FormScriptServerDestroy(self):
        pass

    @Mod.InitClient()  # type: ignore
    def FormScriptClientInit(self):
        RegisterClientSystem(
            "FormScript", "FormClientSystem", "script.client.form.FormSystem"
        )

    @Mod.DestroyClient()  # type: ignore
    def FormScriptClientDestroy(self):
        base_system = GetClientSystem("FormScript", "FormClientSystem")  # type: Any
        form_system = base_system  # type: FormSystem
        form_system.on_shutdown()
