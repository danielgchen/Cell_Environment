# import packages
import numpy as np
# import constants
from utils import *

# TODO: create on and off probabilities for the vent
class Vent:
    # create a vandom or randomly create one
    def __init__(self, canvas, center=None, radius=None):
        # create set parameters
        self.canvas = canvas
        if(center is None):
            center = get_rand_coords(rng=rng)
        if(radius is None):
            radius = vent_radius
        # setup the food attributes
        self.foods = []
        self.foods_attrs = np.array()

    # TODO: set up something for food to diffuse
    # TODO: set up something for create a foods
    # TODO: the diffusion is just a loop on the food functions
    # TODO: the create food is just a wrapper for the instantiation of a food object
