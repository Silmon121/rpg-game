from controller import GameController as gc

player = gc.create_player(name="Hans", hp=30)
player2 = gc.create_player(name="Simon", hp=50)

print(player)

print(repr(player))
print(repr(player2))