from chat_core.trainer import FAISSHelper
from decorator import singleton

train_data = [
    {
        "glob": "Azusa Nakano.pdf",
        "character_name": "azura_nakano"
    },
    {
        "glob": "edge runner lucy.pdf",
        "character_name": "edge_runner_lucy"
    },
    {
        "glob": "Sakura.pdf",
        "character_name": "sakura"
    },
]


# faiss_indexes = {i['character_name']: FAISSHelper.load_data(i['character_name']) for i in train_data}


@singleton
class FAISSService:
    @classmethod
    def get_index(cls, character_name):
        return FAISSHelper.load_data(character_name)
