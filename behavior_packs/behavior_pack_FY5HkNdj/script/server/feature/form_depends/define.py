# -*- coding: utf-8 -*-

import json
from ...storage.base import StringWithHash
from ....packet.packet import ModalFormResponse
from ....formal.base import BaseForm as BaseFormalForm
from ....formal.long import LongForm as LongFormalForm
from ....formal.popup import PopupForm as PopupFormalForm
from ....formal.modal import (
    ModalForm as ModalFormalForm,
    ModalFormElementLabel as ModalFormalFormElementLabel,
    ModalFormElementInput as ModalFormalFormElementInput,
    ModalFormElementToggle as ModalFormalFormElementToggle,
    ModalFormElementDropdown as ModalFormalFormElementDropdown,
    ModalFormElementSlider as ModalFormalFormElementSlider,
    ModalFormElementStepSlider as ModalFormalFormElementStepSlider,
)


EMPTY_BASE_FORMAL_FORM = BaseFormalForm()
EMPTY_STRING_WITH_HASH = StringWithHash()


class FormalWithCallback:
    """
    FormalWithCallback 指示一个已经发送的表单。
    它保存了稳定的形式化表单和对应的回调函数表示
    """

    formal = EMPTY_BASE_FORMAL_FORM
    onsubmit = EMPTY_STRING_WITH_HASH
    oncancel = EMPTY_STRING_WITH_HASH
    onsuberr = EMPTY_STRING_WITH_HASH
    oncanerr = EMPTY_STRING_WITH_HASH

    def __init__(
        self,
        formal,  # type: BaseFormalForm
        onsubmit,  # type: StringWithHash
        oncancel,  # type: StringWithHash
        onsuberr,  # type: StringWithHash
        oncanerr,  # type: StringWithHash
    ):  # type: (...) -> None
        """
        初始化并返回一个新的 FormalWithCallback

        Args:
            formal (BaseFormalForm):
                表单的形式化表示。
                应是不可变的最终状态
            onsubmit (StringWithHash):
                当表单被用户提交时调用的代码
            oncancel (StringWithHash):
                当用户正忙或取消表单时调用的代码
            onsuberr (StringWithHash):
                当执行 onsubmit 所指示的代码出错时，
                应执行的错误处理
            oncanerr (StringWithHash):
                当执行 oncancel 所指示的代码出错时，
                应执行的错误处理
        """
        self.formal = formal
        self.onsubmit = onsubmit
        self.oncancel = oncancel
        self.onsuberr = onsuberr
        self.oncanerr = oncanerr

    def validate(
        self, pk
    ):  # type: (ModalFormResponse) -> int | bool | list[int | bool | float | str | None] | None
        """
        validate 验证玩家提及的表单（玩家对表单的响应）是否合法。
        如果合法，则同时返回解析后的响应数据

        Args:
            pk (ModalFormResponse):
                玩家对表单的响应

        Returns:
            int | bool | list[int | bool | float | str | None] | None:
                如果响应的表单合法，则返回解析后的响应数据；
                否则响应的表单不合法，那么返回 None
        """
        raw = pk.response_data.value()
        if raw is None:
            return None
        try:
            resp = json.loads(raw)
        except Exception:
            return None

        if isinstance(self.formal, LongFormalForm):
            if isinstance(resp, bool) or not isinstance(resp, int):
                return None
            return resp
        if isinstance(self.formal, PopupFormalForm):
            if not isinstance(resp, bool):
                return None
            return resp
        if isinstance(self.formal, ModalFormalForm):
            if not isinstance(resp, list):
                return None
            if len(self.formal.content) != len(resp):
                return None
            for index, value in enumerate(self.formal.content):
                if isinstance(value, ModalFormalFormElementLabel):
                    if resp[index] is not None:
                        return None
                elif isinstance(value, ModalFormalFormElementInput):
                    if not isinstance(resp[index], str):
                        return None
                elif isinstance(value, ModalFormalFormElementToggle):
                    if not isinstance(resp[index], bool):
                        return None
                elif isinstance(value, ModalFormalFormElementDropdown):
                    val = resp[index]
                    if isinstance(val, bool) or not isinstance(val, int):
                        return None
                    if val < 0 or val >= len(value.options):
                        return None
                elif isinstance(value, ModalFormalFormElementSlider):
                    val = resp[index]
                    if isinstance(val, bool) or not isinstance(val, (int, float)):
                        return None
                    if val < value.min_val or val > value.max_val:
                        return None
                    resp[index] = float(val)
                elif isinstance(value, ModalFormalFormElementStepSlider):
                    val = resp[index]
                    if isinstance(val, bool) or not isinstance(val, int):
                        return None
                    if val < 0 or val >= len(value.steps):
                        return None
            return resp

        return None


class FormRefProcesser:
    """
    FormRefProcesser 处理代码中对用户表单响应的引用
    """

    response = None  # type: int | bool | list[int | bool | float | str | None] | None

    def __init__(self):  # type: () -> None
        """初始化并返回一个新的 FormRefProcesser"""
        self.response = None

    def ref(self, index):  # type: (int) -> int | bool | float | str
        """
        ref 处理代码中对用户表单响应的引用。

        - 对于模态表单，用户响应是一个列表 S1
        - 对于长表单，用户响应是一个索引 S2，指示用户点击了哪个按钮
        - 对于信息表单，用户响应是一个布尔值 S3，指示用户点击了“确定”还是“取消”
        - 作为一种特殊情况，代码可能被用作处理表单被关闭的情况
          在这种情况下，认为用户关闭的表单的原因是一个整数 S4

        index 是一个索引值 T，而 ref 将返回特定于 T 的，相应的用户响应。
        下面列出了 ref 具体的运作逻辑。

        对于模态表单：
            - 它将返回 S1[T] 处的值
        对于长表单：
            - 如果 T 为 -1，则应直接返回 S2
            - 否则，返回 T==S2 的运算结果
        对于信息表单：
            - 如果 T 为 -1，则应直接返回 S3
            - 否则，返回 T==int(S3) 的运算结果
        对于关闭表单：
            - 如果 T 为 -1，则应直接返回 S4
            - 否则，返回 T==S4 的运算结果
        另外，请确保：
            - 表单被玩家手动叉掉时 S4 为 0
            - 表单因玩家正忙而无法打开时 S4 为 1

        Raises:
            Exception:
                如果 Ref 语句在非表单响应的上下文下被使用，
                或给定的索引值超出可达范围，
                或引用了 None 值时，将抛出相应的错误

        Returns:
            int | bool | float | str:
                特定于给定索引值的用户响应
        """
        if self.response is None:
            raise Exception(
                "ref: Ref statement can only used under form response environment"
            )

        if isinstance(self.response, (int, bool)):
            if index == -1:
                return self.response
            return index == int(self.response)

        if index < 0 or index >= len(self.response):
            raise Exception(
                "ref: Ref index out of range [{}] with length {}".format(
                    index, len(self.response)
                )
            )
        value = self.response[index]
        if value is None:
            raise Exception(
                "ref: Can not reference a null value (index={})".format(index)
            )

        return value
