from controller import GameController

game = GameController()

# game
game.create_entity(e_name="player", name="Hans", x=0, y=0)

game.run()
