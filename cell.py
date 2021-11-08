# import packages
import numpy as np
import time
import copy
# import constants
from utils import *

class Cell:
    # TODO: link cell cycle to metabolic rate
    # TODO: create a basal metabolic rate and an actual metabolic rate that compounds on health and age
    def __init__(self, canvas, genetics=None, cell_color=None, init_center=None):
        '''
        create a cell object that can be presented on a given center
        genetics consists of a dictionary specifying cell attributes
        '''
        # TODO: change everything to numpy arrays
        # set given attributes
        self.canvas = canvas  # where we are drawing the cell
        self.cell_color = get_rand_color() if cell_color is None else cell_color
        self.genetics = {} if genetics is None else genetics  # contains all attributes
        # set constant attributes
        self.cell_radius = cell_radius  # track how big the cell is
        self.cell_health = cell_health  # food eaten - moves made
        self.cell_metabolic_cost = cell_metabolic_cost  # the rate at which movement costs energy
        # TODO make changeable cell step
        self.cell_step = cell_step  # the size of the step the cell can take in any direction
        # set baseline attributes
        self.cell_alive = True  # tracks if the cell is dead
        self.cell_age = 0  # related to cell alive, after a certain age (i.e. number of rounds) the cell dies
        # create the cell
        self.instantiate(init_center)


    # INSTANTION FUNCTION
    def instantiate(self, init_center=None):
        '''
        create the cell for the first time
        '''
        # create cell's position (random if not given)
        center = get_rand_coords(padding=self.cell_radius) if init_center is None else init_center
        # - specifies topleft(x,y) then bottomright(x,y)
        tl_x,tl_y,br_x,br_y = get_oval_coords(center, self.cell_radius)
        self.cell = self.canvas.create_oval(tl_x, tl_y, br_x, br_y, fill=self.cell_color, outline='maroon')
        self.cell_center = center  # track the cell center to compute movements
        # create cell attributes
        for key, (function, function_params) in cell_instantiation_information.items():
            if(key not in self.genetics):  # create attribute if it does not already exist
                self.genetics[key] = function(**function_params)
        # create mutational information
        if('cell_mutation_information' not in self.genetics):
            self.genetics['cell_mutation_information'] = []
        # - we identify the keys we want to mutate
        mutational_keys = [key for key in self.genetics.keys() if key != 'cell_mutation_information']
        # - we subset for keys that are not in the current cell_mutation_information attribute
        # TODO: store mutational information in dictionary format?
        current_mutational_keys = [row[0] for row in self.genetics['cell_mutation_information']]  # retrieve information
        mutational_keys = [name for name in mutational_keys if name not in current_mutational_keys]
        if('cell_mutational_rate' not in current_mutational_keys):
            mutational_keys.remove('cell_mutational_rate')
            mutational_keys = ['cell_mutational_rate'] + mutational_keys
        for key in mutational_keys:
            # > retrieve mutational percentage
            mutation_function,mutation_params = cell_instantiation_information['cell_mutational_rate']
            mutation_perc = mutation_function(**mutation_params)
            # > retrieve mutational magnitude (dealt via special cases)
            mutation_magnitude = 1  # we use raw percentage
            # > retrieve limits (dealt via the llimit and ulimit described above
            key_params = cell_instantiation_information[key][1]  # retrieve its limit information
            if('llimit' in key_params):  # if it has limits it should have llimit, ulimit and continous
                limits = key_params['llimit'], key_params['ulimit'], key_params['continous']
            else:
                limits = None  # set it to none if no limits detected
            # > create and record values
            values = [key, mutation_perc, mutation_magnitude, limits]
            self.genetics['cell_mutation_information'].append(values)


    # ACTION FUNCTIONS
    def move(self, food, cells, rng=None):
        '''
        move the cell for a certain step
        '''
        # test whether or not we need to pause or move
        if(spin(self.genetics['cell_direction_pause'])):
            # assuming resting does not affect a cell's health but does age the cell
            pass
        else:
            # TODO: incorporate multi-threading/multi-core usage
            # get the new movement vector
            diffs, detected = get_direction(self, food, cells)
            if(not detected):  # if they don't sense anything
                if(rng is None): rng = core_rng
                # TODO: adapt this to a markov like system?
                diffs = np.array([rng.integers(-4, 4) for _ in range(n_dims)])  # random walk
                # adjust for cell step
                dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(self.cell_step, 2))
                dividing_factor = dividing_factor if dividing_factor != 0 else 1  # no movement
                diffs = np.divide(diffs, dividing_factor)
            # calculate the new center based on movement
            new_center = np.array(self.cell_center) + diffs
            # adjust and set the new center
            self.cell_center = adjust_coords(new_center)
            # get the oval coordinates
            new_tl_x,new_tl_y,new_br_x,new_br_y = get_oval_coords(center=self.cell_center, radius=self.cell_radius)
            self.canvas.coords(self.cell, new_tl_x, new_tl_y, new_br_x, new_br_y)

            # update cell attributes
            # - update cell health status
            self.cell_health -= self.cell_step * self.get_cell_metabolic_cost()  # adjust for movement cost
        # universal cell attribute updates
        # - age the cell
        self.cell_age += 1  # as increased cell cycle means more moves per round more likely to accrue fatal mutation
        # - check if cell needs to die
        if(self.cell_age > cell_age_of_death):
            self.cell_alive = False  # marked for apoptosis


    def eat(self, n_eaten):
        '''
        if we eat a piece of food then we revive ourselves by lowering our age
        '''
        # post-eating food needs processing so we return a % of the food
        # TODO: create enzymes to manage this instead of metabolic cost
        benefit = n_eaten * (1 - self.get_cell_metabolic_cost())
        self.cell_age -= benefit  # manages how long the cell may remain alive
        self.cell_health += benefit  # manages the cell's ability to proliferate
        # check if we need to divide
        if(self.cell_health >= cell_threshold_to_divide):
            cell = self.divide()  # cell proliferates
            return cell  # we made a new cell, let's keep track of it
        else:
            return None  # no cell to provide


    def mutate(self, rng=None):
        '''
        perform mutations for the cell, for most mutations it is formatted via
        [key, mutation_perc, mutation_magnitude, (lower_limit, upper_limit)] we also deal with special cases
        '''
        # set random generator defaults to core
        if(rng is None): rng = core_rng
        # copy current genetics
        genetics = copy.deepcopy(self.genetics)
        # change mutational rate based on percent of lifespan
        age_scaling_factor = (1 + self.cell_age / cell_age_of_death) ** 2
        self.genetics['cell_mutational_rate'] *= age_scaling_factor  # so the current mutational rate is increased with age
        # pull out mutational rate and information
        cell_mutational_rate = self.genetics['cell_mutational_rate']  # we want this to be unchanged during the mutation
        cell_mutation_information = genetics['cell_mutation_information']  # we want this to be changed post-mutation
        # mutate each cell
        # - key = dictionary key in genetics
        # - mutation_perc = % change to multiply by
        # - mutation_magnitude = magnitude of the change we add or subtract by
        # - limits = (lower_limit, upper_limit, continous) or None to adjust the values by
        assert cell_mutation_information[0][0] == 'cell_mutational_rate'  # make sure we mutate the mutation first
        # > process the mutations
        for idx, (key, mutation_perc, mutation_magnitude, limits) in enumerate(cell_mutation_information):
            # > mutate the attribute
            if(spin(cell_mutational_rate)):  # see if we need to mutate
                # compute shift
                shift = rng.uniform(-mutation_perc, mutation_perc) * mutation_magnitude
                # perform mutation
                value = genetics[key] + shift
                # adjust values
                if(limits is not None):  # if it needs adjustment
                    lower_limit,upper_limit,continous = limits  # unpack values
                    value = adjust(value, lower_limit=lower_limit, upper_limit=upper_limit, continous=continous)
                # save values
                genetics[key] = value
            # > mutate the mutational rates
            # > we decide if we mutate these values based on the innate cell, but future
            #   mutational values are determined via the new mutational value as they are future cell
            if(spin(cell_mutational_rate)):  # see if we need to mutate
                # compute shift - currently using a fraction of the cell's mutational rate
                shift = rng.uniform(0, 1) * genetics['cell_mutational_rate']
                # perform mutation
                value = mutation_perc + shift
                # adjust values
                value = adjust(value, lower_limit=0, upper_limit=1, continous=False)
                # save values (1 = index of mutational perc)
                cell_mutation_information[idx][1] = value
        # TODO: correlate mutational capacity to cell cycle and maybe track movement and eating separately
        return genetics


    def divide(self):
        '''
        divide the cell, at a random angle next to the mother cell
        '''
        # update the mother cell status
        self.cell_health -= cell_threshold_to_divide  # cost of proliferation
        # compute new locations
        # - get coordinates
        new_center= shift_coords(self.cell_center, radius=self.cell_radius)
        # create the new cell
        # - mutate the cell so the new cell can be different
        genetics = self.mutate()
        # - inherits the mutated traits of the original cell
        cell = Cell(self.canvas, genetics, cell_color=self.cell_color, init_center=new_center)
        return cell


    def die(self):
        '''
        kill the cell, leave an x and delete the original cell
        '''
        # remove the cell
        self.canvas.delete(self.cell)


    # GET-VALUE FUNCTIONS
    # TODO: create a trait attribute to hold immutable attributes
    def get_cell_metabolic_cost(self):
        '''
        calculates the weighted average between factors of stress and scales it by the metabolic cost
        '''
        metabolic_cost = get_metabolic_cost(self.cell_metabolic_cost, self.cell_age, self.genetics['cell_mutational_rate'], self.cell_health)
        return metabolic_cost


    def get_cell_cycle(self):
        '''
        provides the rounded cell cycle
        '''
        cell_cycle = round(self.genetics['cell_cycle'])
        return cell_cycle
