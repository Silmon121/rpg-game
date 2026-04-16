"""
Controller system unit tests.

Covers:
- Collision detection logic
- File loading system
- Player input translation
- GameController entity factory
- Map transformation system

These tests isolate controller logic using mocks
to avoid dependency on pygame runtime.
"""

import pytest

from controller.collision_controller import CollisionController
from controller.file_controller import FileController
from controller.player_controller import PlayerController
from controller.game_controller import GameController

from model.entities.objects.wall import Wall
from model.entities.objects.floor import Floor


# =========================================================
# COLLISION CONTROLLER TESTS
# =========================================================

def test_collision_within_bounds_allowed(monkeypatch):
    """Movement inside bounds should be allowed."""

    monkeypatch.setattr(
        "config.GRID_WIDTH",
        10,
        raising=False
    )
    monkeypatch.setattr(
        "config.GRID_HEIGHT",
        10,
        raising=False
    )

    class DummyGame:
        current_map = type("Map", (), {"grid": []})()

    import registry as reg
    reg.game = DummyGame()

    assert CollisionController.check_collision(5, 5) is True


def test_collision_out_of_bounds_x(monkeypatch):
    """Movement outside X bounds should be blocked."""

    monkeypatch.setattr("config.GRID_WIDTH", 10, raising=False)
    monkeypatch.setattr("config.GRID_HEIGHT", 10, raising=False)

    assert CollisionController.check_collision(999, 5) is False


def test_collision_out_of_bounds_y(monkeypatch):
    """Movement outside Y bounds should be blocked."""

    monkeypatch.setattr("config.GRID_WIDTH", 10, raising=False)
    monkeypatch.setattr("config.GRID_HEIGHT", 10, raising=False)

    assert CollisionController.check_collision(5, 999) is False


def test_collision_wall_block(monkeypatch):
    """Walls should block movement."""

    monkeypatch.setattr("config.GRID_WIDTH", 10, raising=False)
    monkeypatch.setattr("config.GRID_HEIGHT", 10, raising=False)

    wall = Wall(x=2, y=2)

    class DummyMap:
        grid = [[wall]]

    class DummyGame:
        current_map = DummyMap()

    import registry as reg
    reg.game = DummyGame()

    assert CollisionController.check_collision(2, 2) is False


# =========================================================
# FILE CONTROLLER TESTS
# =========================================================

def test_get_maps_json_type(monkeypatch):
    """FileController should return dict/list from JSON."""

    sample_data = {"1": {"id": 1, "grid": []}}

    def fake_open(*args, **kwargs):
        class FakeFile:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self):
                return ""

        return FakeFile()

    monkeypatch.setattr("builtins.open", lambda *a, **k: open)
    monkeypatch.setattr(
        "json.load",
        lambda f: sample_data
    )

    data = FileController.get_maps_json()
    assert isinstance(data, dict)


# =========================================================
# PLAYER CONTROLLER TESTS
# =========================================================

def test_player_controller_moves_w(monkeypatch):
    """W key should move player up."""

    import pygame
    import registry as reg

    class DummyPlayer:
        def __init__(self):
            self.x = 1
            self.y = 1
        def move(self, dx, dy):
            self.x += dx
            self.y += dy

    class DummyGame:
        player = DummyPlayer()

    reg.game = DummyGame()

    event = type("Event", (), {"key": pygame.K_w})

    PlayerController.handle_input(event)

    assert reg.game.player.x == 1
    assert reg.game.player.y == 0


def test_player_controller_moves_d(monkeypatch):
    """D key should move player right."""

    import pygame
    import registry as reg

    class DummyPlayer:
        def __init__(self):
            self.x = 1
            self.y = 1
        def move(self, dx, dy):
            self.x += dx
            self.y += dy

    class DummyGame:
        player = DummyPlayer()

    reg.game = DummyGame()

    event = type("Event", (), {"key": pygame.K_d})

    PlayerController.handle_input(event)

    assert reg.game.player.x == 2
    assert reg.game.player.y == 1


# =========================================================
# GAME CONTROLLER TESTS
# =========================================================

def test_game_controller_entity_factory():
    """GameController should create valid entities."""

    gc = GameController.__new__(GameController)
    gc.entities = []

    entity = gc.create_entity("player", name="Test")

    assert entity.name == "Test"
    assert entity in gc.entities


def test_game_controller_invalid_entity():
    """Unknown entity type should raise error."""

    gc = GameController.__new__(GameController)
    gc.entities = []

    with pytest.raises(ValueError):
        gc.create_entity("unknown")


# =========================================================
# MAP TRANSFORMATION TESTS
# =========================================================

def test_map_transform_wall_and_floor():
    """Map grid should convert strings to objects."""

    gc = GameController.__new__(GameController)
    gc.entities = []
    gc.player = None

    class DummyMap:
        grid = [
            ['1', '0']
        ]

    result = gc._GameController__transform_map(DummyMap())

    assert isinstance(result.grid[0][0], Wall)
    assert isinstance(result.grid[0][1], Floor)