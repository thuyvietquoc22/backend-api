from typing import Literal

from pydantic import BaseModel, Field

StoneColor = Literal["red", "green", "blue"]
StoneLevel = Literal[1, 2, 3]


class Stone(BaseModel):
    level: StoneLevel
    color: StoneColor
    amount: int = Field(..., ge=0, description="Amount of stone")

    @classmethod
    def of(cls, color: StoneColor, level: StoneLevel = 1) -> "Stone":
        return cls(level=level, color=color, amount=0)

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
