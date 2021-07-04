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
        self.cell_color = random_color() if cell_color is None else cell_color
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
        # create cell's position
        if(init_center is None):
            # plot the cell at a random position
            # - define the constraints of our central x and y
            x = np.random.uniform(0 + self.cell_radius, window_width - self.cell_radius)
            y = np.random.uniform(0 + self.cell_radius, window_height - self.cell_radius)
        else:
            # plot the cell at the given location
            x,y = init_center
        # - specifies topleft(x,y) then bottomright(x,y)
        tl_x,tl_y = x - self.cell_radius, y - self.cell_radius  # define top left
        br_x,br_y = x + self.cell_radius, y + self.cell_radius  # define bottom right
        self.cell = self.canvas.create_oval(tl_x, tl_y, br_x, br_y, fill=self.cell_color, outline='maroon')
        self.center = x,y  # track the cell center to compute movements

        # create cell's directions
        # - if needed generate random weightings
        if('cell_direction_weights' not in self.genetics):
            self.genetics['cell_direction_weights'] = {}
            for direction in ['north','east','south','west']:
                # get a random percent
                self.genetics['cell_direction_weights'][direction] = np.random.uniform(0, 1)

    def move(self):
        '''
        move the cell for a certain step
        '''
        # compute new locations
        # - get custom angle TODO add a randomized component to this
        angle = derive_weighted_angle(self.genetics['cell_direction_weights'])
        # - get coordinates
        curr_x,curr_y = self.center  # unpack arguments
        new_x,new_y = create_coords(curr_x, curr_y, radius=self.cell_radius, angle=angle)
        # - add step to current_location
        new_tl_x,new_tl_y = new_x - self.cell_radius, new_y - self.cell_radius  # define top left
        new_br_x,new_br_y = new_x + self.cell_radius, new_y + self.cell_radius  # define bottom right
        # assign new coordinates
        # self.canvas.create_line(curr_x, curr_y, new_x, new_y, fill=self.cell_color)   # to track history
        self.center = new_x,new_y
        self.canvas.coords(self.cell, new_tl_x, new_tl_y, new_br_x, new_br_y)
        # self.canvas.create_oval(new_tl_x, new_tl_y, new_br_x, new_br_y, fill=self.cell_color, outline='maroon')   # to track history

        # update cell attributes
        # - update cell health status
        # TODO health status should be reflective of cell alive state
        self.cell_health -= self.cell_step * self.cell_metabolic_cost  # adjust for movement cost
        # - age the cell
        self.cell_age += 1 / self.genetics['cell_cycle']  # as increased cell cycle means more moves per round
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
        # TODO correlate mutational capacity to age, and cell cycle and maybe track movement and eating separately
        # TODO mutate cell color and cell cycle
        # TODO compute custom mutational rate
        # mutate cell directionality
        for direction in genetics['cell_direction_weights']:
            # TODO set generalizable limits function in constants to control what values we can mutate too
            # TODO possibly set the chance of death via incorrect mutation
            # test if we will mutate value
            # TODO put this in a function somewhere
            mutate = np.random.uniform(0, 1) < cell_mutation_rate
            if(mutate):
                current_value = genetics['cell_direction_weights'][direction]
                change_max = cell_mutation_direction_weights  # since these are percents we don't multiply
                change_value = np.random.uniform(-change_max, change_max)
                current_value += change_value
                # TODO create generalizable method for limit testing
                if(current_value < 0): current_value = 0  # make sure it is within bounds
                elif(current_value > 1): current_value = 1  # make sure the value is reasonable
                genetics['cell_direction_weights'][direction] = current_value + change_value
        return genetics

    def divide(self):
        '''
        divide the cell, at a random angle next to the mother cell
        '''
        # update the mother cell status
        self.cell_health -= cell_threshold_to_divide  # cost of proliferation
        # compute new locations
        # - get coordinates
        curr_x,curr_y = self.center  # unpack arguments
        new_x,new_y = create_coords(curr_x, curr_y, radius=self.cell_radius)
        # create the new cell
        # - mutate the cell so the new cell can be different
        genetics = self.mutate()
        # - inherits the mutated traits of the original cell
        cell = Cell(self.canvas, genetics, cell_color=self.cell_color, init_center=(new_x,new_y))
        return cell

    def die(self):
        '''
        kill the cell, leave an x and delete the original cell
        '''
        # remove the cell
        self.canvas.delete(self.cell)
