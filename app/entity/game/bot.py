from pydantic import Field

from app.entity.game.root_character import CharacterAttribute


class BotInfo(CharacterAttribute):
    url_model: str
    remaining_hp: int = Field(default=100, ge=0, le=100)
