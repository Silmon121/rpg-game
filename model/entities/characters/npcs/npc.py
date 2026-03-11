from model import Character

class NPC(Character):

    __ID_PREFIX = "NPC"
    __expected_parameters = {
        "agro": bool
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agro = kwargs.get("agro", False)


