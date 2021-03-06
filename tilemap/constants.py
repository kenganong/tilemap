NORTH = 0
NORTHEAST = 1
EAST = 2
SOUTHEAST = 3
SOUTH = 4
SOUTHWEST = 5
WEST = 6
NORTHWEST = 7

LEFT = WEST
RIGHT = EAST
NE = NORTHEAST
NW = NORTHWEST
SE = SOUTHEAST
SW = SOUTHWEST


SLOT_DIRECTION_MAP = {LEFT: -1, RIGHT: 1}
RECT_DIRECTION_MAP = {NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)}
HEX_DIRECTION_MAP = {NE: (1, -1), EAST: (1, 0), SE: (0, 1), SW: (-1, 1), WEST: (-1, 0), NW: (0, -1)}
