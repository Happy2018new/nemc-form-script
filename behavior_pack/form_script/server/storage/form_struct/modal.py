# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from .base import BaseForm
from ..base import StringWithHash
from ....formal.base import Marshaler

EMPTY_STRING_WITH_HASH = StringWithHash()


class ModalFormElement(Marshaler):
    """ModalFormElement 是模态表单中各种元素类别的总称"""


class ModalFormElementLabel(ModalFormElement):
    """
    ModalFormElementLabel 指示模态表单中的普通文本元素
    """

    text = EMPTY_STRING_WITH_HASH

    def __init__(self, text=EMPTY_STRING_WITH_HASH):  # type: (StringWithHash) -> None
        """
        初始化并返回一个可放置在模态表单中的普通文本

        Args:
            text (StringWithHash, optional):
                普通文本的内容。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.text = text

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {"text": self.text.marshal()}

    def unmarshal(self, data):  # type: (Any) -> ModalFormElementLabel
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            ModalFormElementLabel: 返回 ModalFormElementLabel 本身
        """
        self.text = StringWithHash().unmarshal(data["text"])
        return self


class ModalFormElementHeader(ModalFormElement):
    """
    ModalFormElementHeader 指示模态表单中的大字文本元素
    """

    text = EMPTY_STRING_WITH_HASH

    def __init__(self, text=EMPTY_STRING_WITH_HASH):  # type: (StringWithHash) -> None
        """
        初始化并返回一个可放置在模态表单中的大字文本

        Args:
            text (StringWithHash, optional):
                大字文本的内容。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.text = text

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {"text": self.text.marshal()}

    def unmarshal(self, data):  # type: (Any) -> ModalFormElementHeader
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            ModalFormElementHeader: 返回 ModalFormElementHeader 本身
        """
        self.text = StringWithHash().unmarshal(data["text"])
        return self


