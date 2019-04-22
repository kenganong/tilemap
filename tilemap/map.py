class Map:
  def __init__(self):
    self.properties = {}
    self.tracking = {}
  def _require_coor(self, coor):
    if not self.exists(coor):
      raise IndexError('Coordinate {} outside tilemap bounds'.format(coor))
  def _shift_coor(self, coor, shift):
    return (coor[0] + shift[0], coor[1] + shift[1])
  def exists(self, coor):
    """Detects whether the given coordinate exists in the map

    Args:
      coor (tuple): the coordinate of the tile

    Returns:
      true or false, whether a tile with the given coordinate exists
    """
    raise NotImplementedError('Exists not yet implemented')
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
    if coor in self.tracking:
      name = self.tracking[coor]
      self.properties[name] = None
      del self.tracking[coor]
    return previous_content
  def tiles(self):
    """Traverses the map, getting all tiles within

    Returns:
      generator of (coor, content) tuples for all tiles
    """
    for coor in self.tile_coors():
      yield (coor, self._get(coor))
  def sides(self):
    """Gets the tiles on the edges of the map.
    A tile is on the side if at least one its borders is out-of-bounds.

    Returns:
      generator of (coor, content) tuples for all side tiles
    """
    for coor in self.side_coors():
      yield (coor, self._get(coor))
  def adjacent(self, coor):
    """Gets the tiles adjacent to the given coordinate

    Args:
      coor (tuple): the coordinate of the tile

    Returns:
      generator of (coor, content) tuples for all adjacent tiles

    Raises:
      IndexError when the given coordinate is outside the map
    """
    self._require_coor(coor)
    for _, direction in self.direction_map.items():
      new_coor = self._shift_coor(coor, direction)
      if self.exists(new_coor):
        yield (new_coor, self._get(new_coor))
  def track(self, coor, name):
    """Start tracking the given coordinate using the given name.
    A new property will be added to the map.properties dict with name as its key and coor as its value.
    Whenever the content starting at coor moves, the property will be updated with its new coordinate.
    If the content starting at coor is overwritten or removed from the map, the property will be set to None.

    Args:
      coor (tuple): the current coordinate for the content to track
      name (str): the name to give the tracking property in the map.properties dict

    Raises:
      IndexError when the given coordinate is outside the map
    """
    self._require_coor(coor)
    self.properties[name] = coor
    self.tracking[coor] = name
  def move(self, start_coor, end_coor):
    """Moves the contents of the given start coordinate to the given end coordinate.
    Fills the start coordinate with empty and overwrites the contens of end coordinate.

    Args: 
      start_coor (tuple): the coordinate from which to move
      end_coor (tuple): the coordinate to which to move

    Returns:
      prior tile contents of end coordinate

    Raises:
      IndexError when either coordinate is outside the map
    """
    self._require_coor(start_coor)
    self._require_coor(end_coor)
    content = self._get(start_coor)
    self._set(start_coor, None)
    removed_content = self._get(end_coor)
    self._set(end_coor, content)
    if end_coor in self.tracking:
      name = self.tracking[end_coor]
      self.properties[name] = None
      del self.tracking[end_coor]
    if start_coor in self.tracking:
      name = self.tracking[start_coor]
      self.properties[name] = end_coor
      del self.tracking[start_coor]
      self.tracking[end_coor] = name
    return removed_content
  def swap(self, first_coor, second_coor):
    """Moves the contents of the given first coordinate to the given second coordinate and vice versa.

    Args:
      first_coor (tuple): content located at this coordinate moves to second_coor
      second_coor (tuple): content located at this coordinate moves to first_coor

    Raises:
      IndexError when either coordinate is outside the map
    """
    track = False
    if second_coor in self.tracking:
      track = True
      name = self.tracking[second_coor]
    content = self.move(first_coor, second_coor)
    self._set(first_coor, content) 
    if track:
      self.properties[name] = first_coor
      self.tracking[first_coor] = name
