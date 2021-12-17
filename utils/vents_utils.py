# import packages
import numpy as np
# import constants
from utils import *

# define a method to add a vent of a specified center and radius
def add_vent_custom(canvas, center, _vent_radius=None):
    '''
    given an x and y coordinate add a vent given a constant vent_radius
    '''
    # check whether or not to use the vent_radius
    if(_vent_radius is None): _vent_radius = vent_radius
    # get the coordinates for the oval
    tl_x,tl_y,br_x,br_y = get_oval_coords(center=center, radius=_vent_radius)
    # plot the piece of food at the mouse position
    vent = self.canvas.create_oval(tl_x, tl_y, br_x, br_y, fill=vent_fillcolor, outline=vent_edgecolor)
    return vent


# define a method to add a vent at a random location
def add_vent_random(center, rng=None, _vent_radius=None):
    '''
    this adds a vent and performs an optional check for vent overlap
    '''
    # grab a random center
    if(_vent_radius is None): _vent_radius = vent_radius
    center = get_rand_coords(rng=rng)
    # check for potential overlap if needed
    if(not vent_random_overlap):
        overlap = membrane_to_center_objectlist_nparray(center, _vent_radius, 1, True)
        while(overlap):
            center = get_rand_coords(rng=rng)
            overlap = membrane_to_center_objectlist_nparray(center, _vent_radius, 1, True)
    add_vent_custom(center, _vent_radius=_vent_radius)
