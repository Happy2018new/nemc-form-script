# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from mod.client.extraClientApi import ScreenNode
    from mod.client.ui.controls.baseUIControl import BaseUIControl

from mod.client.extraClientApi import (
    GetEngineCompFactory,
    GetLevelId,
    GetMinecraftEnum,
)


def point_is_in_rect(
    rect,  # type: tuple[tuple[float,float], tuple[float,float], tuple[float,float], tuple[float,float]]
    point,  # type: tuple[float, float]
):  # type: (...) -> bool
    """
    point_is_in_rect 测定给定的点是否在给定的矩形内（含边界）

    Args:
        rect (tuple[tuple[float,float], tuple[float,float], tuple[float,float], tuple[float,float]]): 矩形的四个顶点坐标
        point (tuple[float, float]): 给定的待测点的坐标

    Returns:
        bool: 如果给定的点在给定的矩形内（含边界），则返回 True；
              否则给定的点不在给定的矩形内，那么返回 False
    """
    if len(set(rect)) != 4:
        return False

    min_x = min(rect[0][0], rect[1][0], rect[2][0], rect[3][0])
    min_y = min(rect[0][1], rect[1][1], rect[2][1], rect[3][1])
    max_x = max(rect[0][0], rect[1][0], rect[2][0], rect[3][0])
    max_y = max(rect[0][1], rect[1][1], rect[2][1], rect[3][1])

    return min_x <= point[0] <= max_x and min_y <= point[1] <= max_y


def input_mode_is_touch():  # type: () -> bool
    """
    input_mode_is_touch 检测当前输入模式是否为触摸屏模式

    Returns:
        bool: 指示当前输入模式是否为触摸屏模式
    """
    comp = GetEngineCompFactory().CreatePlayerView(GetLevelId())
    enum = comp.GetToggleOption(GetMinecraftEnum().OptionId.INPUT_MODE)
    return enum == GetMinecraftEnum().InputMode.Touch


def check_esc_key(key):  # type: (str) -> bool
    """check_esc_key 检查 key 是否指示 ESC 按键

    Args:
        key (str): 欲被检查的按键

    Returns:
        bool: 如果 key 指示 ESC 按键，则返回真；
              否则 key 指示其他按键，那么返回假
    """
    return key == str(GetMinecraftEnum().KeyBoardType.KEY_ESCAPE)


def get_base_path():  # type: () -> str
    """
    get_base_path 返回表单的顶层绝对路径

    Returns:
        str: 表单的顶层绝对路径
    """
    return (
        "/variables_button_mappings_and_controls/safezone_screen_matrix"
        + "/inner_matrix/safezone_screen_panel"
        + "/root_screen_panel/form_factory"
    )


def get_scorll_view_background(
    node, path
):  # type: (ScreenNode, str) -> BaseUIControl | None
    """
    get_scorll_view_background 预期 path 所指示的控件
    下包含 scroll_touch 或 scroll_mouse 子节点，并获取
    该子节点下相应 Scroll View 的 Content 节点。

    如果给定的 path 不满足预期，或相应的 Content 节点未找到，
    那么 get_scorll_view_background 视作失败，那么返回 None

    Args:
        node (ScreenNode): 顶层 UI 的 ScreenNode 实例
        path (str): 被预期的控件的绝对路径

    Returns:
        BaseUIControl | None: 相应 Scroll View 的 Content 节点
    """
    parent = node.GetBaseUIControl(path)
    if parent is None:
        return None

    child = parent.GetChildByPath("/panel_indent/inside_header_panel")
    if child is not None:
        parent = child
    child = parent.GetChildByPath("/scroll")
    if child is not None:
        parent = child
    child = parent.GetChildByPath("/scrolling_panel")
    if child is not None:
        parent = child

    child = parent.GetChildByPath("/scroll_touch")
    if child is None:
        child = parent.GetChildByPath("/scroll_mouse")
    if child is None:
        return None

    panel = child.GetChildByPath("/scroll_view/panel")
    if panel is None:
        panel = child.GetChildByPath("/scroll_view/stack_panel")
    if panel is None:
        return None

    return panel.GetChildByPath("/background_and_viewport")


def get_scroll_view_content(
    node, path
):  # type: (ScreenNode, str) -> BaseUIControl | None
    """
    get_scroll_view_content 预期 path 所指示的
    控件下包含 scroll_touch 或 scroll_mouse 子节点，
    并获取该子节点下相应 Scroll View 的 Content 节点。

    如果给定的 path 不满足预期，或相应的 Content 节点未找到，
    那么 get_scroll_view_content 视作失败，那么返回 None

    Args:
        node (ScreenNode): 顶层 UI 的 ScreenNode 实例
        path (str): 被预期的控件的绝对路径

    Returns:
        BaseUIControl | None: 相应 Scroll View 的 Content 节点
    """
    control = get_scorll_view_background(node, path)
    if control is None:
        return None
    return control.GetChildByPath("/scrolling_view_port/scrolling_content")
