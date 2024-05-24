from enum import Enum
from typing import Literal, Callable

from pydantic import BaseModel, Field

from app.core.contance import Experience as Exp
from app.utils.random_utils import RandomConfigBase

StoneColor = Literal["red", "green", "blue"]
StoneLevel = Literal[1, 2, 3]


class Stone(BaseModel):
    level: StoneLevel
    color: StoneColor
    amount: int = Field(..., ge=0, description="Amount of stone")

    @classmethod
    def of(cls, color: StoneColor, level: StoneLevel = 1) -> "Stone":
        return cls(level=level, color=color, amount=0)

    def convert_to_level_1(self) -> "Stone":
        return Stone(level=1, color=self.color, amount=self.amount * (20 ** (self.level - 1)))

    def insert_to(self, stones: list["Stone"]) -> int:
        """
        Insert stone to list of stones
        :param stones:
        :return: index inserted
        """
        try:
            index = stones.index(self)
            stones[index].amount += self.amount
            return index
        except ValueError as e:
            if "is not in list" not in str(e):
                raise e
            stones.append(self)
            return len(stones) - 1

    def __eq__(self, other):
        return self.level == other.level and self.color == other.color

    def __hash__(self):
        return hash((self.level, self.color))

    def __ge__(self, other):
        if self == other:
            return self.amount >= other.amount
        raise ValueError("Cannot compare different stone")

    def __gt__(self, other):
        if self == other:
            return self.amount > other.amount
        raise ValueError("Cannot compare different stone")

    def __le__(self, other):
        if self == other:
            return self.amount <= other.amount
        raise ValueError("Cannot compare different stone")

    def __lt__(self, other):
        if self == other:
            return self.amount < other.amount
        raise ValueError("Cannot compare different stone")

    def __sub__(self, other):
        if self == other:
            self.amount -= other.amount
            return self.amount - other.amount
        raise ValueError("Cannot subtract different stone")


class RandomLevel1Config(RandomConfigBase[StoneLevel]):
    @property
    def rate_by_exp(self) -> dict[range, Callable[[int], float]]:
        def callback_1_35(exp: int):
            # y = -0.3529411764706x + 90.3529411764706
            return -0.3529411764706 * exp + 90.3529411764706  # using exp to calculate rate

        def callback_35_70(exp: int):
            # y = -x + 113
            return -exp + 113  # using exp to calculate rate

        def callback_70_999(exp: int):
            # y = -0.7666666666667x + 96.6666666666667
            return -0.7666666666667 * exp + 96.6666666666667

        return {
            range(int(Exp.LEVEL_1.value), int(Exp.LEVEL_35.value)): callback_1_35,
            range(int(Exp.LEVEL_35.value), int(Exp.LEVEL_70.value)): callback_35_70,
            range(int(Exp.LEVEL_70.value), int(Exp.LEVEL_100.value)): callback_70_999
        }

    @property
    def value(self) -> StoneLevel:
        return 1


class RandomLevel2Config(RandomConfigBase[StoneLevel]):
    @property
    def rate_by_exp(self) -> dict[range, Callable[[int], float]]:
        def callback_1_35(exp: int):
            # y = 0.2941176470588x + 9.7058823529412
            return 0.2941176470588 * exp + 9.7058823529412  # using exp to calculate rate

        def callback_35_70(exp: int):
            # y = 0.8571428571429x - 10
            return 0.8571428571429 * exp - 10  # using exp to calculate rate

        def callback_70_999(exp: int):
            # y = 0.3333333333333x + 26.6666666666667
            return 0.3333333333333 * exp + 26.6666666666667  # using exp to calculate rate

        return {
            range(int(Exp.LEVEL_1.value), int(Exp.LEVEL_35.value)): callback_1_35,
            range(int(Exp.LEVEL_35.value), int(Exp.LEVEL_70.value)): callback_35_70,
            range(int(Exp.LEVEL_70.value), int(Exp.LEVEL_100.value)): callback_70_999
        }

    @property
    def value(self) -> StoneLevel:
        return 2


class RandomLevel3Config(RandomConfigBase[StoneLevel]):
    @property
    def rate_by_exp(self) -> dict[range, Callable[[int], float]]:
        def callback_1_35(exp: int):
            # y = 0.0588235294118x - 0.0588235294118
            return 0.0588235294118 * exp - 0.0588235294118  # using exp to calculate rate

        def callback_35_70(exp: int):
            # y = 0.1428571428571x - 3
            return 0.1428571428571 * exp - 3

        def callback_70_999(exp: int):
            # y = 0.4333333333333x - 23.3333333333333
            return 0.4333333333333 * exp - 23.3333333333333

        return {
            range(int(Exp.LEVEL_1.value), int(Exp.LEVEL_35.value)): callback_1_35,
            range(int(Exp.LEVEL_35.value), int(Exp.LEVEL_70.value)): callback_35_70,
            range(int(Exp.LEVEL_70.value), int(Exp.LEVEL_100.value)): callback_70_999
        }

    @property
    def value(self) -> StoneLevel:
        return 3
