from model.entities.entity import Entity

class Floor(Entity):
    __ID_PREFIX: str = "F"
    __EXPECTED_PARAMETERS: dict[str, type] = {

    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)