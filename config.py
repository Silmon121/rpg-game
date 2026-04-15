"""
Config file where project constants are stored.
"""

# Game settings

GAME_TITLE = "RPG Game"
"""Title of the game."""
FPS = 60
"""Frame rate of the game."""

# Grid settings

TILE_SIZE = 64
"""Size of one tile of a grid."""

GRID_WIDTH = 15
"""Amount of tiles in 'x' axis."""

GRID_HEIGHT = 10
"""Amount of tiles in 'y' axis."""

SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
"""Total screen width in pixels."""

SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT
"""Total screen height in pixels."""

# Colors (RGB)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Sprite paths

WOODEN_WALL_SPRITE = "assets/images/walls/wooden_wall.png"
WOODEN_FLOOR_SPRITE = "assets/images/floors/wood_floor.png"
PLAYER_SPRITE = "assets/images/player/player.png"
