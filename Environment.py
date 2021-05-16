from operator import le
from Food import *
from Ant import *
from Vector import *
from settings import *

def custom_ant_comparator(ant):
    return ant.dna['energy']
    
class Environment:
    def __init__(self, dna, num_initial_ants, num_initial_food, day_length):
        self.base_dna = dna
        self.food = Food(num_initial_food)
        self.ants = []
        self.add_ants([], num_initial_ants)
        self.day_length = day_length
        self.num_initial_food = num_initial_food
    
    def add_ants(self, ants, num_ants, mutation = False):
        if len(ants) == 0:
            for _ in range(num_ants):
                ant = Ant(self.base_dna, self.food, self.random_location())
                if mutation:
                    ant.mutate(ant)
                self.ants.append(ant)
        else:
            self.ants.extend(ants)

    def random_location(self):
        return Vector(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))

    def rank_population(self):
        self.ants.sort(key=custom_ant_comparator, reverse=True)

    def random_pick(self):
        parent_select_percentage = 0.5
        l = 0
        r = floor(parent_select_percentage * len(self.ants))
        return random.randrange(l, r+1)

    def mating(self):
        parent1 = self.ants[self.random_pick()]
        parent2 = self.ants[self.random_pick()]
        child = Ant(parent1.dna, self.food, self.random_location())
        for key in parent2.dna.keys():
            if random.randrange(0, 2)==1:
                child.dna[key] = parent2.dna[key]
        child.dna['energy'] = 1000
        if random.random() <= 0.5:
            child.mutate(child)
        return child

    def next_generation(self, elitesize):
        ants = []
        self.rank_population()
        # print(self.ants[0].energy, self.ants[0].velocity)
        eng = 0
        for ant in self.ants:
            eng += ant.dna['energy']
        print(eng, self.ants[0].dna)
        self.food = Food(self.num_initial_food)
        for _ in range(elitesize):
            ants.append(Ant(self.ants[0].dna, self.food, self.random_location()))
        for _ in range(len(self.ants) - elitesize):
            ants.append(self.mating())
        self.ants = ants
        # for ant in ants:
        #     print(ant.dna)

    def loop(self, gui):
        if gui:
            FPS = 7
            WHITE = (200, 200, 200)
            pygame.display.set_caption("Ant Game")
            clock = pygame.time.Clock()
            ANT_IMAGE = None
            WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

        QUIT = False
        while QUIT == False and len(self.food.food) > 0:
            if gui:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        QUIT = True
                        pygame.quit()
                        quit()

                # print(ant, end='\n\n\n\n')
                WIN.fill((255, 255, 255))
                self.food.draw(WIN)
                for ant in self.ants:
                    ant.draw(WIN)
                pygame.display.update()
            
            less_energy_ant = []
            for ant in self.ants:
                ant_new_locaion, food_on_ant = ant.move()
                if ant_new_locaion == None:
                    less_energy_ant.append(ant)
                elif food_on_ant != None:
                    self.food.add_competition(food_on_ant, ant)

            energy_dict = self.food.get_energy()
            for ant in self.ants:
                if ant in energy_dict:
                    ant.dna['energy'] += energy_dict[ant]

            # print(ant.energy)
        # for ant in self.ants:
        #     print(ant.energy, ant.velocity)

    def ga(self, gui, num_iter, elitesize):
        while num_iter > 0:
            if num_iter >= 2:
                self.loop(gui)
            else:
                break
                print(len(self.ants))
                self.loop(True)
            # print('\n\n\n')
            self.next_generation(elitesize)
            num_iter -= 1
        