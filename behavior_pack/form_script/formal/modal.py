# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from .base import Marshaler, BaseForm


class ModalFormElement(Marshaler):
    """ModalFormElement 是模态表单中各种元素类别的总称"""


class ModalFormElementLabel(ModalFormElement):
    """
    ModalFormElementLabel 指示模态表单中的普通文本元素
    """

    text = ""

    def __init__(self, text=""):  # type: (str) -> None
        """
        初始化并返回一个可放置在模态表单中的普通文本

        Args:
            text (str, optional):
                普通文本的内容。
                默认值为空字符串
        """
        self.text = text

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {"text": self.text}

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
        self.text = ""
        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        if isinstance(text, str):
            self.text = text
        return self


class ModalFormElementInput(ModalFormElement):
    """
    ModalFormElementLabel 指示模态表单中的输入框
    """

    text = ""
    default = ""
    place_holder = ""

    def __init__(
        self, text="", default="", place_holder=""
    ):  # type: (str, str, str) -> None
        """
        初始化并返回一个可放置在模态表单中的输入框

        Args:
            text (str, optional):
                输入框的标题文本。
                默认值为空字符串
            default (str, optional):
                输入框已输入的内容。
                默认值为空字符串
            place_holder (str, optional):
                输入框的提示文本。
                默认值为空字符串
        """
        self.text = text
        self.default = default
        self.place_holder = place_holder

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text,
            "default": self.default,
            "placeholder": self.place_holder,
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
        self.text = ""
        self.default = ""
        self.place_holder = ""
        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        default = data.get("default", "")
        place_holder = data.get("placeholder", "")

        if isinstance(text, str):
            self.text = text
        if isinstance(default, str):
            self.default = default
        if isinstance(place_holder, str):
            self.place_holder = place_holder
        return self


class ModalFormElementToggle(ModalFormElement):
    """
    ModalFormElementToggle 指示模态表单中的开关
    """

    text = ""
    default = False

    def __init__(self, text="", default=False):  # type: (str, bool) -> None
        """
        初始化并返回一个可放置在模态表单中的开关

        Args:
            text (str, optional):
                开关的标题文本。
                默认值为空字符串
            default (bool, optional):
                开关的默认状态。
                默认值为 False
        """
        self.text = text
        self.default = default

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text,
            "default": self.default,
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
        self.text = ""
        self.default = False
        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        default = data.get("default", False)

        if isinstance(text, str):
            self.text = text
        if isinstance(default, bool):
            self.default = default
        return self


class ModalFormElementDropdown(ModalFormElement):
    """
    ModalFormElementDropdown 指示模态表单中的下拉框
    """

    text = ""  # type: str
    options = []  # type: list[str]
    default = 0  # type: int

    def __init__(
        self, text="", options=[], default=0
    ):  # type: (str, list[str], int) -> None
        """
        初始化并返回一个可放置在模态表单中的下拉框

        Args:
            text (str, optional):
                下拉框的标题文本。
                默认值为空字符串
            options (list[str], optional):
                下拉框的选项列表。
                默认值为空列表
            default (int, optional):
                下拉框在初始状态下，
                所选中选项的索引。
                默认值为 0
        """
        self.text = text
        self.options = options if len(options) > 0 else []
        self.default = int(default)

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text,
            "options": self.options,
            "default": int(self.default),
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
        self.text = ""
        self.options = []
        self.default = 0
        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        options = data.get("options", [])
        default = data.get("default", 0)

        if isinstance(text, str):
            self.text = text
        if isinstance(options, list):
            self.options = [i for i in options if isinstance(i, str)]
        if not isinstance(default, bool) and isinstance(default, (int, bool)):
            self.default = int(default)
        return self


