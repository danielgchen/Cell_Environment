# import packages
import numpy as np
from food import *
# import constants
from utils import *

# TODO: create on and off probabilities for the vent
# TODO: define key bindings such as `self.canvas.bind('<Button-1>', self.add_food_click)``
class Vent:
    def __init__(self, canvas, rng=None, center=None, radius=None):
        '''
        create a Vent object on a given or a random location
        '''
        # create set parameters
        self.canvas = canvas
        self.radius = vent_radius if radius is None else radius
        self.center = get_rand_coords(padding=self.radius) if center is None else center
        # physically create the vent
        # TODO: change all namings to blob
        tl_x,tl_y,br_x,br_y = get_oval_coords(self.center, self.radius)
        self.blob = self.canvas.create_oval(tl_x, tl_y, br_x, br_y, fill='forestgreen', outline='forestgreen')
        # setup the food attributes
        self.foods = []
        self.foods_attrs = np.empty((0,n_dims + 1))


    # adds a new piece of food at any given location or randomly
    def _add_food(self, center=None, radius=None):
        '''
        method to add a new piece of food at a given center and given radius
        '''
        food = Food(self.canvas, center=center, radius=radius)
        self.foods, self.foods_attrs = add_to_env(food, self.foods, self.foods_attrs)


    # adds a new piece of food from the center of the vent
    def add_food(self):
        '''
        method to add a new piece of food within the vent
        '''
        # TODO: make sure to make it so it can be anywhere in the vent
        self._add_food(center=self.center)


    # diffuses foods in brownian motion in a radiating manner away from the vent
    def diffuse_foods(self):
        '''
        temperature based probability movement function where the probability
        is based on the magnitude from the source
        '''
        if(len(self.foods) > 0):
            for idx,food in enumerate(self.foods):
                # mathematically update the values
                food_center = self.foods_attrs[idx,1:]  # get the row of information
                vent_center = self.center  # assign to a variable for ease of reading
                food_center = adjust_coords(get_food_diffusion(food_center, vent_center))
                # update the object
                food.center,self.foods_attrs[idx,1:] = food_center, food_center
                # physically update the object
                tl_x,tl_y,br_x,br_y = get_oval_coords(center=food.center, radius=food.radius)
                food.canvas.coords(food.blob, tl_x, tl_y, br_x, br_y)
