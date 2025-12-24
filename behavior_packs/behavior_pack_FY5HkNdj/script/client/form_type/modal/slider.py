# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl

import uuid
from ..base import BaseComponent

DEF_NAME_SLIDER_STEP = "utils.slider_step"
DEF_NAME_SLIDER_STEP_PROGRESS = "utils.slider_step_progress"
DEF_NAME_SLIDER_STEP_HOVER = "utils.slider_step_hover"
DEF_NAME_SLIDER_STEP_PROGRESS_HOVER = "utils.slider_step_progress_hover"


def get_slider_def_name(
    slider_step_index, current_slider_index, is_hover
):  # type: (int, int, bool) -> str
    """
    get_slider_def_name 用于在渲染滑块的进度竖线时，
    根据进度竖线的索引 slider_step_index 和当前滑块
    的位置 current_slider_index 获取对应进度竖线控件
    的定义路径名

    Args:
        slider_step_index (int): 要渲染的进度竖线的索引
        current_slider_index (int): 滑块当前所在的位置
        is_hover (bool): 整个滑块是否已经被鼠标选中。
                         换句话说，它们是否已经变绿

    Returns:
        str: 欲渲染的进度竖线对应控件的定义路径名
    """
    if slider_step_index + 1 < current_slider_index:
        if not is_hover:
            return DEF_NAME_SLIDER_STEP
        else:
            return DEF_NAME_SLIDER_STEP_HOVER
    else:
        if not is_hover:
            return DEF_NAME_SLIDER_STEP_PROGRESS
        else:
            return DEF_NAME_SLIDER_STEP_PROGRESS_HOVER


def get_slider_step_texture_by_enum(slider_step_enum):  # type: (str) -> str
    """
    get_slider_step_texture_by_enum 根据进度
    竖线控件的定义路径名，获取其对应贴图路径

    Args:
        slider_step_enum (str): 进度竖线控件的定义路径名

    Returns:
        str: 该进度竖线控件应使用的贴图路径
    """
    if slider_step_enum == DEF_NAME_SLIDER_STEP:
        return "textures/ui/slider_step_background"
    if slider_step_enum == DEF_NAME_SLIDER_STEP_PROGRESS:
        return "textures/ui/slider_step_progress"
    if slider_step_enum == DEF_NAME_SLIDER_STEP_HOVER:
        return "textures/ui/slider_step_background_hover"
    if slider_step_enum == DEF_NAME_SLIDER_STEP_PROGRESS_HOVER:
        return "textures/ui/slider_step_progress_hover"
    return "textures/ui/slider_step_background"


