from app.entity.game.battle import BattleResponse
from app.exceptions.base_exception import BaseExceptionMixin


class UserInBattleException(BaseExceptionMixin):

    def __init__(self, battles: list[BattleResponse]):
        super().__init__(f"User is in battle {[battle.id for battle in battles]}")
