import pygame
import numpy as np
import random
from settings import *
from Ant import *
from Food import *
from Environment import *

gui = True
# gui = False

dna = {'energy': 1000, 'vision_mask': [1 for i in range(8)], 'vision_distance': 20, 'offspring_range': 5, 'velocity': 1}

def main():
    env = Environment(dna = dna, num_initial_ants= 4, num_initial_food=40,day_length=100)
    env.ga(gui = gui, num_iter=2, elitesize=1)


main()