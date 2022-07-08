# import packages
import numpy as np
# import constants
from .core import *
from matplotlib.colors import to_hex

def get_detected(self, center, radius):
    '''
    filters for things within the x and y center, radius derived square
    as oval and square objects will all be forced to be within this larger boundary
    '''
    # compute boundaries
    ck_x,ck_y = center
    ck_x_min,ck_x_max = ck_x - radius, ck_x + radius
    ck_y_min,ck_y_max = ck_y - radius, ck_y + radius
    # filter foods for things within boundaries [min,max] based
    valid_foods = []
    for food,(x,y) in self.foods:
        if(x >= ck_x_min and x <= ck_x_max and y >= ck_y_min and y <= ck_y_max):
            valid_foods.append((food,(x,y)))
    return valid_foods


def get_food_color(age):
    '''
    retrieves the color from the given age
    '''
    return to_hex(food_cmap(age / food_lifespan))
