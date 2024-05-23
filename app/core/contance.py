from enum import Enum


class CharacterName(Enum):
    _2B = "2B"
    AZUSA_NAKANO = "Azusa Nakano"
    EDGE_RUNNER_LUCY = "Edge Runner Lucy"
    SAKURA = "Sakura"

    @property
    def character_name(self):
        return self.name.lower().replace(" ", "_")


class Experience(Enum):
    LEVEL_1: int = 1.5
    LEVEL_35: int = 347
    LEVEL_70: int = 1306
    LEVEL_100: int = 2615

    @property
    def range_1_35(self):
        return range(int(self.LEVEL_1.value), int(self.LEVEL_35.value))

    @property
    def range_35_70(self):
        return range(int(self.LEVEL_35.value), int(self.LEVEL_70.value))

    @property
    def range_70_100(self):
        return range(int(self.LEVEL_70.value), int(self.LEVEL_100.value))
