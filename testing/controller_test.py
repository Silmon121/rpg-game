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

import pygame
import pytest
import json
import io
from controller.collision_controller import CollisionController
from controller.file_controller import FileController
from controller.game_controller import GameController
from model import Map
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

    assert CollisionController.check_collision(type[CollisionController], new_x=5, new_y=5) is True


def test_collision_out_of_bounds_x(monkeypatch):
    """Movement outside X bounds should be blocked."""

    monkeypatch.setattr("config.GRID_WIDTH", 10, raising=False)
    monkeypatch.setattr("config.GRID_HEIGHT", 10, raising=False)

    assert CollisionController.check_collision(type[CollisionController], new_x=999, new_y=5) is False


def test_collision_out_of_bounds_y(monkeypatch):
    """Movement outside Y bounds should be blocked."""

    monkeypatch.setattr("config.GRID_WIDTH", 10, raising=False)
    monkeypatch.setattr("config.GRID_HEIGHT", 10, raising=False)

    assert CollisionController.check_collision(type[CollisionController], new_x=5, new_y=999) is False


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

    assert CollisionController.check_collision(type[CollisionController], new_x=2, new_y=2) is False


# =========================================================
# FILE CONTROLLER TESTS
# =========================================================

def test_get_maps_json_type(monkeypatch):
    """FileController should return dict/list from JSON."""

    sample_data = {"1": {"id": 1, "grid": []}}

    fake_json = json.dumps(sample_data)

    def fake_open(*args, **kwargs):
        return io.StringIO(fake_json)

    monkeypatch.setattr("builtins.open", fake_open)

    data = FileController.get_maps_json()

    assert isinstance(data, dict)
    assert data == sample_data


# =========================================================
# PLAYER CONTROLLER TESTS
# =========================================================

from controller.player_controller import PlayerController


class DummyPlayer:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.sword_attack = False
        self.face_direction = (0, -1)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class DummyGC:
    def __init__(self):
        self.player = DummyPlayer()
        self.entities = []
        self.cc = type("CC", (), {"check_entity_collision": lambda *a, **k: None})()

        def create_entity(*args, **kwargs):
            class DummySword:
                def __init__(self):
                    self.id = "SW-1"
                    self.x = kwargs.get("x", 0)
                    self.y = kwargs.get("y", 0)
                    self.ready = True

            sword = DummySword()
            self.entities.append(sword)
            return sword

        self.create_entity = create_entity

        def restart_level():
            self.restarted = True

        self.restart_level = restart_level


# ---------------------------------------------------------
# MOVEMENT TESTS
# ---------------------------------------------------------

def test_player_controller_moves_w():
    gc = DummyGC()
    pc = PlayerController(gc)

    event = type("Event", (), {"key": pygame.K_w})()

    pc.handle_input(event)

    assert gc.player.x == 1
    assert gc.player.y == 0


def test_player_controller_moves_d():
    gc = DummyGC()
    pc = PlayerController(gc)

    event = type("Event", (), {"key": pygame.K_d})()

    pc.handle_input(event)

    assert gc.player.x == 2
    assert gc.player.y == 1


# ---------------------------------------------------------
# SWORD ATTACK TEST
# ---------------------------------------------------------

def test_player_controller_sword_attack_creates_entity():
    gc = DummyGC()
    pc = PlayerController(gc)

    event = type("Event", (), {"key": pygame.K_SPACE})()

    pc.handle_input(event)

    assert gc.player.sword_attack is True
    assert len(gc.entities) == 1
    assert gc.entities[0].id.startswith("SW")


# ---------------------------------------------------------
# PLAYER STATUS TEST
# ---------------------------------------------------------

def test_player_controller_restart_on_death():
    gc = DummyGC()
    pc = PlayerController(gc)

    gc.player.health = 0

    pc.check_player_status(dt=0.1)

    assert hasattr(gc, "restarted")
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

    result = gc._transform_map(Map(id=-100, grid=['1', '0']))

    assert isinstance(result.grid[0][0], Wall)
    assert isinstance(result.grid[0][1], Floor)