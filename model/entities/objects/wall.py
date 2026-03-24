from model.entities.entity import Entity

class Wall(Entity):
    __ID_PREFIX: str = "W"
    __EXPECTED_PARAMETERS: dict[str, type] = {

    }
    __COLOR = (0, 255, 0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
