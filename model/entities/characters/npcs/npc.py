from model.entities.characters.character import Character

class NPC(Character):

    __ID_PREFIX = "NPC"
    __EXPECTED_PARAMETERS: dict[str, type] = {
        "agro": bool
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agro = kwargs.get("agro", False)


