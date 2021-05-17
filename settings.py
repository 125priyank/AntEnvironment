from math import sqrt, ceil, floor
TILE_SIZE = 30
GRID_WIDTH = 25
GRID_HEIGHT = 25
WIN_WIDTH = TILE_SIZE*GRID_WIDTH
WIN_HEIGHT = TILE_SIZE*GRID_HEIGHT

slopes = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

possible_directions = {
    'u': 0, 'd': 1, 'l': 2, 'r': 3, 'ur': 4, 'ul': 5, 'dr': 6, 'dl': 7, 's': 8, 
    0: 'u', 1: 'd', 2: 'l', 3: 'r', 4:'ur', 5: 'ul', 6: 'dr', 7: 'dl', 8: 's'
}
moves = {
  'u': (0, 1),
  'd': (0, -1),
  'l': (-1, 0),
  'r': (1, 0),
  'ur': (1, 1),
  'ul': (-1, 1),
  'dr': (1, -1),
  'dl': (-1, -1),
  's': (0, 0)
}

offspring_energy_required = 1000

def manhattan_distance(v1, v2):
    return abs(v1.x-v2.x) + abs(v1.y-v2.y)

def euclidean_distance(v1, v2):
    return sqrt(pow(v1.x-v2.x, 2) + pow(v1.y-v2.y, 2))

def box_distance(v1, v2):
    dist = sqrt(pow(v1.x-v2.x, 2) + pow(v1.y-v2.y, 2))
    # in a line box
    if ceil(dist) == floor(dist):
        return dist
    
    # diagonal box
    else:
        return dist/sqrt(2)


def in_grid(x, y):
  return x>=0 and y>=0 and x < GRID_WIDTH and y < GRID_HEIGHT