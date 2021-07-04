import numpy as np

'''
define all of the constants needed for the simulatons
'''

# define cell mutational rate for directionality
# TODO incorporate this into the cell itself
# TODO define limits in the constants file
# TODO total mutation and directional weight mutation can be different
# TODO define the chance of a mutation and the mutational change as separate entities
cell_mutation_rate = 0.25  # chance for a mutation to occur
cell_mutation_direction_weights = 0.25  # mutate the values by a max of X%
# define the filename to track data in
track_filename = 'track.txt'
# define delay in time between rounds
round_delay = 0  # in seconds
# define canvas size
window_width,window_height = 500,500
# define initial amount of food
initial_num_food = 25  # number of starting pieces of food
# define food per round
food_per_round = 5  # get new pieces of food per round
# define initial cells
initial_num_cells = 100  # how many cells do we start with
# define time between actions for a cell
cell_cycle = 1  # number of actions per round
# define time for a cell to dies
cell_age_of_death = 50  # number of rounds total
# compute food radius size
food_radius = min(window_width,window_height) * 0.01 / 2  # take 1% of the smallest dimension
# compute cell radius size
cell_radius = min(window_width,window_height) * 0.025 / 2  # take 2.5% of the smallest dimension
# compute the length of a step for the cell to be able to take
cell_step = min(window_width,window_height) * 0.01 / 2  # take 1% of the smallest dimension
# define the initial cell health
cell_health = 0  # basically the handicap for the cell to divide
# define the food movement balance needed for the cell to divide
cell_threshold_to_divide = 1  # eaten one more food than movement
# define the metabolic cost of movements
cell_metabolic_cost = 0.01  # a movement has X% metabolic cost so moving costs X% of the step size

# define method to adjust coordinates
def adjust_coords(new_x, new_y):
    '''
    adjusts the given x and y with the constants window_width and window_height
    '''
    if(new_x < 0): new_x += window_width
    elif(new_x > window_width): new_x -= window_width
    if(new_y < 0): new_y += window_height
    elif(new_y > window_height): new_y -= window_height
    return new_x, new_y

# define method to produce random coordinates next to a given center
def create_coords(curr_x, curr_y, radius, angle=None):
    '''
    produces random coordinates next to a given x and y and radius
    can use a given angle if provided in radians
    '''
    # TODO add random x and y generation capability
    if(angle is None):
        # - choose a random angle
        angle = np.random.uniform(0, 2*np.pi)  # angle in radians
    # - compute step
    shift_x,shift_y = np.cos(angle) * radius, np.sin(angle) * radius
    # - add step to current location
    new_x,new_y = curr_x + shift_x, curr_y + shift_y
    # - make sure new_x and new_y are within the bounds of the window if not shift them over
    new_x,new_y = adjust_coords(new_x, new_y)
    return new_x, new_y

# define method to create random colors
def random_color():
    '''
    creates a random color via the rgb value type switched into hex formation
    '''
    rand_rgb = lambda: np.random.randint(0, 255)  # define method to generate random rgb value
    # create hex color %02X means convert to hexadecimal format
    hex_color = '#%02X%02X%02X' % (rand_rgb(),rand_rgb(),rand_rgb())
    return hex_color

# define method to compute a randomized angle given certain weights in a dictionary form
def derive_weighted_angle(directions):
    '''
    gets a preferential direction and weights it according to input
    '''
    x = directions['east'] - directions['west']
    y = directions['north'] - directions['south']
    angle = np.arctan2(y, x)  # compute angle
    return angle
