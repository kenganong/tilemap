from .context import tilemap
from tilemap import factory
import pytest

class GamePiece:
  def __init__(self, name, color):
    self.name = name
    self.color = color

@pytest.fixture
def empty_map():
  return factory.create_line_map(8)

@pytest.fixture
def simple_map(empty_map):
  empty_map.set(2, GamePiece('pawn', 'black'))
  empty_map.set(5, GamePiece('bishop', 'white'))
  return empty_map

def test_get(simple_map):
  assert None == simple_map.get(0)
  assert 'pawn' == simple_map.get(2).name
  assert 'bishop' == simple_map.get(5).name
  assert None == simple_map.get(7)

def test_get_out_of_bounds(empty_map):
  with pytest.raises(IndexError):
    empty_map.get(8)
  with pytest.raises(IndexError):
    empty_map.get(-1)
  empty_map.get(0)
  empty_map.get(7)

def test_set(empty_map):
  empty_map.set(1, GamePiece('meeple', 'blue'))
  assert None == empty_map.get(0)
  assert None != empty_map.get(1)
  assert 'meeple' == empty_map.get(1).name

def test_set_out_of_bounds(empty_map):
  with pytest.raises(IndexError):
    empty_map.set(8, GamePiece('meeple', 'yellow'))
  with pytest.raises(IndexError):
    empty_map.set(-1, GamePiece('pawn', 'black'))
  with pytest.raises(IndexError):
    empty_map.set(-3, GamePiece('bishop', 'white'))
  # No errors
  empty_map.set(0, GamePiece('cube', 'brown'))
  empty_map.set(7, GamePiece('road', 'blue'))
