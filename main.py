from settings import *
from Ant import *
from Food import *
from Environment import *
import pickle

gui = True
# gui = False

dna = {'energy': 1000, 'vision_mask': [1 for i in range(8)], 'vision_distance': 20, 'offspring_range': 4, 'velocity': 1}

def main():
    env = Environment(dna = dna, num_initial_ants= 4, num_initial_food=40,day_length=100)
    save = env.ga(gui = gui, num_iter=2)
    with open('save.pickle', 'wb') as handle:
        pickle.dump(save, handle, protocol=4)

def main2():
    for i in range(0, 11):
        print('Sacrifice rate - >', i*0.1)
        env = Environment(dna = dna, num_initial_ants= 4, num_initial_food=40,day_length=100)
        env.sacrifice_rate = i*0.1
        env.ga(gui = gui, num_iter=1000, elitesize=1)

main()
# main2()