# import packages
import numpy as np
# import constants
from utils import *

class Food:
    def __init__(self, canvas):
        '''
        create a Food object that is presented on the mouse click location
        '''
        # define attributes
        self.canvas = canvas
        self.food_radius = food_radius
        self.foods = []  # track the food present in our system

        # define key bindings
        self.canvas.bind('<Button-1>', self.add_food_click)


    def add_food_click(self, event):
        '''
        default function to add food to a given mouse click
        '''
        # get position from mouse click event
        center = event.x, event.y
        # call helper function
        self.add_food_custom(center)


    def add_food_random(self):
        '''
        default function to add food to a random location
        '''
        # get random position
        center = get_rand_coords(padding=self.food_radius)
        # >>>>>>> purely for testing
        angle = get_rand_angle()
        x,y = np.cos(angle), np.sin(angle)
        x,y = np.cos(angle), np.sin(angle)
        scale = np.random.uniform(100,125)
        x,y = x*scale + window_width / 2, y*scale + window_height / 2
        center = x,y
        # <<<<<<< purely for testing
        # call helper function
        self.add_food_custom(center)


    def add_food_custom(self, center):
        '''
        given an x and y coordinate add a piece of food given a constant food_radius
        '''
        # get the coordinates for the oval
        tl_x,tl_y,br_x,br_y = get_oval_coords(center=center, radius=self.food_radius)
        # plot the piece of food at the mouse position
        food = self.canvas.create_oval(tl_x, tl_y, br_x, br_y, fill='green', outline='forestgreen')
        # track the instantiated piece of food
        self.foods.append((food,center)) # add the object to track


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


    def get_eaten(self, cell):
        '''
        checks if a cell is overlapping with the food, in this case we define overlapping as cell barrier
        is touching the food center, so cell center - food center - cell radius <= food radius
        '''
        # set tracking variables
        eaten = 0  # track if a food was indeed eaten
        # work through all currently existing foods
        valid_foods = membrane_to_center_objectlist(cell.cell_center, cell.cell_radius, self.foods, 1)
        for food,food_center in valid_foods:
            if(membrane_to_center_overlap(cell.cell_center, cell.cell_radius, food_center, 1)):
                eaten += 1  # count how many we're eaten
                self.canvas.delete(food)  # remove from canvas
                self.foods.remove((food, food_center))
        return eaten


    def get_seen(self, cell):
        '''
        checks if a cell can see the food if so it reports the food and the distance
        '''
        # set tracking variables
        seen = np.empty((0,n_dims))  # manage an array of one-dimensional movements
        weights = []  # manage the relative weights of each of these movements
        # work through currently existing foods
        valid_foods = membrane_to_center_objectlist(cell.cell_center, cell.cell_radius, self.foods, cell.genetics['cell_vision_scale'])
        for food, food_center in valid_foods:
            # get differences in position from the cell
            diff = np.array(food_center) - np.array(cell.cell_center)
            seen = np.vstack([seen, diff])
            # get weight factor
            dist = np.linalg.norm(np.array(cell.cell_center) - np.array(food_center))
            weight = 1 / dist if dist != 0 else 1e10  # artifically large to prevent divide by zero errors
            weights.append(weight)
        diffs = []  # instantiate
        if(weights):  # if there were any seen food
            # sort the list of seen foods
            weights = np.array(weights)
            idx = np.argsort(weights)
            seen,weights = seen[idx], weights[idx]
            # filter for the top ones (i.e. min distance) that the cell considers
            n_seen = round(cell.genetics['cell_vision_nconsidered'])
            seen,weights = seen[:n_seen], weights[:n_seen]
            # compute final direction
            diffs = np.dot(weights, seen)
            # scale according to the cell step
            dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(cell.cell_step, 2))
            diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
        # return the final movement
        return diffs
