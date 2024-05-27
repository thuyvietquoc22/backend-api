import random as rd

from app.decorator import singleton
from app.repositories.battle import BattleRepository
from app.services.game.character import CharacterService
from app.services.game.root_character import RootCharacterService


@singleton
class BattleService:
    def __init__(self):
        self.battle_repo = BattleRepository()
        self.character_service = CharacterService()
        self.r_character = RootCharacterService().get_root_characters()

    def start_battle(self):
        pass

    def end_battle(self):
        pass

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
