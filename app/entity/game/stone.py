from typing import Literal

from pydantic import BaseModel, Field


class Stone(BaseModel):
    level: Literal[1, 2, 3]
    color: Literal["red", "green", "blue"]
    amount: int = Field(..., ge=0, description="Amount of stone")



    def __eq__(self, other):
        return self.level == other.level and self.color == other.color

    def __hash__(self):
        return hash((self.level, self.color))
