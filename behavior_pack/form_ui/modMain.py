# -*- coding: utf-8 -*-
from __future__ import division

"""
NEMC Form Script

Open source in: https://github.com/Happy2018new/nemc-form-script
"""

from mod.common.mod import Mod
from mod.server.extraServerApi import (
    RegisterSystem as RegisterServerSystem,
)


@Mod.Binding(name="FormUI", version="0.0.1")  # type: ignore
class FormUI(object):
    """
    FormUI 是该表单模组的入口类
    """

    def __init__(self):
        """初始化并返回一个新的 FormUI"""
        pass

    @Mod.InitServer()  # type: ignore
    def FormUIServerInit(self):
        """
        FormUIServerInit 注册本模组在服务端侧的系统
        """
        RegisterServerSystem(
            "FormUI", "FormServerSystem", "form_ui.server.form.FormSystem"
        )

    @Mod.DestroyServer()  # type: ignore
    def FormUIServerDestroy(self):
        """
        FormUIServerDestroy 销毁本模组在服务端侧的系统
        """
        pass

    @Mod.InitClient()  # type: ignore
    def FormUIClientInit(self):
        """
        FormUIClientInit 注册本模组在客户端侧的系统
        """
        pass

    @Mod.DestroyClient()  # type: ignore
    def FormUIClientDestroy(self):
        """
        FormUIClientDestroy 销毁本模组在客户端侧的系统
        """
        pass
