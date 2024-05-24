import random as rd

from loguru import logger

from app.decorator import singleton
from app.decorator.parser import parse_as
from app.entity.game.character import CharacterCreate, Character, CharacterResponse, CharacterUpdate
from app.entity.game.stone import Stone, StoneColor
from app.entity.game.user import User
from app.exceptions.not_found_exception import NotFoundException
from app.repositories.character_repository import CharacterRepository
from app.services.game.root_character import RootCharacterService
from app.services.game.user import UserService
from app.utils import calculate_ratio_upgrading


@singleton
class CharacterService:

    def __init__(self):
        self.character_repo = CharacterRepository()

        self.r_character_service = RootCharacterService()
        self.user_service = UserService()

    @parse_as(CharacterResponse, get_first=True)
    def create_character_for_user(self, user: User, root_character_id: str):
        # Validate user, root_character_id
        r_character = self.r_character_service.get_root_character_by_id(root_character_id)
        if r_character is None:
            raise NotFoundException("Root character not found")

        character = CharacterCreate.from_root_character(r_character, str(user.id))

        return self.character_repo.create(character)

    @parse_as(Character, get_first=True)
    def get_character_by_id(self, character_id: str):
        return self.character_repo.get_by_id(character_id)

    def upgrade_character(self, user: User, stones: list[Stone], character_id: str):

        if stones is None or len(stones) == 0:
            raise ValueError("Stones must not be empty")

        character = self.get_character_by_id(character_id)
        if character is None:
            raise NotFoundException("Character not found")

        if character.owner_id != user.id:
            raise ValueError("Character not belong to this user")

        stone_color = stones[0].color
        count_stone = 0
        # Check stones greater than 0 and same color
        for stone in stones:
            if stone.amount <= 0:
                raise ValueError("Stone amount must be greater than 0")

            if stone.color != stone_color:
                raise ValueError("All stones must have the same color")

            count_stone += stone.convert_to_level_1().amount

        # Update bag
        self.user_service.consume_stone(set(stones), user)

        current_stat = character.get_current_stats(stone_color)
        ratio_per_1 = calculate_ratio_upgrading(current_stat)

        ratio_success = ratio_per_1 * count_stone
        ratio_fail = 0 if ratio_success > 100 else (100 - ratio_success)

        value = rd.choices([True, False], [ratio_success, ratio_fail])[0]

        logger.info(
            f"User: {user.id}, Character: {character.id}, ratio_per_1: {ratio_per_1}, ratio_success: {ratio_success}, result: {value}")

        if value is False:
            return False

        self.update_character_stat(character, stone_color)

        return True

    def update_character_stat(self, character: Character, stone_color: StoneColor):
        update_data = CharacterUpdate()

        if stone_color == 'red':
            update_data.attack = character.attack + 1
        elif stone_color == 'green':
            update_data.defense = character.defense + 1
        elif stone_color == 'blue':
            update_data.energy = character.energy + 1
        else:
            raise ValueError("Invalid stone color")

        self.character_repo.update(character.id, update_data)
        return character
