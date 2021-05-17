from settings import *
from Vector import *
from math import ceil, floor
import operator
import random
import pygame
import copy

class Ant:
    # def __init__(self, dna, food, vector, create_timestamp, end_timestamp, parent=None):
    def __init__(self, dna, food, vector, parent=None):
        self.dna = copy.deepcopy(dna)
        # self._decision_brain = dna['decision_brain']
        # self.movement_brain = dna['movement_brain']
        # self.offsprint_brain = dna['offspring_brain']
        # direction = [up, up-right, right, right-down, down, down-left, left, left-up]
        self.direction_move = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        self.vector = vector
        self.food = food
        self.direction = 0
        self.parent = parent
        # self.create_timestamp = create_timestamp
        # self.end_timestamp = end_timestamp

        self.dna['energy'] = 1000
        self.dna['vision_mask'] = self.dna['vision_mask']
        self.dna['vision_distance'] = self.dna['vision_distance']
        self.dna['offspring_range'] = self.dna['offspring_range']
        self.dna['velocity'] = self.dna['velocity']

    def mutate(self, ant):
        ant.dna['vision_mask'][random.randrange(0, 8)] ^= 1
        ant.dna['vision_distance'] = max(1, ant.dna['vision_distance'] + random.randint(-1, 1))
        ant.dna['offspring_range'] = ant.dna['offspring_range'] + random.randint(-1, 1)
        ant.dna['velocity'] = max(1, ant.dna['velocity'] + random.randrange(-1, 2))

        # ant.dna = {'energy': ant.energy, 'vision_mask': ant.vision_mask, 'vision_distance': ant.vision_distance, 'offspring_range': ant.offspring_range, 'velocity': ant.velocity}
    def offspring_generation(self):
        ants = []
        num_ant = random.randint(0, self.dna['offspring_range'])
        for _ in range(num_ant):
            if self.dna['energy'] < offspring_energy_required:
                break
            ant = Ant(self.dna, None, self.vector, self)
            self.dna['energy'] -= offspring_energy_required

    def energy_calc(self, vector):
        return max(1, (self.dna['energy']/1000)) + self.dna['velocity']*box_distance(self.vector, vector) + (self.dna['vision_mask'].count(1)*self.dna['vision_distance'])/10

    def x_y_vision(self, x, y):
        if x < 0:
            x = -1
        elif x > 0:
            x = 1
        if y < 0:
            y = -1
        elif y > 0:
            y = 1

        ind = self.direction
        for _ in range(8):
            # print(x, y, ind)
            if (x, y) == self.direction_move[ind]:
                return ind
            ind = (ind + 1)%8
        return 8

    def set_direction(self, prev_location, cur_location):
        x = cur_location.x - prev_location.x 
        y = cur_location.y - prev_location.y
        vs_msk = self.x_y_vision(x, y)
        if vs_msk == 8:
            self.direction = 0
        else:
            self.direction =  self.x_y_vision(x, y)

    def move(self):

        nearest_food = []
        nearest_food_to_move = None
        nearest_location_to_move = None
        prev_location = self.vector
        # map_ind = [column, row, right_diagonal, left_diagonal]
        map_ind = [self.vector.x, self.vector.y, self.vector.x + self.vector.y, GRID_WIDTH-self.vector.x + self.vector.y]
        ind = 0
        for map in self.food.food_map.values():
            for food in map[map_ind[ind]]:
                x = self.vector.x - food.x
                y = self.vector.y - food.y
                vs_msk = self.x_y_vision(x, y)
                if box_distance(self.vector, food) <= self.dna['vision_distance'] and (vs_msk == 8 or self.dna['vision_mask'][vs_msk]):
                    nearest_food.append([box_distance(food, self.vector), food])
            ind += 1


        found_food = False
        # move to the nearest food
        if len(nearest_food) > 0:
            nearest_food.sort(key = operator.itemgetter(0))
            nearest_food_len = nearest_food[0][0]

            # move to random food having distance same as nearest food
            ind = 0
            while ind < len(nearest_food):
                if nearest_food[ind][0] > nearest_food_len:
                    break
                ind += 1
            rnd = random.randrange(0, ind)
            nearest_food_to_move = nearest_food[rnd][1]

            # move directly to food position if velocity is greater than distance
            # if box_distance(nearest_food_to_move, self.vector) <= self.dna['velocity'] and self.dna['energy'] >= self.energy_calc(nearest_food_to_move):
            if box_distance(nearest_food_to_move, self.vector) <= self.dna['velocity']:
                nearest_location_to_move = nearest_food_to_move
                self.vector = nearest_location_to_move
                self.set_direction(prev_location, self.vector)
                return nearest_location_to_move, nearest_food_to_move

            # move randomly to any 8 pos which is near to the nearest food
            else:
                min_distance = 1e9
                for move in slopes:
                    x, y = move[0]*self.dna['velocity'] + self.vector.x, move[1]*self.dna['velocity'] + self.vector.y
                    # if in_grid(x, y) and self.dna['energy'] >= self.energy_calc(Vector(x, y)):
                    if in_grid(x, y):
                        euclid_dist = euclidean_distance(nearest_food_to_move, Vector(x, y))
                        if euclid_dist < min_distance:
                            min_distance = euclid_dist
                            nearest_location_to_move = Vector(x, y)
                
                        

        # if no food found in vision move randomly
        if nearest_food_to_move == None:
            moves = slopes
            random.shuffle(moves)
            for move in moves:
                x, y = move[0] + self.vector.x, move[1] + self.vector.y
                # if in_grid(x, y) and self.energy_calc(Vector(x, y)) <= self.dna['energy']:
                if in_grid(x, y):
                    nearest_location_to_move = Vector(x, y)
                    break
        
        self.dna['energy'] -= self.energy_calc(nearest_location_to_move)
        self.vector = nearest_location_to_move
        self.set_direction(prev_location, self.vector)

        
        return nearest_location_to_move, None

    def draw(self, WIN):
        ant_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        ant_image.fill((0, 0, 0))
        WIN.blit(ant_image, (self.vector.x*TILE_SIZE, self.vector.y*TILE_SIZE))
        # Color_line=(100,100,100)
        # pygame.draw.line(WIN,Color_line,(60,80),(130,100))


    # def __str__(self):
    #     return str(self.__class__) + ": " + str(self.__dict__)

    # def __repr__(self):
    #     return str(self.__class__) + ": " + str(self.__dict__)
            
            
