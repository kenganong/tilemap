from tilemap.constants import *

def create_line_map(length):
  return LineMap(length)
def create_rectangle_map(width, height):
  return RectRectMap(width, height)
def create_rectangle_hex_map(width, height):
  return RectHexMap(width, height)

class Map:
  def _require_coor(self, coor):
    if not self.exists(coor):
      raise IndexError('Coordinate {} outside tilemap bounds'.format(coor))
  def _shift_coor(self, coor, shift):
    return (coor[0] + shift[0], coor[1] + shift[1])
  def get(self, coor):
    """Gets the content of the tile at the given coordinate

    Args:
      coor (tuple): the coordinate of the tile

    Returns:
      tile contents

    Raises:
      IndexError when the given coordinate is outside the map
    """
    self._require_coor(coor)
    return self._get(coor)
  def set(self, coor, content):
    """Sets the content of the tile at the given coordinate

    Args:
      coor (tuple): the coordinate of the tile
      content: desired tile content

    Returns:
      prior tile contents

    Raises:
      IndexError when the given coordinate is outside the map
    """
    self._require_coor(coor)
    previous_content = self._get(coor)
    self._set(coor, content)
    return previous_content
  def adjacent(self, coor):
    """Gets the tiles adjacent to the given coordinate
    """
    self._require_coor(coor)
    for _, direction in self.direction_map.items():
      new_coor = self._shift_coor(coor, direction)
      if self.exists(new_coor):
        yield (new_coor, self._get(new_coor))

class LineMap(Map):
  def __init__(self, size):
    self.tiles = [None for _ in range(size)]
    self.direction_map = SLOT_DIRECTION_MAP
  def exists(self, coor):
    return coor > -1 and coor < len(self.tiles)
  def _shift_coor(self, coor, shift):
    return coor + shift
  def _get(self, coor):
    # internal get assumes that coor is valid
    return self.tiles[coor]
  def _set(self, coor, content):
    # internal set assumes that coor is valid
    self.tiles[coor] = content

class RectRectMap(Map):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.cols = []
    for _ in range(width):
      self.cols.append([None for _ in range(height)])
    self.direction_map = RECT_DIRECTION_MAP
  def exists(self, coor):
    x, y = coor
    return x > -1 and x < self.width and y > -1 and y < self.height
  def _get(self, coor):
    # internal get assumes that coor is valid
    x, y = coor
    return self.cols[x][y]
  def _set(self, coor, content):
    # internal set assumes that coor is valid
    x, y = coor
    self.cols[x][y] = content

class RectHexMap(Map):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.tiles = []
    for _ in range(height):
      self.tiles.append([None for _ in range(width)])
    self.direction_map = HEX_DIRECTION_MAP
  def exists(self, coor):
    q, r = coor
    row_offset = (r + 1) // 2
    return r > -1 and r < self.height and q > -1 - row_offset and q < self.width - row_offset
  def _get(self, coor):
    q, r = coor
    row_offset = (r + 1) // 2
    return self.tiles[r][q + row_offset]
  def _set(self, coor, content):
    q, r = coor
    row_offset = (r + 1) // 2
    self.tiles[r][q + row_offset] = content
