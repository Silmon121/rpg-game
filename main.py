from controller import GameController as gc

player = gc.create_player("Hans")
player2 = gc.create_player("Hans2")

print(player)

print(repr(player))
print(repr(player2))