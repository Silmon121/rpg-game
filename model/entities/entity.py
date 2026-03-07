class Entity:
    _max_hp = 100
    _name = "Entity"
    def __init__(self, name):
        self.__hp = self._max_hp
    def __str__(self):
        return f"{self._name}"

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        raise ValueError("Name can't be changed")