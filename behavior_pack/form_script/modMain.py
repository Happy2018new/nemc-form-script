# -*- coding: utf-8 -*-
from __future__ import division

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
    """
    FormScript 是该表单模组的入口类
    """

    def __init__(self):
        """初始化并返回一个新的 FormScript"""
        pass

    @Mod.InitServer()  # type: ignore
    def FormScriptServerInit(self):
        """
        FormScriptServerInit 注册本模组在服务端侧的系统
        """
        RegisterServerSystem(
            "FormScript", "FormServerSystem", "form_script.server.form.FormSystem"
        )

    @Mod.DestroyServer()  # type: ignore
    def FormScriptServerDestroy(self):
        """
        FormScriptServerDestroy 销毁本模组在服务端侧的系统
        """
        pass

    @Mod.InitClient()  # type: ignore
    def FormScriptClientInit(self):
        """
        FormScriptClientInit 注册本模组在客户端侧的系统
        """
        RegisterClientSystem(
            "FormScript", "FormClientSystem", "form_script.client.form.FormSystem"
        )

    @Mod.DestroyClient()  # type: ignore
    def FormScriptClientDestroy(self):
        """
        FormScriptClientDestroy 销毁本模组在客户端侧的系统
        """
        base_system = GetClientSystem("FormScript", "FormClientSystem")  # type: Any
        form_system = base_system  # type: FormSystem
        form_system.on_shutdown()
