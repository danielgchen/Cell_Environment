# import packages
import numpy as np
import time
import copy
# import constants
from constants import *

class Cell:
    def __init__(self, canvas, genetics, cell_color=None, init_center=None):
        '''
        create a cell object that can be presented on a given center
        genetics consists of a dictionary specifying cell attributes
        '''
        # set given attributes
        self.canvas = canvas  # where we are drawing the cell
        self.cell_color = get_rand_color() if cell_color is None else cell_color
        # TODO add MUTATIONAL RATE
        self.genetics = genetics  # contains cell cycle, and directionalties
        # set constant attributes
        self.cell_radius = cell_radius  # track how big the cell is
        self.cell_health = cell_health  # food eaten - moves made
        self.cell_metabolic_cost = cell_metabolic_cost  # the rate at which movement costs energy
        self.cell_step = cell_step  # the size of the step the cell can take in any direction
        # set baseline attributes
        self.cell_alive = True  # tracks if the cell is dead
        self.cell_age = 0  # related to cell alive, after a certain age (i.e. number of rounds) the cell dies
        # create the cell
        self.instantiate(init_center)

    # define key cellular functions
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
        # create cell's directions
        # - if needed generate random weightings
        if('cell_direction_weights' not in self.genetics):
            self.genetics['cell_direction_weights'] = [[get_rand_angle(),1]]
        # get vision radius and vision nconsidered
        if('cell_vision_radius' not in self.genetics):
            self.genetics['cell_vision_radius'] = np.random.uniform(1.01, 3) * self.cell_radius  # 101-300% cell radius
        if('cell_vision_nconsidered' not in self.genetics):
            self.genetics['cell_vision_nconsidered'] = np.random.uniform(1, 3)  # 1-3 foods

    def move(self, foods):
        '''
        move the cell for a certain step
        '''
        # TODO get the cell to have variable memory of the past food locations?
        # compute new locations
        # - get angle
        angle = get_weighted_mean(self.genetics['cell_direction_weights']) if len(foods) == 0 else get_weighted_mean(foods)
        # - get coordinates
        new_center = shift_coords(self.cell_center, radius=self.cell_radius, angle=angle)
        self.cell_center = new_center
        # - add step to current_location
        new_tl_x,new_tl_y,new_br_x,new_br_y = get_oval_coords(center=new_center, radius=self.cell_radius)
        # assign new coordinates
        self.canvas.coords(self.cell, new_tl_x, new_tl_y, new_br_x, new_br_y)

        # update cell attributes
        # - update cell health status
        self.cell_health -= self.cell_step * self.cell_metabolic_cost  # adjust for movement cost
        # - age the cell
        self.cell_age += 1  # as increased cell cycle means more moves per round more likekly to accrue fatal mutation
        # - check if cell needs to die
        if(self.cell_age > cell_age_of_death):
            self.cell_alive = False  # marked for apoptosis

    def eat(self, n_eaten):
        '''
        if we eat a piece of food then we revive ourselves by lowering our age
        '''
        self.cell_age -= n_eaten  # manages how long the cell may remain alive
        self.cell_health += n_eaten  # manages the cell's ability to proliferate
        # check if we need to divide
        if(self.cell_health >= cell_threshold_to_divide):
            cell = self.divide()  # cell proliferates
            return cell  # we made a new cell, let's keep track of it
        else:
            return None  # no cell to provide

    def mutate(self):
        '''
        perform mutations for the cell
        '''
        # copy current genetics
        genetics = copy.deepcopy(self.genetics)
        # mutate genetic directionality
        if(get_spin_outcome(cell_mutation_rate)):
            # compute shift
            max_shift = cell_mutation_direction_weights
            shift = np.random.uniform(-max_shift, max_shift) * 2 * np.pi
            # perform mutation
            angle,weight = genetics['cell_direction_weights'][0]
            genetics['cell_direction_weights'] = [[angle + shift,weight]]
        # mutate cell vision radius
        if(get_spin_outcome(cell_mutation_rate)):
            # compute shift
            max_shift = cell_mutation_vision_radius
            shift = np.random.uniform(-max_shift, max_shift) * 1
            # perform mutation
            vision_radius = genetics['cell_vision_radius'] + shift
            # - a cell needs to at least be able to see 1% of it's radius away but it cannot be a supervision cell so it maxes out at 10x
            vision_radius = adjust_value(vision_radius, lower_limit=1.01*self.cell_radius, upper_limit=10*self.cell_radius, continous=False)
            genetics['cell_vision_radius'] = vision_radius
        # mutate cell vision n-considered
        if(get_spin_outcome(cell_mutation_rate)):
            # compute shift
            max_shift = cell_mutation_vision_nconsidered
            shift = np.random.uniform(-max_shift, max_shift) * 1
            # perform mutation
            vision_radius = genetics['cell_vision_nconsidered'] + shift
            # - a cell should only consider 1-100 pieces of food or it gets out of hand
            vision_radius = adjust_value(vision_radius, lower_limit=1, upper_limit=100, continous=False)
            genetics['cell_vision_radius'] = vision_radius
        # TODO correlate mutational capacity to age, and cell cycle and maybe track movement and eating separately
        # TODO mutate cell color and cell cycle
        # TODO compute custom mutational rate
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
