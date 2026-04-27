"""Config file where project constants are stored."""

# Game settings

#: Title of the game.
GAME_TITLE = "RPG Game"
#: Frame rate of the game.
FPS = 60

# Grid settings

#: Size of one tile of a grid.
TILE_SIZE = 64

#: Amount of tiles in 'x' axis.
GRID_WIDTH = 15

#: Amount of tiles in 'y' axis.
GRID_HEIGHT = 10

#: Total screen width in pixels.
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH

#: Total screen height in pixels.
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

# Colors (RGB)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Sprite paths

WOODEN_WALL_SPRITE = "assets/images/walls/wooden_wall.png"
WOODEN_FLOOR_SPRITE = "assets/images/floors/wood_floor.png"
PLAYER_SPRITE = "assets/images/player/player.png"
LIGHT_ELF_SPRITE = "assets/images/enemies/light_elf.png"
GOAL_DOOR_SPRITE = "assets/images/goal/goal_door.png"
GOAL_DOOR_LOCKED_SPRITE = "assets/images/goal/goal_door_locked.png"
SWORD_SPRITE = "assets/images/weapons/sword.png"
