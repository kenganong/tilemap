from tilemap.constants import *
from tilemap.map import Map

def create_line_map(length):
  return LineMap(length)
def create_rectangle_map(width, height):
  return RectRectMap(width, height)
def create_rectangle_hex_map(width, height):
  return RectHexMap(width, height)

class LineMap(Map):
  def __init__(self, size):
    super().__init__()
    self.slots = [None for _ in range(size)]
    self.direction_map = SLOT_DIRECTION_MAP
  def exists(self, coor):
    return coor > -1 and coor < len(self.slots)
  def _shift_coor(self, coor, shift):
    return coor + shift
  def _get(self, coor):
    # internal get assumes that coor is valid
    return self.slots[coor]
  def _set(self, coor, content):
    # internal set assumes that coor is valid
    self.slots[coor] = content
  def tile_coors(self):
    for i in range(len(self.slots)):
      yield i
  def side_coors(self):
    if len(self.slots) < 3:
      yield from self.tile_coors()
      return
    yield 0
    yield len(self.slots) - 1

class RectRectMap(Map):
  def __init__(self, width, height):
    super().__init__()
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
  def tile_coors(self):
    for x in range(self.width):
      for y in range(self.height):
        yield (x, y)
  def side_coors(self):
    if self.width < 3 or self.height < 3:
      yield from self.tile_coors()
      return
    for x in range(self.width):
      yield (x, 0)
      yield (x, self.height - 1)
    for y in range(1, self.height - 1):
      yield (0, y)
      yield (self.width - 1, y)

class RectHexMap(Map):
  def __init__(self, width, height):
    super().__init__()
    self.width = width
    self.height = height
    self._tiles = []
    for _ in range(height):
      self._tiles.append([None for _ in range(width)])
    self.direction_map = HEX_DIRECTION_MAP
  def _row_offset(self, row):
    return (row + 1) // 2
  def exists(self, coor):
    q, r = coor
    row_offset = self._row_offset(r)
    return r > -1 and r < self.height and q > -1 - row_offset and q < self.width - row_offset
  def _get(self, coor):
    q, r = coor
    row_offset = self._row_offset(r)
    return self._tiles[r][q + row_offset]
  def _set(self, coor, content):
    q, r = coor
    row_offset = self._row_offset(r)
    self._tiles[r][q + row_offset] = content
  def tile_coors(self):
    for r in range(self.height):
      row_offset = self._row_offset(r)
      for q in range(-row_offset, self.width - row_offset):
        yield (q, r)
  def side_coors(self):
    if self.width < 3 or self.height < 3:
      yield from self.tile_coors()
      return
    for x in range(self.width):
      yield (x, 0)
      r = self.height - 1
      yield (x - self._row_offset(r), r)
    for r in range(1, self.height - 1):
      row_offset = self._row_offset(r)
      yield (-row_offset, r)
      yield (self.width - row_offset - 1, r)
