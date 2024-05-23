from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Callable
import random as rd

__T__ = TypeVar('__T__')


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
                return callback(current_exp)
        return 0.0


class RandomUtils:

    def __init__(self, *args: RandomConfigBase[__T__]):
        self.configs = args

    def get_item(self, exp: int) -> __T__:
        list_value = [i.value for i in self.configs]
        weights = [i.get_rate(exp) for i in self.configs]

        return rd.choices(list_value, weights=weights)[0]