class ModalFormElementSlider(ModalFormElement):
    """
    ModalFormElementSlider 指示模态表单中的隐式步进滑块
    """

    text = ""
    min_val = 0.0
    max_val = 1.0
    step = 1.0
    default = 0.0

    def __init__(
        self, text="", min_val=0.0, max_val=1.0, step=1.0, default=0.0
    ):  # type: (str, float, float, float, float) -> None
        """
        初始化并返回一个可放置在模态表单中的隐式步进滑块

        Args:
            text (str, optional):
                滑块的标题文本。
                默认值为空字符串
            min_val (float, optional):
                滑块允许的最小值。
                默认值为 0.0
            max_val (float, optional):
                滑块允许的最大值。
                默认值为 1.0
            step (float, optional):
                滑块的步进值。
                默认值为 1.0
            default (float, optional):
                滑块的初始值。
                默认值为 0.0
        """
        self.text = text
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.step = float(step)
        self.default = float(default)

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text,
            "min": float(self.min_val),
            "max": float(self.max_val),
            "step": float(self.step),
            "default": float(self.default),
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
        self.text = ""
        self.min_val = 0.0
        self.max_val = 1.0
        self.step = 1.0
        self.default = 0.0
        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        min_val = data.get("min", 0.0)
        max_val = data.get("max", 1.0)
        step = data.get("step", 1.0)
        default = data.get("default", 0.0)

        if isinstance(text, str):
            self.text = text
        if not isinstance(min_val, bool) and isinstance(min_val, (float, int)):
            self.min_val = float(min_val)
        if not isinstance(max_val, bool) and isinstance(max_val, (float, int)):
            self.max_val = float(max_val)
        if not isinstance(step, bool) and isinstance(step, (float, int)):
            self.step = float(step)
        if not isinstance(default, bool) and isinstance(default, (float, int)):
            self.default = float(default)
        return self


class ModalFormElementStepSlider(ModalFormElement):
    """
    ModalFormElementStepSlider 指示模态表单中的显式步进滑块
    """

    text = ""  # type: str
    steps = []  # type: list[str]
    default = 0  # type: int

    def __init__(
        self, text="", steps=[], default=0
    ):  # type: (str, list[str], int) -> None
        """
        初始化并返回一个可放置在模态表单中的显式步进滑块

        Args:
            text (str, optional):
                滑块的标题文本。
                默认值为空字符串
            steps (list[str], optional):
                滑块的内容列表。
                默认值为空列表
            default (int, optional):
                滑块在初始状态下，
                所显示内容的索引。
                默认值为 0
        """
        self.text = text
        self.steps = steps if len(steps) > 0 else []
        self.default = int(default)

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {
            "text": self.text,
            "steps": self.steps,
            "default": int(self.default),
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
        self.text = ""
        self.steps = []
        self.default = 0
        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        steps = data.get("steps", [])
        default = data.get("default", 0)

        if isinstance(text, str):
            self.text = text
        if isinstance(steps, list):
            self.steps = [i for i in steps if isinstance(i, str)]
        if not isinstance(default, bool) and isinstance(default, (int, float)):
            self.default = int(default)
        return self


class ModalForm(BaseForm):
    """ModalForm 是模态表单的形式化表示"""

    title = ""  # type: str
    content = []  # type: list[ModalFormElement]

    def __init__(
        self, title="", content=[]
    ):  # type: (str, list[ModalFormElement]) -> None
        """初始化并返回一个新的形式化的模态表单

        Args:
            title (str, optional):
                模态表单的标题文本。
                默认值为空字符串
            content (list[ModalFormElement], optional):
                模态表单的内容。
                默认值为空列表
        """
        self.title = title
        self.content = content if len(content) > 0 else []

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将形式化的模态表单编码为对应的 JSON 表示

        Returns:
            dict[str, Any]: 该模态表单对应的 JSON 表示
        """
        content = []  # type: list[dict[str, Any]]

        for i in self.content:
            value = i.marshal()
            if isinstance(i, ModalFormElementLabel):
                value["type"] = "label"
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
            "title": self.title,
            "content": content,
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
        self.title = ""
        self.content = []
        if not isinstance(data, dict):
            return self

        title = data.get("title", "")
        if isinstance(title, str):
            self.title = title

        content = data.get("content", [])
        if not isinstance(content, list):
            return self
        for i in content:
            if not isinstance(i, dict):
                continue

            element_type = i.get("type", "")
            if not isinstance(element_type, str):
                continue
            if len(element_type) == 0:
                continue

            if element_type == "label":
                self.content.append(ModalFormElementLabel().unmarshal(i))
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
