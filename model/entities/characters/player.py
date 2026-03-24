from model.entities.characters.character import Character

class Player(Character):
    __ID_PREFIX = "P"
    __EXPECTED_PARAMETERS: dict[str, type] = {

    }
    _max_health = 120
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def __str__(self):
        return f"Player\nName: {self._name}\nHP: {self._hp}\n"
    def __init_subclass__(cls):
        super().__init_subclass__()
