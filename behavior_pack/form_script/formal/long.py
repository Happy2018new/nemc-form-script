# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from .base import Marshaler, BaseForm


class LongFormIcon(Marshaler):
    """LongFormIcon 是长表单中单个按钮所使用的图标的总称"""


class LongFormIconNone(LongFormIcon):
    """
    LongFormIconNone 指示没有图标。
    任何使用该图标的按钮将不显示图标
    """

    def __init__(self):  # type: () -> None
        """
        初始化并返回一个新的 LongFormIconNone
        """
        return

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {}

    def unmarshal(self, data):  # type: (Any) -> LongFormIconNone
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            LongFormIconNone: 返回 LongFormIconNone 本身
        """
        _ = data
        return self


class LongFormIconPathImage(LongFormIcon):
    """LongFormIconPathImage 指示使用本地材质贴图作为按钮的图标"""

    image_path = ""

    def __init__(self, image_path=""):  # type: (str) -> None
        """
        初始化并返回一个新的 LongFormIconPathImage

        Args:
            image_path (str, optional):
                本地贴图路径，如 "textures/ui/anvil_icon.png"。
                默认值为空字符串
        """
        self.image_path = image_path

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {"data": self.image_path}

    def unmarshal(self, data):  # type: (Any) -> LongFormIconPathImage
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            LongFormIconPathImage: 返回 LongFormIconPathImage 本身
        """
        self.text = ""
        if not isinstance(data, dict):
            return self

        data = data.get("data", "")
        if isinstance(data, str):
            self.image_path = data
        return self


class LongFormIconURLImage(LongFormIcon):
    """LongFormIconURLImage 指示使用 URL 所指示的图片作为按钮的图标"""

    image_url = ""

    def __init__(self, image_url=""):  # type: (str) -> None
        """
        初始化并返回一个新的 LongFormIconURLImage

        Args:
            image_url (str, optional):
                图片的 URL 地址。
                默认值为空字符串
        """
        self.image_url = image_url

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {"data": self.image_url}

    def unmarshal(self, data):  # type: (Any) -> LongFormIconURLImage
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            LongFormIconURLImage: 返回 LongFormIconURLImage 本身
        """
        self.image_url = ""
        if not isinstance(data, dict):
            return self

        data = data.get("data", "")
        if isinstance(data, str):
            self.image_url = data
        return self


class LongFormElement(Marshaler):
    """
    LongFormElement 是长表单中各种元素类别的总称
    """


class LongFormButton(LongFormElement):
    """LongFormButton 指示长表单中的单个按钮"""

    text = ""
    icon = LongFormIcon()

    def __init__(
        self, text="", icon=LongFormIconNone()
    ):  # type: (str, LongFormIcon) -> None
        """初始化并返回一个新的 LongFormButton

        Args:
            text (str, optional):
                该按钮上所显示的文本。
                默认值为空字符串
            icon (LongFormIcon, optional):
                该按钮所使用的图标。
                默认值为 LongFormIconNone()
        """
        self.text = text
        self.icon = (
            icon if not isinstance(icon, LongFormIconNone) else LongFormIconNone()
        )

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        image = self.icon.marshal()

        if isinstance(self.icon, LongFormIconPathImage):
            image["type"] = "path"
            return {"text": self.text, "image": image}
        elif isinstance(self.icon, LongFormIconURLImage):
            image["type"] = "url"
            return {"text": self.text, "image": image}

        return {"text": self.text, "image": None}

    def unmarshal(self, data):  # type: (Any) -> LongFormButton
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            LongFormButton: 返回 LongFormButton 本身
        """
        self.text = ""
        self.icon = LongFormIconNone()

        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        if isinstance(text, str):
            self.text = text

        image = data.get("image", None)
        if image is None or not isinstance(image, dict):
            return self
        if len(image) == 0:
            return self

        image_type = image.get("type", "")
        if not isinstance(image_type, str):
            return self
        if image_type == "path":
            self.icon = LongFormIconPathImage().unmarshal(image)
        elif image_type == "url":
            self.icon = LongFormIconURLImage().unmarshal(image)

        return self