class ModalFormElementDivider(ModalFormElement):
    """
    ModalFormElementDivider 指示模态表单中的分割线元素
    """

    def __init__(self):  # type: () -> None
        """
        初始化并返回一个可放置在模态表单中的分割线
        """
        pass

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {}

    def unmarshal(self, data):  # type: (Any) -> ModalFormElementDivider
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            ModalFormElementDivider: 返回 ModalFormElementDivider 本身
        """
        _ = data
        return self


class ModalFormElementInput(ModalFormElement):
    """
    ModalFormElementInput 指示模态表单中的输入框
    """

    text = EMPTY_STRING_WITH_HASH
    default = EMPTY_STRING_WITH_HASH
    place_holder = EMPTY_STRING_WITH_HASH
    tooltip = EMPTY_STRING_WITH_HASH

    def __init__(
        self,
        text=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        default=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        place_holder=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        tooltip=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
    ):  # type: (...) -> None
        """
        初始化并返回一个可放置在模态表单中的输入框

        Args:
            text (StringWithHash, optional):
                输入框的标题文本。
                默认值为 EMPTY_STRING_WITH_HASH
            default (StringWithHash, optional):
                输入框已输入的内容。
                默认值为 EMPTY_STRING_WITH_HASH
            place_holder (StringWithHash, optional):
                输入框的提示文本。
                默认值为 EMPTY_STRING_WITH_HASH
            tooltip (StringWithHash, optional):
                输入框的灯泡提示文本。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.text = text
        self.default = default
        self.place_holder = place_holder
        self.tooltip = tooltip

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text.marshal(),
            "default": self.default.marshal(),
            "placeholder": self.place_holder.marshal(),
            "tooltip": self.tooltip.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> ModalFormElementInput
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            ModalFormElementInput: 返回 ModalFormElementInput 本身
        """
        assert isinstance(data, dict)

        self.text = StringWithHash().unmarshal(data["text"])
        self.default = StringWithHash().unmarshal(data["default"])
        self.place_holder = StringWithHash().unmarshal(data["placeholder"])
        self.tooltip = (
            StringWithHash().unmarshal(data["tooltip"])
            if "tooltip" in data
            else StringWithHash("return ''")
        )

        return self


class ModalFormElementToggle(ModalFormElement):
    """
    ModalFormElementToggle 指示模态表单中的开关
    """

    text = EMPTY_STRING_WITH_HASH
    default = EMPTY_STRING_WITH_HASH
    tooltip = EMPTY_STRING_WITH_HASH

    def __init__(
        self,
        text=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        default=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        tooltip=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
    ):  # type: (...) -> None
        """
        初始化并返回一个可放置在模态表单中的开关

        Args:
            text (StringWithHash, optional):
                开关的标题文本。
                默认值为 EMPTY_STRING_WITH_HASH
            default (StringWithHash, optional):
                开关的默认状态。
                默认值为 EMPTY_STRING_WITH_HASH
            tooltip (StringWithHash, optional):
                开关的灯泡提示文本。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.text = text
        self.default = default
        self.tooltip = tooltip

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text.marshal(),
            "default": self.default.marshal(),
            "tooltip": self.tooltip.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> ModalFormElementToggle
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            ModalFormElementToggle: 返回 ModalFormElementToggle 本身
        """
        assert isinstance(data, dict)

        self.text = StringWithHash().unmarshal(data["text"])
        self.default = StringWithHash().unmarshal(data["default"])
        self.tooltip = (
            StringWithHash().unmarshal(data["tooltip"])
            if "tooltip" in data
            else StringWithHash("return ''")
        )

        return self


class ModalFormElementDropdown(ModalFormElement):
    """
    ModalFormElementDropdown 指示模态表单中的下拉框
    """

    text = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    options = []  # type: list[StringWithHash]
    default = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    tooltip = EMPTY_STRING_WITH_HASH  # type: StringWithHash

    def __init__(
        self,
        text=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        options=[],  # type: list[StringWithHash]
        default=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        tooltip=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
    ):  # type: (...) -> None
        """
        初始化并返回一个可放置在模态表单中的下拉框

        Args:
            text (StringWithHash, optional):
                下拉框的标题文本。
                默认值为 EMPTY_STRING_WITH_HASH
            options (list[StringWithHash], optional):
                下拉框的选项列表。
                默认值为空列表
            default (StringWithHash, optional):
                下拉框在初始状态下，
                所选中选项的索引。
                默认值为 EMPTY_STRING_WITH_HASH
            tooltip (StringWithHash, optional):
                下拉框的灯泡提示文本。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.text = text
        self.options = options if len(options) > 0 else []
        self.default = default
        self.tooltip = tooltip

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text.marshal(),
            "options": [i.marshal() for i in self.options],
            "default": self.default.marshal(),
            "tooltip": self.tooltip.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> ModalFormElementDropdown
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            ModalFormElementDropdown: 返回 ModalFormElementDropdown 本身
        """
        assert isinstance(data, dict)

        self.text = StringWithHash().unmarshal(data["text"])
        self.options = [StringWithHash().unmarshal(i) for i in data["options"]]
        self.default = StringWithHash().unmarshal(data["default"])
        self.tooltip = (
            StringWithHash().unmarshal(data["tooltip"])
            if "tooltip" in data
            else StringWithHash("return ''")
        )

        return self


class ModalFormElementSlider(ModalFormElement):
    """
    ModalFormElementSlider 指示模态表单中的隐式步进滑块
    """

    text = EMPTY_STRING_WITH_HASH
    min_val = EMPTY_STRING_WITH_HASH
    max_val = EMPTY_STRING_WITH_HASH
    step = EMPTY_STRING_WITH_HASH
    default = EMPTY_STRING_WITH_HASH
    tooltip = EMPTY_STRING_WITH_HASH

    def __init__(
        self,
        text=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        min_val=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        max_val=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        step=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        default=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        tooltip=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
    ):  # type: (...) -> None
        """
        初始化并返回一个可放置在模态表单中的隐式步进滑块

        Args:
            text (StringWithHash, optional):
                滑块的标题文本。
                默认值为 EMPTY_STRING_WITH_HASH
            min_val (StringWithHash, optional):
                滑块允许的最小值。
                默认值为 EMPTY_STRING_WITH_HASH
            max_val (StringWithHash, optional):
                滑块允许的最大值。
                默认值为 EMPTY_STRING_WITH_HASH
            step (StringWithHash, optional):
                滑块的步进值。
                默认值为 EMPTY_STRING_WITH_HASH
            default (StringWithHash, optional):
                滑块的初始值。
                默认值为 EMPTY_STRING_WITH_HASH
            tooltip (StringWithHash, optional):
                滑块的灯泡提示文本。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.text = text
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.default = default
        self.tooltip = tooltip

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text.marshal(),
            "min": self.min_val.marshal(),
            "max": self.max_val.marshal(),
            "step": self.step.marshal(),
            "default": self.default.marshal(),
            "tooltip": self.tooltip.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> ModalFormElementSlider
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            ModalFormElementSlider: 返回 ModalFormElementSlider 本身
        """
        assert isinstance(data, dict)

        self.text = StringWithHash().unmarshal(data["text"])
        self.min_val = StringWithHash().unmarshal(data["min"])
        self.max_val = StringWithHash().unmarshal(data["max"])
        self.step = StringWithHash().unmarshal(data["step"])
        self.default = StringWithHash().unmarshal(data["default"])
        self.tooltip = (
            StringWithHash().unmarshal(data["tooltip"])
            if "tooltip" in data
            else StringWithHash("return ''")
        )

        return self


class ModalFormElementStepSlider(ModalFormElement):
    """
    ModalFormElementStepSlider 指示模态表单中的显式步进滑块
    """

    text = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    steps = []  # type: list[StringWithHash]
    default = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    tooltip = EMPTY_STRING_WITH_HASH  # type: StringWithHash

    def __init__(
        self,
        text=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        steps=[],  # type: list[StringWithHash]
        default=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        tooltip=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
    ):  # type: (...) -> None
        """
        初始化并返回一个可放置在模态表单中的显式步进滑块

        Args:
            text (StringWithHash, optional):
                滑块的标题文本。
                默认值为 StringWithHash
            steps (list[StringWithHash], optional):
                滑块的内容列表。
                默认值为空列表
            default (StringWithHash, optional):
                滑块在初始状态下，
                所显示内容的索引。
                默认值为 StringWithHash
            tooltip (StringWithHash, optional):
                滑块的灯泡提示文本。
                默认值为 StringWithHash
        """
        self.text = text
        self.steps = steps if len(steps) > 0 else []
        self.default = default
        self.tooltip = tooltip

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text.marshal(),
            "steps": [i.marshal() for i in self.steps],
            "default": self.default.marshal(),
            "tooltip": self.tooltip.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> ModalFormElementStepSlider
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            ModalFormElementStepSlider: 返回 ModalFormElementStepSlider 本身
        """
        assert isinstance(data, dict)

        self.text = StringWithHash().unmarshal(data["text"])
        self.steps = [StringWithHash().unmarshal(i) for i in data["steps"]]
        self.default = StringWithHash().unmarshal(data["default"])
        self.tooltip = (
            StringWithHash().unmarshal(data["tooltip"])
            if "tooltip" in data
            else StringWithHash("return ''")
        )

        return self