class Slider(BaseComponent):
    """Slider 是隐式步进滑块实现"""

    slider_label = ""  # type: str
    slider_contents = []  # type: list[str]
    _should_update_screen = False  # type: bool
    _last_render_text = ""  # type: str

    def __init__(self, ui_node, control):  # type: (ScreenNode, BaseUIControl) -> None
        """初始化并返回一个新的 隐式步进滑块 实例

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将滑块挂接在哪个父节点下
        """
        self.ui_node = ui_node
        self.control = ui_node.CreateChildControl(
            "modal_component.custom_step_slider",
            "slider-" + str(uuid.uuid4()),
            control,
            False,
        )
        self.slider_label = ""
        self.slider_contents = []
        self._should_update_screen = False
        self._last_render_text = ""

    def _get_slider_control(self):  # type: () -> BaseUIControl | None
        """_get_slider_control 获取滑块控件的基本控件实例

        Returns:
            BaseUIControl | None: 如果成功，返回对应的控件实例。
                                  否则失败，那么返回 None
        """
        if self.control is None:
            return None
        return self.control.GetChildByPath(
            "/option_generic_core/two_line_layout/settings_common.option_slider_control/slider"
        )

    def _set_slider_text(self, slider_text):  # type: (str) -> Slider
        """_set_slider_text 设置滑块的文本

        Args:
            slider_text (str): 要设置的滑块文本

        Returns:
            Slider: 返回 Slider 本身
        """
        if self.control is None:
            return self

        child = self.control.GetChildByPath(
            "/option_generic_core/two_line_layout/option_label_panel/option_label"
        )
        if child is None:
            return self

        child = child.asLabel()
        if child is None:
            return self
        child.SetText(slider_text)

        return self

    def _set_slider_progress(
        self, slider_step, slider_value
    ):  # type: (int, float) -> Slider
        """_set_slider_progress 设置滑块的步进长度和进度

        Args:
            slider_step (int): 滑块的步进长度
            slider_value (float): 滑块应当抵达的进度

        Returns:
            Slider: 返回 Slider 本身
        """
        control = self._get_slider_control()
        if control is None:
            return self

        raw_bag = control.GetPropertyBag()  # type: Any
        property = raw_bag  # type: dict[str, Any]
        property["#slider_steps"] = slider_step
        property["#slider_value"] = slider_value

        control.SetPropertyBag(property)
        self._should_update_screen = True
        return self

    def on_update_screen(self):  # type: () -> bool
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Returns:
            bool: 指示是否需要刷新屏幕
        """
        should_update = self._should_update_screen
        if self._should_update_screen:
            self._should_update_screen = False

        index = self.get_slider_index()
        if index is None:
            return should_update

        content = self.slider_contents[index]
        current_render_text = self.slider_label + ": " + content
        if self._last_render_text != current_render_text:
            _ = self._set_slider_text(self.slider_label + ": " + content)
            self._last_render_text = current_render_text
            should_update = True

        return should_update

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None or self.control is None:
            return
        self.ui_node.RemoveChildControl(self.control)

    def get_slider_index(self):  # type: () -> int | None
        """get_slider_index 获取当前滑块所指示的内容的索引

        Returns:
            int | None: 如果获取成功，则返回索引；
                        否则获取失败，那么返回 None
        """
        if self.control is None:
            return None

        child = self.control.GetChildByPath(
            "/option_generic_core/two_line_layout"
            + "/settings_common.option_slider_control/slider"
        )
        if child is None:
            return None

        raw_bag = child.GetPropertyBag()  # type: Any
        property = raw_bag  # type: dict[str, Any]
        index = int(property["#slider_value"])
        if index >= len(self.slider_contents):
            return None

        return index

    def set_slider_label(self, label):  # type: (str) -> Slider
        """set_slider_label 设置滑块的标题

        Args:
            label (str): 欲设置的标题

        Returns:
            Slider: 返回 Slider 本身
        """
        self.slider_label = label
        return self

    def set_slider_contents(
        self, contents, index=-1
    ):  # type: (list[str], int) -> Slider
        """set_slider_contents 设置滑块可以选择的内容

        Args:
            contents (list[str]): 滑块可以选择的内容
            index (int, optional): 滑块最开始的位置。
                                   不使用请置为 -1

        Returns:
            Slider: 返回 Slider 本身
        """
        self.slider_contents = contents
        return self._set_slider_progress(
            len(contents), 0.0 if index == -1 else float(index)
        )


class StepSlider(Slider):
    """StepSlider 是基于 Slider 实现的显式步进滑块"""

    _last_slider_steps = 0  # type: int
    _slider_steps_control = []  # type: list[BaseUIControl]
    _slider_steps_def_name = []  # type: list[str]

    def __init__(self, ui_node, control):  # type: (ScreenNode, BaseUIControl) -> None
        """初始化并返回一个新的 显式步进滑块 实例

        Args:
            ui_node (ScreenNode): 该组件所在的屏幕结点
            control (BaseUIControl): 要将滑块挂接在哪个父节点下
        """
        Slider.__init__(self, ui_node, control)
        self._last_slider_steps = 0
        self._slider_steps_control = []
        self._slider_steps_def_name = []

    def _update_slider_step_progress(self):  # type: () -> bool
        """_update_slider_step_progress 更新滑块中各个进度竖线的显示状态

        Returns:
            bool: 如果有任何进度竖线的显示状态被更新，返回 True；
                  否则无需刷新屏幕，那么返回 False
        """
        if self.ui_node is None:
            return False

        control = self._get_slider_control()
        if control is None:
            return False
        slider_size = control.GetSize()
        if slider_size[0] == 0:
            return False

        slider_bar_hover = control.GetChildByPath("/slider_bar_hover")
        if slider_bar_hover is None:
            return False
        is_hover = slider_bar_hover.GetVisible()

        current_slider_index = self.get_slider_index()
        if current_slider_index is None:
            return False
        slider_step_count = len(self.slider_contents) - 2

        if self._last_slider_steps != len(self.slider_contents):
            for i in self._slider_steps_control:
                _ = self.ui_node.RemoveChildControl(i)
            self._slider_steps_control = []
            self._slider_steps_def_name = []

            for i in range(slider_step_count):
                slider_step_def_name = get_slider_def_name(
                    i, current_slider_index, is_hover
                )

                slider_step_control = self.ui_node.CreateChildControl(
                    slider_step_def_name,
                    "custom_step-" + str(uuid.uuid4()),
                    control,
                )
                slider_step_control.SetPosition(
                    (
                        (i + 1) * slider_size[0] / (slider_step_count + 1),
                        slider_step_control.GetPosition()[1],
                    )
                )

                self._slider_steps_control.append(slider_step_control)
                self._slider_steps_def_name.append(slider_step_def_name)

            self._last_slider_steps = len(self.slider_contents)
            return True

        should_update = False
        for i in range(slider_step_count):
            slider_step_def_name = get_slider_def_name(
                i, current_slider_index, is_hover
            )
            if self._slider_steps_def_name[i] == slider_step_def_name:
                continue

            image = self._slider_steps_control[i].asImage()
            if image is None:
                continue

            image.SetSprite(get_slider_step_texture_by_enum(slider_step_def_name))
            self._slider_steps_def_name[i] = slider_step_def_name
            should_update = True
        return should_update

    def on_update_screen(self):  # type: () -> bool
        """
        on_update_screen 在游戏每次刷新屏幕时调用。
        通常情况下，1 秒钟内游戏会调用 30 次

        Returns:
            bool: 指示是否需要刷新屏幕
        """
        should_update = False
        if Slider.on_update_screen(self):
            should_update = True
        if self._update_slider_step_progress():
            should_update = True
        return should_update

    def on_destroy(self):  # type: () -> None
        """on_destroy 在该组件被销毁时调用"""
        if self.ui_node is None:
            return
        for i in self._slider_steps_control:
            _ = self.ui_node.RemoveChildControl(i)
        Slider.on_destroy(self)
