from app.decorator import singleton
from app.decorator.parser import parse_as
from app.entity.game.root_character import RootCharacterCreate, RootCharacter, RootCharacterUpdate
from app.repositories.root_character import RootCharacterRepository


@singleton
class RootCharacterService:

    def __init__(self):
        self.r_character_repo = RootCharacterRepository()

    @parse_as(RootCharacter, True)
    def get_root_character_by_id(self, root_character_id):
        return self.r_character_repo.get_by_id(root_character_id)

    @parse_as(list[RootCharacter])
    def get_root_characters(self):
        return self.r_character_repo.get_all()

    @parse_as(RootCharacter, True)
    def create_root_character(self, root_character: RootCharacterCreate):
        return self.r_character_repo.create(root_character)

    @parse_as(RootCharacter, True)
    def update_root_character(self, update_id: str, root_character: RootCharacterUpdate):
        return self.r_character_repo.update(update_id, root_character)
