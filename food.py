# import packages
import numpy as np
# import constants
from constants import *

class Food:
    def __init__(self, canvas):
        '''
        create a Food object that is presented on the mouse click location
        '''
        self.canvas = canvas
        self.food_radius = food_radius
        self.foods = []  # track the food present in our system
        self.canvas.bind('<Button-1>', self.add_food_click)

    def add_food_click(self, event):
        '''
        default function to add food to a given mouse click
        '''
        # get position from mouse click event
        x,y = event.x, event.y
        # call helper function
        self.add_food_custom(x,y)

    def add_food_random(self):
        '''
        default function to add food to a given mouse click
        '''
        # get random position
        x = np.random.uniform(0 + self.food_radius, window_width - self.food_radius)
        # y = np.random.uniform(0 + self.food_radius, window_height - self.food_radius)
        y = np.random.uniform(window_height * 0.4 + self.food_radius, window_height * 0.6 - self.food_radius)
        # call helper function
        self.add_food_custom(x,y)

    def add_food_custom(self, x, y):
        '''
        given an x and y coordinate add a piece of food given a constant food_radius
        '''
        # plot the piece of food at the mouse position
        # - specifies topleft(x,y) then bottomright(x,y)
        tl_x,tl_y = x - self.food_radius, y - self.food_radius  # define top left
        br_x,br_y = x + self.food_radius, y + self.food_radius  # define bottom right
        food = self.canvas.create_oval(tl_x, tl_y, br_x, br_y, fill='green', outline='forestgreen')
        self.foods.append((food,(x,y))) # add the object to track

    def eaten(self, cell):
        '''
        checks if a cell is overlapping with the food, in this case we define overlapping as cell barrier
        is touching the food center, so cell center - food center - cell radius <= food radius
        '''
        eaten = 0  # track if a food was indeed eaten
        def distance(xs, ys):
            '''
            assumes xs and ys are of equal length and calculates euclidean distance
            '''
            dist = 0
            for idx,x in enumerate(xs):
                dist += (x - ys[idx]) ** 2
            dist = np.sqrt(dist)  # to get sqrt((x2-x1)^2.....)
            return dist
        # retrieve cell center
        cell_x,cell_y = cell.center
        # work through all currently existing foods
        for food,(food_x,food_y) in self.foods:
            cell_to_food_dist = distance([cell_x,cell_y],[food_x,food_y]) - cell.cell_radius
            if(cell_to_food_dist <= self.food_radius):
                eaten += 1  # count how many we're eaten
                self.canvas.delete(food)  # remove from canvas
                self.foods.remove((food,(food_x,food_y)))
        return eaten
