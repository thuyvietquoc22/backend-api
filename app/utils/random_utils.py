import random as rd
from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Callable

__T__ = TypeVar('__T__')

from loguru import logger

from app.utils import calculate_level


class RandomConfigBase(Generic[__T__], ABC):
    @property
    @abstractmethod
    def rate_by_exp(self) -> dict[range, Callable[[int], float]]:
        pass

    @property
    @abstractmethod
    def value(self) -> __T__:
        pass

    def get_rate(self, current_exp: int):
        for level_range, callback in self.rate_by_exp.items():
            if current_exp in level_range:
                level = calculate_level(current_exp)
                return callback(level)
        return 0.0


class RandomUtils:

    def __init__(self, *args: RandomConfigBase[__T__]):
        self.configs = args

    def get_item(self, exp: int) -> __T__:
        list_value = [i.value for i in self.configs]
        weights = [i.get_rate(exp) for i in self.configs]

        logger.debug(f"List_value={list_value}, weights={weights}")
        value = rd.choices(list_value, weights=weights)[0]
        logger.debug(f"Value={value}")
        return value
