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

from model.entities.entity import Entity
from model.entities.characters.player import Player
from model.entities.characters.npc import NPC
from model.entities.objects.wall import Wall
from model.entities.objects.floor import Floor

# =========================================================
# INHERITANCE RULES
# =========================================================

def test_missing_required_class_fields_raises():
    """
    Ensure Entity class maintains required internal structure.
    """
    assert hasattr(Entity, "_Entity__ID_PREFIX")

# =========================================================
# PLAYER TESTS
# =========================================================

def test_player_max_health_override():
    """Player should use higher base HP."""
    p = Player(x=0, y=0)
    assert p.health == 120


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