class LongFormLabel(LongFormElement):
    """LongFormLabel 指示长表单中的单个普通文本"""

    text = ""

    def __init__(self, text=""):  # type: (str) -> None
        """初始化并返回一个新的 LongFormLabel

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

    def unmarshal(self, data):  # type: (Any) -> LongFormLabel
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            LongFormLabel: 返回 LongFormLabel 本身
        """
        self.text = ""
        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        if isinstance(text, str):
            self.text = text
        return self


class LongFormHeader(LongFormElement):
    """LongFormHeader 指示长表单中的单个大字文本"""

    text = ""

    def __init__(self, text=""):  # type: (str) -> None
        """初始化并返回一个新的 LongFormHeader

        Args:
            text (str, optional):
                大字文本的内容。
                默认值为空字符串
        """
        self.text = text

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {"text": self.text}

    def unmarshal(self, data):  # type: (Any) -> LongFormHeader
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            LongFormHeader: 返回 LongFormHeader 本身
        """
        self.text = ""
        if not isinstance(data, dict):
            return self

        text = data.get("text", "")
        if isinstance(text, str):
            self.text = text
        return self


class LongFormDivider(LongFormElement):
    """LongFormDivider 指示长表单中的单个分割线"""

    def __init__(self):  # type: () -> None
        """初始化并返回一个新的 LongFormDivider"""
        pass

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {"text": ""}

    def unmarshal(self, data):  # type: (Any) -> LongFormDivider
        """
        unmarshal 从 data 所指示的 JSON 数据中解码，
        然后将解码所得的数据传输到本实例中

        Args:
            data (Any): 给定的 JSON 数据。
                        应确保它是一个字典

        Returns:
            LongFormDivider: 返回 LongFormDivider 本身
        """
        _ = data
        return self


class LongForm(BaseForm):
    """LongForm 是长表单的形式化表示"""

    title = ""  # type: str
    content = ""  # type: str
    elements = []  # type: list[LongFormElement]

    def __init__(
        self, title="", content="", elements=[]
    ):  # type: (str, str, list[LongFormElement]) -> None
        """初始化并返回一个新的形式化的长表单

        Args:
            title (str, optional):
                长表单的标题文本。
                默认值为空字符串
            content (str, optional):
                长表单的内容文本。
                默认值为空字符串
            elements (list[LongFormElement], optional):
                长表单中的元素。
                默认值为空列表
        """
        self.title = title
        self.content = content
        self.elements = elements if len(elements) > 0 else []

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将形式化的长表单编码为对应的 JSON 表示

        Returns:
            dict[str, Any]: 该长表单对应的 JSON 表示
        """
        elements = []  # type: list[dict[str, Any]]

        for i in self.elements:
            value = i.marshal()
            if isinstance(i, LongFormButton):
                value["type"] = "button"
            elif isinstance(i, LongFormLabel):
                value["type"] = "label"
            elif isinstance(i, LongFormHeader):
                value["type"] = "header"
            elif isinstance(i, LongFormDivider):
                value["type"] = "divider"
            elements.append(value)

        return {
            "title": self.title,
            "content": self.content,
            "elements": elements,
        }

    def unmarshal(self, data):  # type: (Any) -> LongForm
        """
        unmarshal 从 JSON 中解码数据，
        并将解码所得的数据置入本实例中

        Args:
            data (Any): 给定的 data 数据。
                        应确保它是一个字典

        Returns:
            LongForm: 返回 LongForm 本身
        """
        self.title = ""
        self.content = ""
        self.elements = []
        if not isinstance(data, dict):
            return self

        title = data.get("title", "")
        content = data.get("content", "")

        if isinstance(title, str):
            self.title = title
        if isinstance(content, str):
            self.content = content

        if "buttons" in data:
            buttons = data["buttons"]
            if isinstance(buttons, list):
                self.elements = [LongFormButton().unmarshal(i) for i in buttons]
            return self

        elements = data.get("elements", [])
        if not isinstance(elements, list):
            return self
        for i in elements:
            if not isinstance(i, dict):
                continue

            element_type = i.get("type", "")
            if not isinstance(element_type, str):
                continue
            if len(element_type) == 0:
                continue

            if element_type == "button":
                self.elements.append(LongFormButton().unmarshal(i))
            elif element_type == "label":
                self.elements.append(LongFormLabel().unmarshal(i))
            elif element_type == "header":
                self.elements.append(LongFormHeader().unmarshal(i))
            elif element_type == "divider":
                self.elements.append(LongFormDivider().unmarshal(i))

        return self
