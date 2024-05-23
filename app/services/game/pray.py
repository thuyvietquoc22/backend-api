import random as rd

from loguru import logger

from app.decorator import singleton
from app.entity.game.stone import Stone
from app.entity.game.user import User
from app.services.game.user import UserService


@singleton
class PrayService:

    def __init__(self):
        self.user_service = UserService()

    @property
    def rate_map_level(self):
        return {
            1: 0.5,
            2: 0.3,
            3: 0.2
        }

    @property
    def rate_map_color(self):
        return {
            "red": 0.3,
            "green": 0.3,
            "blue": 0.4
        }

    def random_stone(self):
        level = rd.choices(list(self.rate_map_level.keys()), weights=list(self.rate_map_level.values()))[0]
        color = rd.choices(list(self.rate_map_color.keys()), weights=list(self.rate_map_color.values()))[0]
        return Stone(level=level, color=color, amount=1)

    def pray(self, user: User, time: int = 1) -> list[Stone]:
        stones = [self.random_stone() for _ in range(time)]
        logger.info(f"User {user.username} prayed {time} times and received {len(stones)} stones is {stones}")
        self.user_service.add_stone_to_user(user, stones)
        return stones
