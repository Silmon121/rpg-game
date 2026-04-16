"""
Entity system unit tests.

Covers:
- Base Entity behavior (validation, IDs, position system)
- Character system (HP, stats, immortality)
- Player and NPC specializations
- MovableEntity movement logic (with mocked collision)
- Object entities (Wall, Floor)

These tests ensure correctness of:
- inheritance system
- runtime validation logic
- core gameplay entity mechanics
"""

import pytest

from model.entities.entity import Entity
from model.entities.characters.character import Character
from model.entities.characters.player import Player
from model.entities.characters.npc import NPC
from model.entities.movable_entity import MovableEntity
from model.entities.objects.wall import Wall
from model.entities.objects.floor import Floor


# =========================================================
# ENTITY BASE TESTS
# =========================================================

def test_entity_creation_with_position():
    """Entity should correctly store position and name."""
    e = Entity(x=5, y=10, name="Test")
    assert e.x == 5
    assert e.y == 10
    assert e.name == "Test"


def test_entity_default_name():
    """Entity should default name to class name."""
    e = Entity(x=1, y=2)
    assert e.name == "Entity"


def test_entity_negative_x_raises():
    """Negative X should raise ValueError."""
    with pytest.raises(ValueError):
        Entity(x=-1, y=2)


def test_entity_negative_y_raises():
    """Negative Y should raise ValueError."""
    with pytest.raises(ValueError):
        Entity(x=1, y=-2)


def test_position_property_valid():
    """Position property should return [x, y]."""
    e = Entity(x=3, y=4)
    assert e.position == [3, 4]


def test_position_missing_raises():
    """Accessing incomplete position should raise ValueError."""
    e = Entity()
    with pytest.raises(ValueError):
        _ = e.position


def test_entity_id_is_string():
    """Entity ID must be a string."""
    e = Entity(x=1, y=1)
    assert isinstance(e.id, str)


def test_entity_id_format():
    """Entity ID should contain prefix marker."""
    e = Entity(x=1, y=1)
    assert "E" in e.id


def test_entity_ids_increment():
    """Each entity must have a unique ID."""
    e1 = Entity(x=1, y=1)
    e2 = Entity(x=1, y=1)
    assert e1.id != e2.id


def test_invalid_parameter_key():
    """Unknown parameter should raise ValueError."""
    with pytest.raises(ValueError):
        Entity(x=1, y=1, invalid=123)


def test_invalid_parameter_type():
    """Wrong parameter type should raise ValueError."""
    with pytest.raises(ValueError):
        Entity(x="wrong", y=1)


# =========================================================
# INHERITANCE RULES
# =========================================================

def test_missing_required_class_fields_raises():
    """
    Ensure Entity class maintains required internal structure.
    """
    assert hasattr(Entity, "_Entity__ID_PREFIX")


# =========================================================
# CHARACTER TESTS
# =========================================================

def test_character_hp_default():
    """Character should default HP to 100."""
    c = Character(x=0, y=0)
    assert c.hp == 100


def test_character_hp_custom():
    """Character should accept custom HP."""
    c = Character(x=0, y=0, hp=50)
    assert c.hp == 50


def test_character_stats():
    """Character should store strength and intelligence."""
    c = Character(
        x=0, y=0,
        strength=10,
        intelligence=20
    )
    assert c.strength == 10
    assert c.intelligence == 20


def test_character_immortal_flag():
    """Character should store immortality flag."""
    c = Character(x=0, y=0, immortal=True)
    assert c.is_immortal is True


# =========================================================
# PLAYER TESTS
# =========================================================

def test_player_max_health_override():
    """Player should use higher base HP."""
    p = Player(x=0, y=0)
    assert p.hp == 120


def test_player_string_output():
    """Player __str__ should return readable output."""
    p = Player(x=1, y=2)
    s = str(p)
    assert "Player" in s


# =========================================================
# NPC TESTS
# =========================================================

def test_npc_agro_default():
    """NPC should default agro to False."""
    n = NPC(x=0, y=0)
    assert n.agro is False


def test_npc_agro_true():
    """NPC should accept agro=True."""
    n = NPC(x=0, y=0, agro=True)
    assert n.agro is True


# =========================================================
# MOVABLE ENTITY TESTS
# =========================================================

def test_movable_entity_move_updates_position():
    """Movement should update position when allowed."""

    class DummyCollision:
        def check_collision(self, x, y):
            return True  # allow movement

    import registry as reg
    reg.game = type("Game", (), {})()
    reg.game.cc = DummyCollision()

    m = MovableEntity(x=1, y=1)
    m.move(1, 1)

    assert m.x == 2
    assert m.y == 2


def test_movable_entity_blocked_move():
    """Movement should not update position when blocked."""

    class DummyCollision:
        def check_collision(self, x, y):
            return False  # block movement

    import registry as reg
    reg.game = type("Game", (), {})()
    reg.game.cc = DummyCollision()

    m = MovableEntity(x=1, y=1)
    m.move(1, 1)

    assert m.x == 1
    assert m.y == 1


# =========================================================
# OBJECT TESTS
# =========================================================

def test_wall_creation():
    """Wall should store correct coordinates."""
    w = Wall(x=1, y=1)
    assert w.x == 1
    assert w.y == 1


def test_floor_creation():
    """Floor should store correct coordinates."""
    f = Floor(x=2, y=2)
    assert f.x == 2
    assert f.y == 2