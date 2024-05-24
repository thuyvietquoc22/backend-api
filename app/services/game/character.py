from app.decorator import singleton
from app.decorator.parser import parse_as
from app.entity.game.character import CharacterCreate
from app.entity.game.user import User
from app.exceptions.not_found_exception import NotFoundException
from app.repositories.character_repository import CharacterRepository
from app.services.game.root_character import RootCharacterService


@singleton
class CharacterService:

    def __init__(self):
        self.character_repo = CharacterRepository()

        self.r_character_service = RootCharacterService()

    @parse_as(CharacterCreate, get_first=True)
    def create_character_for_user(self, user: User, root_character_id: str):
        # Validate user, root_character_id
        r_character = self.r_character_service.get_root_character_by_id(root_character_id)
        if r_character is None:
            raise NotFoundException("Root character not found")

        character = CharacterCreate.from_root_character(r_character, str(user.id))

        return self.character_repo.create(character)
