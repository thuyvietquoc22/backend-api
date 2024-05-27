import random as rd

from app.decorator import singleton
from app.decorator.parser import parse_as
from app.entity.game.battle import BattleCreate, BattleStart, BattleResponse, BattleEnd
from app.entity.game.user import User
from app.exceptions.game.user_in_battle_exception import UserInBattleException
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.repositories.battle import BattleRepository
from app.services.game.character import CharacterService
from app.services.game.root_character import RootCharacterService


@singleton
class BattleService:
    def __init__(self):
        self.battle_repo = BattleRepository()
        self.character_service = CharacterService()
        self.r_character = RootCharacterService().get_root_characters()

    @parse_as(BattleResponse, True)
    def start_battle(self, battle_create: BattleStart, user: User):

        # TODO Check user has battle before
        battling = self.battle_repo.find_battling_by_user_id(user.id)
        if len(battling) > 0:
            raise UserInBattleException(battling)

        # TODO Check user.character_id belongs to user
        character = self.character_service.get_character_by_id(battle_create.character_id)
        if character.owner_id != user.id:  # có thể khác kiểm dữ liêu nhớ debug
            raise ParamInvalidException("Character in battle must belong to user")

        # TODO Save battle to database
        battle = BattleCreate.from_battle_start(battle_create, user.id)
        battle = self.battle_repo.create(battle)

        # TODO Create end battle background task

        return battle

    @parse_as(BattleResponse, True)
    def end_battle(self, battle_id: str, battle_end: BattleEnd, user: User):
        battling = self.battle_repo.find_battling_by_user_id(user.id)
        battling = [i for i in battling if i.id == battle_id]
        if len(battling) == 0:
            raise ParamInvalidException(f"User is not in battle {battle_id}")

        self.battle_repo.end_battle(battle_id, battle_end)

    @parse_as(list[BattleResponse])
    def get_battle_history(self, user):
        return self.battle_repo.find_all_battle(user.id)


def generate_bot(self, character_id: str, user):
    character = self.character_service.get_character_by_id(character_id)

    if character is None:
        raise ValueError("Character not found")
    elif character.owner_id != user.id:
        raise ValueError("Character not belong to this user")

    bounce = 0.3

    attack = rd.randint(-int(character.attack * bounce), int(character.attack * bounce))
    defense = rd.randint(-int(character.defense * bounce), int(character.defense * bounce))
    energy = rd.randint(-int(character.energy * bounce), int(character.energy * bounce))

    character.attack += attack
    character.defense += defense
    character.energy += energy

    bot = character.dict(exclude={
        "id",
        "owner_id",
        "code",
        "root_character_id",
    })
    bot["owner_id"] = "bot"
    bot.update(rd.choice(self.r_character).dict(exclude={
        "id",
        "owner_id",
        "attack",
        "defense",
        "energy"
    }))

    return bot
