import pygame
import numpy as np
import random
from settings import *
from Ant import *
from Food import *
from Environment import *

gui = True
# gui = False

dna = {'energy': 1000, 'vision_mask': [1 for i in range(8)], 'vision_distance': 20, 'offspring_range': 4, 'velocity': 1}

def main():
    env = Environment(dna = dna, num_initial_ants= 4, num_initial_food=40,day_length=100)
    env.ga(gui = gui, num_iter=1000, elitesize=1)

def main2():
    for i in range(0, 11):
        print('Sacrifice rate - >', i*0.1)
        env = Environment(dna = dna, num_initial_ants= 4, num_initial_food=40,day_length=100)
        env.sacrifice_rate = i*0.1
        env.ga(gui = gui, num_iter=1000, elitesize=1)

main()
# main2()