from enum import Enum


# [
#     {
#         "glob": "Azusa Nakano.pdf",
#         "character_name": "azura_nakano"
#     },
#     {
#         "glob": "edge runner lucy.pdf",
#         "character_name": "edge_runner_lucy"
#     },
#     {
#         "glob": "Sakura.pdf",
#         "character_name": "sakura"
#     },
# ]
class CharacterName(Enum):
    AZUSA_NAKANO = "Azusa Nakano"
    EDGE_RUNNER_LUCY = "Edge Runner Lucy"
    SAKURA = "Sakura"

    @property
    def character_name(self):
        return self.name.lower().replace(" ", "_")


print(CharacterName.AZUSA_NAKANO.character_name)
