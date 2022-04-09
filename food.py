# import packages
import numpy as np
# import constants
from utils import *

class Food:
    def __init__(self, canvas, center=None, radius=None):
        '''
        create a Food object on a given or a random location
        '''
        # define attributes
        self.canvas = canvas
        self.radius = food_radius if radius is None else radius
        self.center = get_rand_coords(padding=self.radius) if center is None else center
        # physically create the food
        # TODO: change all namings to blob FINISHED HERE
        tl_x,tl_y,br_x,br_y = get_oval_coords(self.center, self.radius)
        self.blob = self.canvas.create_oval(tl_x, tl_y, br_x, br_y, fill='limegreen', outline='forestgreen')
        # create food_lifespan
        self.age = 0


    def die(self):
        '''
        kill the food
        '''
        # remove the food
        self.canvas.delete(self.blob)
