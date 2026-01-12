# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Callable

import random
from .lib_object import BaseManager


class Random:
    """
    Random 提供了随机数相关的内置函数
    """

    _manager = BaseManager()

    def __init__(self, manager):  # type: (BaseManager) -> None
        """初始化并返回一个新的 Random

        Args:
            manager (BaseManager):
                用于管理引用对象的对象管理器
        """
        self._manager = manager

    def rand(self):  # type: () -> random.Random
        """
        rand 返回用于生成随机数的随机数生成器。
        它是对 self._manager.rand() 的简单包装

        Returns:
            random.Random:
                用于生成随机数的随机数生成器
        """
        return self._manager.rand()

    def shuffle(self, ptr):  # type: (int) -> bool
        """
        shuffle shuffles the given list in place,
        and always returns True.

        Args:
            ptr (int):
                The pointer points to the list to be shuffled

        Returns:
            bool: Always returns True
        """
        self.rand().shuffle(self._manager.deref(ptr))
        return True

    def seed(self, a=None):  # type: (int | float | str | None) -> bool
        """
        Initialize internal state from a seed.

        The only supported seed types are None, int, float or str.

        None or no argument seeds from current time or from
        an operating system specific randomness source if available.

        If *a* is an int, all bits are used.

        Args:
            a (int | float | str | None, optional):
                The seed value.
                Defaults to None.

        Returns:
            bool: Always returns True
        """
        self.rand().seed(a)
        return True

    def setstate(self, ptr):  # type: (int) -> bool
        """
        setstate restores internal state
        from object returned by getstate.

        Args:
            ptr (int):
                The pointer points to the state object

        Returns:
            bool: Always returns True
        """
        self.rand().setstate(self._manager.deref(ptr))
        return True

    def build_func(
        self,
        origin,  # type: dict[str, Callable[..., int | bool | float | str]]
    ):  # type: (...) -> None
        """
        build_func 构建 random 模块的内置函数，
        并将构建结果写入到传递的 origin 字典中

        Args:
            origin (dict[str, Callable[..., int | bool | float | str]]):
                用于存放所有内置函数的字典
        """
        funcs = {}  # type: dict[str, Callable[..., int | bool | float | str]]

        funcs["random.betavariate"] = lambda alpha, beta: self.rand().betavariate(
            alpha, beta
        )
        funcs["random.choice"] = lambda ptr: self._manager.ref(
            self.rand().choice(self._manager.deref(ptr))
        )
        funcs["random.expovariate"] = lambda lambd=1.0: self.rand().expovariate(lambd)
        funcs["random.gammavariate"] = lambda alpha, beta: self.rand().gammavariate(
            alpha, beta
        )
        funcs["random.gauss"] = lambda mu=0.0, sigma=1.0: self.rand().gauss(mu, sigma)
        funcs["random.lognormvariate"] = lambda mu, sigma: self.rand().lognormvariate(
            mu, sigma
        )
        funcs["random.normalvariate"] = (
            lambda mu=0.0, sigma=1.0: self.rand().normalvariate(mu, sigma)
        )
        funcs["random.paretovariate"] = lambda alpha: self.rand().paretovariate(alpha)
        funcs["random.randint"] = lambda a, b: self.rand().randint(a, b)
        funcs["random.random"] = lambda: self.rand().random()
        funcs["random.randrange"] = (
            lambda start, stop=None, step=1: self.rand().randrange(start, stop, step)
        )
        funcs["random.sample"] = lambda population_ptr, k: self._manager.ref(
            self.rand().sample(self._manager.deref(population_ptr), k)
        )
        funcs["random.shuffle"] = self.shuffle
        funcs["random.triangular"] = (
            lambda low=0.0, high=1.0, mode=None: self.rand().triangular(low, high, mode)
        )
        funcs["random.uniform"] = lambda a, b: self.rand().uniform(a, b)
        funcs["random.vonmisesvariate"] = lambda mu, kappa: self.rand().vonmisesvariate(
            mu, kappa
        )
        funcs["random.weibullvariate"] = lambda alpha, beta: self.rand().weibullvariate(
            alpha, beta
        )
        funcs["random.seed"] = self.seed
        funcs["random.getstate"] = lambda: self._manager.ref(self.rand().getstate())
        funcs["random.setstate"] = self.setstate

        for key, value in funcs.items():
            origin[key] = value
