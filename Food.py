from settings import *
from Vector import *
import random
import pygame

class Food:
    def __init__(self, num_food):
        self.food = []
        self.energy_in_food = 100
        self.food_competition = {}
        self.food_map = {
            'column' : [[] for i in range(GRID_HEIGHT+GRID_WIDTH)],
            'row' : [[] for i in range(GRID_HEIGHT+GRID_WIDTH)],
            'right_diagonal' : [[] for i in range(GRID_HEIGHT+GRID_WIDTH)],
            'left_diagonal' : [[] for i in range(GRID_HEIGHT+GRID_WIDTH)]
        }
        for _ in range(num_food):
            self.add_food()

    def mapind(self, food):
        return [food.x, food.y, food.x + food.y, GRID_WIDTH-food.x + food.y]

    def add_food(self):
        x, y = random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)
        food = Vector(x, y)
        self.food.append(food)
        map_ind = self.mapind(food)
        ind = 0
        for map in self.food_map.values():
            map[map_ind[ind]].append(food)
            ind += 1

    def add_competition(self, food_on_ant, ant):
        if food_on_ant in self.food_competition:
            self.food_competition[food_on_ant].append(ant)
        else:
            self.food_competition[food_on_ant] = [ant]

    def get_energy(self):
        energy_dict = {}
        for ants in self.food_competition.values():
            l = len(ants)
            for ant in ants:
                energy_dict[ant] = self.energy_in_food/l

        for food in self.food_competition.keys():
            self.food.remove(food)
            map_ind = self.mapind(food)
            ind = 0
            for map in self.food_map.values():
                map[map_ind[ind]].remove(food)
                ind += 1

            
        self.food_competition = {}
        return energy_dict

    def draw(self, WIN):
        food_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        food_image.fill((255, 0, 0))
        for food in self.food:
            WIN.blit(food_image, (food.x*TILE_SIZE, food.y*TILE_SIZE))

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
