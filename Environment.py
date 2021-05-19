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
        self.clock = 0
        self.food = Food(num_initial_food)
        self.ants = []
        self.removed_ants = []
        self.removed_foods = []
        self.add_ants([], num_initial_ants)
        self.day_length = day_length
        self.num_initial_food = num_initial_food
        self.sacrifice_rate = 0
        self.generation_num = 1
    
    def add_ants(self, ants, num_ants, mutation = False):
        if len(ants) == 0:
            for _ in range(num_ants):
                ant = Ant(self.base_dna, self.food, self.random_location(), self.clock)
                if mutation:
                    ant.mutate(ant)
                self.ants.append(ant)
        else:
            self.ants.extend(ants)

    def random_location(self):
        return Vector(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))

    # def rank_population(self):
    #     self.ants.sort(key=custom_ant_comparator, reverse=True)

    # def random_pick(self):
        parent_select_percentage = 0.5
        l = 0
        r = floor(parent_select_percentage * len(self.ants))
        return random.randrange(l, r+1)

    # def mating(self):
        parent1 = self.ants[self.random_pick()]
        parent2 = self.ants[self.random_pick()]
        child = Ant(parent1.dna, self.food, self.random_location())
        for key in parent2.dna.keys():
            if random.randrange(0, 2)==1:
                child.dna[key] = parent2.dna[key]
        # child.dna['energy'] = 1000
        if random.random() <= 0.5:
            child.mutate(child)
        return child

    def remove_ants(self, remove_ant):
        for ant in remove_ant:
            ant.end_timestamp = self.clock
            self.removed_ants.append(ant)
            self.ants.remove(ant)
        
        # for ant in remove_ant:
        #     print(ant.create_timestamp, ant.end_timestamp )
        
    def next_generation(self, elitesize):
        if len(self.ants) == 0:
            return None


        self.food = Food(self.num_initial_food)

        remove_ant = []
        ants = []
        for ant in self.ants:
            offspring_ants = ant.offspring_generation(self.food)
            for offspring_ant in offspring_ants:
                offspring_ant.create_timestamp = self.clock
                offspring_ant.end_timestamp = self.clock

            if ant.dna['energy'] <= 0 or (len(self.ants) > len(self.food.food) and random.random() < self.sacrifice_rate):
                remove_ant.append(ant)
            ant.food = self.food
            ants.extend(offspring_ants)
        self.ants.extend(ants)

        self.remove_ants(remove_ant)

    def loop(self, gui):
        if gui:
            FPS = 20
            WHITE = (200, 200, 200)
            pygame.display.set_caption("Ant Game")
            clock = pygame.time.Clock()
            ANT_IMAGE = None
            WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

        QUIT = False
        prev_clock = self.clock
        # while QUIT == False and len(self.ants) > 0 and (self.clock - prev_clock < 20 or len(self.food.food) > 0):
        while QUIT == False and len(self.ants) > 0 and (self.clock - prev_clock < 20 or len(self.food.food) > 0) and self.clock - prev_clock < 100:
            self.clock += 1
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
            
            less_energy_ants = []
            for ant in self.ants:
                ant_new_locaion, food_on_ant = ant.move()
                if food_on_ant != None:
                    self.food.add_competition(food_on_ant, ant)

            energy_dict = self.food.get_energy()
            for ant in self.ants:
                if ant in energy_dict:
                    ant.dna['energy'] += energy_dict[ant]

            for ant in self.ants:
                if ant.dna['energy'] <= 0:
                    less_energy_ants.append(ant)

            self.remove_ants(less_energy_ants)

        # for ant in self.ants:
        #     print(ant.dna['energy'], ant.dna['velocity'])

    def ga(self, gui, num_iter, elitesize):
        gui=False
        while num_iter > 0 and len(self.ants) > 0:
            print('Generation Number = {}  Number of ants = {}'.format(self.generation_num, len(self.ants)))
            self.loop(gui)
            # for ant in self.ants:
            #     print(ant.dna['energy'])
            # for ant in self.removed_ants:
            #     print(len(ant.all_vector_positions), ant.dna['velocity'])
            if num_iter > 1:
                self.next_generation(elitesize)
            self.generation_num += 1
            num_iter -= 1

        
        while len(self.ants) > 0:
            ant = self.ants.pop()
            ant.end_timestamp = self.clock
            self.removed_ants.append(ant)

        # print(len(set(self.ants)))
        # for ant in self.removed_ants:
        #     print(ant.create_timestamp, ant.end_timestamp)
        # for ant in self.removed_ants:
        #     print(ant.all_vector_positions, len(ant.all_vector_positions), ant.dna['energy'])
        

        