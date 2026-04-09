# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable
    from mod.server.extraServerApi import ServerSystem

from .static import (
    BaseManager,
    Reflect,
    Slices,
    Maps,
    Tuple,
    Set,
    Strings,
    UUID,
    StructTime,
    CommonTime,
    Math,
    Random,
    JSON,
    Binascii,
    TimeDelta,
    Time,
    Date,
    DateTime,
    Base64,
)
from .dynamic import (
    Context,
    General,
    World,
    Entity,
    Player,
    Block,
    Item,
    Utils,
)


def new_base_manager():  # type: () -> BaseManager
    """
    new_base_manager 初始化并返回一个新的基本管理器

    manager (BaseManager):
                用于管理引用对象的对象管理器
    """
    return BaseManager()


class StaticBuiltInFunction:
    """StaticBuiltInFunction 管理了所有静态的内置函数"""

    manager = None  # type: BaseManager | None
    reflect = None  # type: Reflect | None
    slices = None  # type: Slices | None
    maps = None  # type: Maps | None
    tuple = None  # type: Tuple | None
    set = None  # type: Set | None
    strings = None  # type: Strings | None
    uuid = None  # type: UUID | None
    struct_time = None  # type: StructTime | None
    common_time = None  # type: CommonTime | None
    math = None  # type: Math | None
    random = None  # type: Random | None
    json = None  # type: JSON | None
    binascii = None  # type: Binascii | None
    time = None  # type: Time | None
    date = None  # type: Date | None
    datetime = None  # type: DateTime | None
    timedelta = None  # type: TimeDelta | None
    base64 = None  # type: Base64 | None

    def __init__(self, manager=None):  # type: (BaseManager | None) -> None
        """
        初始化并返回一个新的静态内置函数集合

        Args:
            manager (BaseManager | None):
                用于管理引用对象的对象管理器。
                默认值为 None
        """
        self.manager = manager if manager is not None else new_base_manager()
        self.reflect = Reflect(self.manager)
        self.slices = Slices(self.manager)
        self.maps = Maps(self.manager)
        self.tuple = Tuple(self.manager)
        self.set = Set(self.manager)
        self.strings = Strings(self.manager)
        self.uuid = UUID(self.manager)
        self.struct_time = StructTime(self.manager)
        self.common_time = CommonTime(self.manager)
        self.math = Math(self.manager)
        self.random = Random(self.manager)
        self.json = JSON(self.manager)
        self.binascii = Binascii(self.manager)
        self.time = Time(self.manager)
        self.date = Date(self.manager)
        self.datetime = DateTime(self.manager)
        self.timedelta = TimeDelta(self.manager)
        self.base64 = Base64(self.manager)

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建所有静态内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        assert self.manager is not None
        assert self.reflect is not None
        assert self.slices is not None
        assert self.maps is not None
        assert self.tuple is not None
        assert self.set is not None
        assert self.strings is not None
        assert self.uuid is not None
        assert self.struct_time is not None
        assert self.common_time is not None
        assert self.math is not None
        assert self.random is not None
        assert self.json is not None
        assert self.binascii is not None
        assert self.time is not None
        assert self.date is not None
        assert self.datetime is not None
        assert self.timedelta is not None
        assert self.base64 is not None

        self.manager.build_func(origin)
        self.reflect.build_func(origin)
        self.slices.build_func(origin)
        self.maps.build_func(origin)
        self.tuple.build_func(origin)
        self.set.build_func(origin)
        self.strings.build_func(origin)
        self.uuid.build_func(origin)
        self.struct_time.build_func(origin)
        self.common_time.build_func(origin)
        self.math.build_func(origin)
        self.random.build_func(origin)
        self.json.build_func(origin)
        self.binascii.build_func(origin)
        self.time.build_func(origin)
        self.date.build_func(origin)
        self.datetime.build_func(origin)
        self.timedelta.build_func(origin)
        self.base64.build_func(origin)


class DynamicBuiltInFunction:
    """DynamicBuiltInFunction 管理了所有动态的内置函数"""

    context = None  # type: Context | None
    general = None  # type: General | None
    world = None  # type: World | None
    entity = None  # type: Entity | None
    player = None  # type: Player | None
    block = None  # type: Block | None
    item = None  # type: Item | None
    utils = None  # type: Utils | None

    def __init__(self, manager, system):  # type: (BaseManager, ServerSystem) -> None
        """
        初始化并返回一个新的动态内置函数集合

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
            system (ServerSystem):
                当前模组的服务端实现
        """
        self.context = Context(manager)
        self.general = General(manager, system)
        self.world = World(manager, system)
        self.entity = Entity(manager)
        self.player = Player(manager)
        self.block = Block(manager)
        self.item = Item(manager)
        self.utils = Utils(manager)

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建所有动态内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        assert self.context is not None
        assert self.general is not None
        assert self.world is not None
        assert self.entity is not None
        assert self.player is not None
        assert self.block is not None
        assert self.item is not None
        assert self.utils is not None

        self.context.build_func(origin)
        self.general.build_func(origin)
        self.world.build_func(origin)
        self.entity.build_func(origin)
        self.player.build_func(origin)
        self.block.build_func(origin)
        self.item.build_func(origin)
        self.utils.build_func(origin)
