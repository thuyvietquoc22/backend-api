import random as rd
from typing import get_args

from loguru import logger

from app.decorator import singleton
from app.entity.game.stone import Stone, RandomLevel1Config, RandomLevel2Config, RandomLevel3Config, StoneColor
from app.entity.game.user import User
from app.services.game.user import UserService
from app.utils import calculate_level
from app.utils.random_utils import RandomUtils


@singleton
class PrayService:

    def __init__(self):
        self.user_service = UserService()
        self.random_utils = RandomUtils(
            RandomLevel1Config(),
            RandomLevel2Config(),
            RandomLevel3Config()
        )

    def random_stone(self, exp: int):
        level = self.random_utils.get_item(exp)
        color = rd.choices(list(get_args(StoneColor)))[0]
        return Stone(level=level, color=color, amount=1)

    def pray(self, user: User, time: int = 1) -> list[Stone]:
        stones = [self.random_stone(user.experience) for _ in range(time)]
        logger.info(
            f"User {user.username} has lv {calculate_level(user.experience)} prayed {time} times and received {len(stones)} stones is {stones}")
        self.user_service.add_stone_to_user(user, stones)
        return stones
