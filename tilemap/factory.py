def create_line_map(length):
  return LineMap(length)

class LineMap:
  def __init__(self, size):
    self.tiles = [None for _ in range(size)]
  def get(self, coor):
    if coor < 0 or coor > len(self.tiles):
      raise IndexError('Coordinate {} outside tilemap bounds'.format(coor))
    return self.tiles[coor]
  def set(self, coor, content):
    if coor < 0 or coor > len(self.tiles):
      raise IndexError('Coordinate {} outside tilemap bounds'.format(coor))
    self.tiles[coor] = content
