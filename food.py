# import packages
import numpy as np
# import constants
from constants import *

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
        default function to add food to a given mouse click
        '''
        # get random position
        center = get_rand_coords(padding=self.food_radius)
        # >>> only for testing
        angle = get_rand_angle()
        # x,y = np.cos(angle), np.sin(angle)
        # scale = np.random.uniform(100,125)
        # x,y = x*scale + window_width / 2, y*scale + window_height / 2
        x,y = angle/(2*np.pi), np.sin(angle)
        scale = np.random.uniform(100,125)
        x,y = x*window_width, y*scale + window_height / 2
        # <<<
        # call helper function
        self.add_food_custom((x,y))


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
        valid_foods = self.get_detected(cell.cell_center, cell.cell_radius + self.food_radius)
        for food,(x,y) in valid_foods:
            cell_to_food_dist = get_distance(cell.cell_center,[x,y]) - cell.cell_radius
            if(cell_to_food_dist <= self.food_radius):
                eaten += 1  # count how many we're eaten
                self.canvas.delete(food)  # remove from canvas
                self.foods.remove((food,(x,y)))
        return eaten


    def get_seen(self, cell):
        '''
        checks if a cell can see the food if so it reports the food and the distance
        '''
        # set tracking variables
        seen = []
        # work through currently existing foods
        valid_foods = self.get_detected(cell.cell_center, cell.genetics['cell_vision_radius'] * cell.cell_radius + self.food_radius)
        for food,(x,y) in valid_foods:
            cell_to_food_dist = get_distance(cell.cell_center,[x,y]) - cell.genetics['cell_vision_radius'] * cell.cell_radius
            if(cell_to_food_dist <= self.food_radius):
                # get angle from cell
                y = y - cell.cell_center[1]
                x = x - cell.cell_center[0]
                angle = np.arctan2(y, x)
                # get weight factor
                vec_dist = [angle, cell_to_food_dist + cell.genetics['cell_vision_radius'] * cell.cell_radius]
                # take weight as inverse distance such that smaller distances have larger weights
                assert vec_dist[1] >= 0  # so we can assume that distance is not a negative number
                vec_dist[1] = 1 / vec_dist[1] if vec_dist[1] != 0 else 1e10  # artifically large to prevent divide by zero errors
                seen.append(vec_dist)
        # filter for the top ones (i.e. min distance) that the cell considers
        seen = sorted(seen, key=lambda vec_dist: vec_dist[1])[:round(cell.genetics['cell_vision_nconsidered'])]
        return seen
