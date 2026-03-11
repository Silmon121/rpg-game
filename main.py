from controller import GameController

game = GameController()

# game
player = game.create_player(name="Hans")

print(player)
print(repr(player))
