from bson import ObjectId

from app.entity.game.character import CharacterCreate
from app.entity.game.root_character import RootCharacter


class TestCharacter:
    @staticmethod
    def test_from_root_character():
        root_id = ObjectId()
        root_character = RootCharacter(
            id=root_id,
            url_model="https://www.google.com",
            name="root_character",
            attack=100,
            defense=100,
            energy=100,
        )

        owner = ObjectId()

        response = CharacterCreate.from_root_character(root_character, owner_id=str(owner))

        assert response.owner_id == str(owner)
        assert len(response.code) == 7
        assert response.attack == 100
        assert response.defense == 100
        assert response.energy == 100
        assert response.root_character_id == str(root_id)
