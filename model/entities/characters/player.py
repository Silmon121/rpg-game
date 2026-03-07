from model import Character


class Player(Character):
    __id_prefix = "P"
    _max_health = 120
    def __init__(self, name:str):
        super().__init__(name)
    def __str__(self):
        return f"Player\nName: {self._name}\nHP: {self._hp}\n"

    def move(self):
        pass
    def attack(self):
        pass