class ModalForm(BaseForm):
    """ModalForm 是数据保存实现中的模态表单"""

    title = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    content = []  # type: list[ModalFormElement]

    onsubmit = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    oncancel = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    onsuberr = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    oncanerr = EMPTY_STRING_WITH_HASH  # type: StringWithHash

    def __init__(
        self,
        title=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        content=[],  # type: list[ModalFormElement]
        onsubmit=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        oncancel=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        onsuberr=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        oncanerr=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
    ):  # type: (...) -> None
        """初始化并返回一个新的 ModalForm

        Args:
            title (StringWithHash, optional):
                模态表单的标题文本。
                默认值为 EMPTY_STRING_WITH_HASH
            content (list[ModalFormElement], optional):
                模态表单的内容。
                默认值为空列表
            onsubmit (StringWithHash, optional):
                当表单被用户提交时调用的代码。
                默认值为 EMPTY_STRING_WITH_HASH
            oncancel (StringWithHash, optional):
                当表单被关闭时应调用的代码。
                默认值为 EMPTY_STRING_WITH_HASH
            onsuberr (StringWithHash, optional):
                当执行 onsubmit 所指示的代码出错时，
                应执行的错误处理。
                默认值为 EMPTY_STRING_WITH_HASH
            oncanerr (StringWithHash, optional):
                当执行 oncancel 所指示的代码出错时，
                应执行的错误处理。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.title = title
        self.content = content if len(content) > 0 else []
        self.onsubmit = onsubmit
        self.oncancel = oncancel
        self.onsuberr = onsuberr
        self.oncanerr = oncanerr

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将该 ModalForm 编码为对应的 JSON 表示

        Returns:
            dict[str, Any]: 该模态表单对应的 JSON 表示
        """
        content = []  # type: list[dict[str, Any]]

        for i in self.content:
            value = i.marshal()
            if isinstance(i, ModalFormElementLabel):
                value["type"] = "label"
            elif isinstance(i, ModalFormElementHeader):
                value["type"] = "header"
            elif isinstance(i, ModalFormElementDivider):
                value["type"] = "divider"
            elif isinstance(i, ModalFormElementInput):
                value["type"] = "input"
            elif isinstance(i, ModalFormElementToggle):
                value["type"] = "toggle"
            elif isinstance(i, ModalFormElementDropdown):
                value["type"] = "dropdown"
            elif isinstance(i, ModalFormElementSlider):
                value["type"] = "slider"
            elif isinstance(i, ModalFormElementStepSlider):
                value["type"] = "step_slider"
            content.append(value)

        return {
            "title": self.title.marshal(),
            "content": content,
            "onsubmit": self.onsubmit.marshal(),
            "oncancel": self.oncancel.marshal(),
            "onsuberr": self.onsuberr.marshal(),
            "oncanerr": self.oncanerr.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> ModalForm
        """
        unmarshal 从 JSON 中解码数据，
        并将解码所得的数据置入本实例中

        Args:
            data (Any): 给定的 data 数据。
                        应确保它是一个字典

        Returns:
            ModalForm: 返回 ModalForm 本身
        """
        self.title = StringWithHash().unmarshal(data["title"])
        self.onsubmit = StringWithHash().unmarshal(data["onsubmit"])
        self.oncancel = StringWithHash().unmarshal(data["oncancel"])
        self.onsuberr = StringWithHash().unmarshal(data["onsuberr"])
        self.oncanerr = StringWithHash().unmarshal(data["oncanerr"])

        self.content = []
        for i in data["content"]:
            element_type = i["type"]
            if element_type == "label":
                self.content.append(ModalFormElementLabel().unmarshal(i))
            elif element_type == "header":
                self.content.append(ModalFormElementHeader().unmarshal(i))
            elif element_type == "divider":
                self.content.append(ModalFormElementDivider().unmarshal(i))
            elif element_type == "input":
                self.content.append(ModalFormElementInput().unmarshal(i))
            elif element_type == "toggle":
                self.content.append(ModalFormElementToggle().unmarshal(i))
            elif element_type == "dropdown":
                self.content.append(ModalFormElementDropdown().unmarshal(i))
            elif element_type == "slider":
                self.content.append(ModalFormElementSlider().unmarshal(i))
            elif element_type == "step_slider":
                self.content.append(ModalFormElementStepSlider().unmarshal(i))

        return self

    def all_codes(self):  # type: () -> list[StringWithHash]
        """
        all_codes 返回该 ModalForm 中存在的所有代码

        Returns:
            list[StringWithHash]:
                该 ModalForm 中存在的所有代码
        """
        codes = [
            self.title,
            self.onsubmit,
            self.oncancel,
            self.onsuberr,
            self.oncanerr,
        ]  # type: list[StringWithHash]

        for i in self.content:
            if isinstance(i, ModalFormElementLabel):
                codes.append(i.text)
            elif isinstance(i, ModalFormElementHeader):
                codes.append(i.text)
            elif isinstance(i, ModalFormElementDivider):
                pass
            elif isinstance(i, ModalFormElementInput):
                codes.append(i.text)
                codes.append(i.default)
                codes.append(i.place_holder)
                codes.append(i.tooltip)
            elif isinstance(i, ModalFormElementToggle):
                codes.append(i.text)
                codes.append(i.default)
                codes.append(i.tooltip)
            elif isinstance(i, ModalFormElementDropdown):
                codes.append(i.text)
                codes.append(i.default)
                codes.append(i.tooltip)
                for option in i.options:
                    codes.append(option)
            elif isinstance(i, ModalFormElementSlider):
                codes.append(i.text)
                codes.append(i.min_val)
                codes.append(i.max_val)
                codes.append(i.step)
                codes.append(i.default)
                codes.append(i.tooltip)
            elif isinstance(i, ModalFormElementStepSlider):
                codes.append(i.text)
                codes.append(i.default)
                codes.append(i.tooltip)
                for step in i.steps:
                    codes.append(step)

        return codes
