from loguru import logger
from pydantic import ValidationError

from app.entity.game.stone import Stone
from app.entity.game.user import User, BaseUser


class TestUser:

    @staticmethod
    def test_duplicate_stone_in_bag():
        try:
            BaseUser(
                tele_id=1,
                username="test",
                stones=[
                    Stone(level=1, color="red", amount=100),
                    Stone(level=1, color="blue", amount=200),
                    Stone(level=1, color="red", amount=300),
                    Stone(level=2, color="red", amount=400),
                    Stone(level=2, color="red", amount=500),
                    Stone(level=2, color="red", amount=600),
                    Stone(level=3, color="red", amount=700),
                    Stone(level=3, color="red", amount=800),
                    Stone(level=3, color="red", amount=900)
                ]
            )
            assert False
        except ValidationError as e:
            assert "Duplicate stones" in str(e)

    @staticmethod
    def test_not_duplicate_stone_in_bag():
        try:
            BaseUser(
                tele_id=1,
                username="test",
                stones=[
                    Stone(level=1, color="red", amount=100),
                    Stone(level=1, color="blue", amount=200),
                    Stone(level=1, color="green", amount=300),
                    Stone(level=2, color="red", amount=400),
                    Stone(level=2, color="blue", amount=500),
                    Stone(level=2, color="green", amount=600),
                    Stone(level=3, color="red", amount=700),
                    Stone(level=3, color="blue", amount=800),
                    Stone(level=3, color="green", amount=900)
                ]
            )
            assert True
        except ValidationError as e:
            logger.error(e)
            assert False
