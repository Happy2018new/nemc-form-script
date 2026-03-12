# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from .base import BaseForm
from ..base import StringWithHash
from ....formal.base import Marshaler

EMPTY_STRING_WITH_HASH = StringWithHash()


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

    image_path = EMPTY_STRING_WITH_HASH

    def __init__(
        self, image_path=EMPTY_STRING_WITH_HASH
    ):  # type: (StringWithHash) -> None
        """
        初始化并返回一个新的 LongFormIconPathImage

        Args:
            image_path (StringWithHash, optional):
                本地贴图路径，如 "textures/ui/anvil_icon.png"。
                默认值为 EMPTY_STRING_WITH_HASH
        """
        self.image_path = image_path

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将本实例编码为其对应 JSON 表示

        Returns:
            dict[str, Any]: 本实例对应的 JSON 表示
        """
        return {"data": self.image_path.marshal()}

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
        self.image_path = StringWithHash().unmarshal(data["data"])
        return self


class LongFormElement(Marshaler):
    """
    LongFormElement 是长表单中各种元素类别的总称
    """


class LongFormButton(LongFormElement):
    """LongFormButton 指示长表单中的单个按钮"""

    text = EMPTY_STRING_WITH_HASH
    icon = LongFormIcon()

    def __init__(
        self, text=EMPTY_STRING_WITH_HASH, icon=LongFormIconNone()
    ):  # type: (StringWithHash, LongFormIcon) -> None
        """初始化并返回一个新的 LongFormButton

        Args:
            text (StringWithHash, optional):
                该按钮上所显示的文本。
                默认值为 EMPTY_STRING_WITH_HASH
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
        if isinstance(self.icon, LongFormIconPathImage):
            return {
                "text": self.text.marshal(),
                "image": self.icon.marshal(),
            }
        else:
            return {
                "text": self.text.marshal(),
            }

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
        self.text = StringWithHash().unmarshal(data["text"])
        self.icon = (
            LongFormIconPathImage().unmarshal(data["image"])
            if "image" in data
            else LongFormIconNone()
        )
        return self


class LongFormLabel(LongFormElement):
    """LongFormLabel 指示长表单中的单个普通文本"""

    text = EMPTY_STRING_WITH_HASH

    def __init__(self, text=EMPTY_STRING_WITH_HASH):  # type: (StringWithHash) -> None
        """初始化并返回一个新的 LongFormLabel

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
        self.text = StringWithHash().unmarshal(data["text"])
        return self


class LongFormHeader(LongFormElement):
    """LongFormHeader 指示长表单中的单个大字文本"""

    text = EMPTY_STRING_WITH_HASH

    def __init__(self, text=EMPTY_STRING_WITH_HASH):  # type: (StringWithHash) -> None
        """初始化并返回一个新的 LongFormHeader

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
        self.text = StringWithHash().unmarshal(data["text"])
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
        return {}

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
    """LongForm 是数据保存实现中的长表单"""

    title = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    content = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    elements = []  # type: list[LongFormElement]

    onsubmit = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    oncancel = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    onsuberr = EMPTY_STRING_WITH_HASH  # type: StringWithHash
    oncanerr = EMPTY_STRING_WITH_HASH  # type: StringWithHash

    def __init__(
        self,
        title=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        content=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        elements=[],  # type: list[LongFormElement]
        onsubmit=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        oncancel=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        onsuberr=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
        oncanerr=EMPTY_STRING_WITH_HASH,  # type: StringWithHash
    ):  # type: (...) -> None
        """初始化并返回一个新的 LongForm

        Args:
            title (StringWithHash, optional):
                长表单的标题文本。
                默认值为 EMPTY_STRING_WITH_HASH
            content (StringWithHash, optional):
                长表单的内容文本。
                默认值为 EMPTY_STRING_WITH_HASH
            elements (list, optional):
                长表单中的按钮。
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
        self.content = content
        self.elements = elements if len(elements) > 0 else []
        self.onsubmit = onsubmit
        self.oncancel = oncancel
        self.onsuberr = onsuberr
        self.oncanerr = oncanerr

    def marshal(self):  # type: () -> dict[str, Any]
        """marshal 将该 LongForm 编码为对应的 JSON 表示

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
            "title": self.title.marshal(),
            "content": self.content.marshal(),
            "elements": elements,
            "onsubmit": self.onsubmit.marshal(),
            "oncancel": self.oncancel.marshal(),
            "onsuberr": self.onsuberr.marshal(),
            "oncanerr": self.oncanerr.marshal(),
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
        assert isinstance(data, dict)

        self.title = StringWithHash().unmarshal(data["title"])
        self.content = StringWithHash().unmarshal(data["content"])
        self.onsubmit = StringWithHash().unmarshal(data["onsubmit"])
        self.oncancel = StringWithHash().unmarshal(data["oncancel"])
        self.onsuberr = StringWithHash().unmarshal(data["onsuberr"])
        self.oncanerr = StringWithHash().unmarshal(data["oncanerr"])

        if "buttons" in data:
            self.elements = [LongFormButton().unmarshal(i) for i in data["buttons"]]
            return self

        self.elements = []
        for i in data["elements"]:
            element_type = i["type"]
            if element_type == "button":
                self.elements.append(LongFormButton().unmarshal(i))
            elif element_type == "label":
                self.elements.append(LongFormLabel().unmarshal(i))
            elif element_type == "header":
                self.elements.append(LongFormHeader().unmarshal(i))
            elif element_type == "divider":
                self.elements.append(LongFormDivider().unmarshal(i))

        return self

    def all_codes(self):  # type: () -> list[StringWithHash]
        """
        all_codes 返回该 LongForm 中存在的所有代码

        Returns:
            list[StringWithHash]:
                该 LongForm 中存在的所有代码
        """
        codes = [
            self.title,
            self.content,
            self.onsubmit,
            self.oncancel,
            self.onsuberr,
            self.oncanerr,
        ]  # type: list[StringWithHash]

        for i in self.elements:
            if isinstance(i, LongFormButton):
                codes.append(i.text)
                if isinstance(i.icon, LongFormIconPathImage):
                    codes.append(i.icon.image_path)
            elif isinstance(i, LongFormLabel):
                codes.append(i.text)
            elif isinstance(i, LongFormHeader):
                codes.append(i.text)
            elif isinstance(i, LongFormDivider):
                pass

        return codes
