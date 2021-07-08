import numpy as np

'''
define all of the constants needed for the simulatons
'''

# define base mutational rate mean
# > this represents the chance of mutation and the std represents the
#   max change of all mutational rates as if we hit the max twice we should
#   be able to exit the 95% confidence interval of normal mutations
cell_mutational_rate_mean = 0.25
cell_mutational_rate_std = 0.05
# define cell mutational rate limits
cell_mutational_rate_llimit = 1e-10
cell_mutational_rate_ulimit = 1
# define cell cycle limits
cell_cycle_llimit = 0.5 + 1e-10  # below one in case it wants to encode for a suppressive function
cell_cycle_ulimit = 5
# define cell directional remembrance limits
cell_direction_remember_llimit = 0
cell_direction_remember_ulimit = 1
# define cell vision radius limits
cell_vision_radius_llimit = 1.01
cell_vision_radius_ulimit = 20
# define cell vision nconsidered limits
cell_vision_nconsidered_llimit = 1
cell_vision_nconsidered_ulimit = 100
# define the filename to track data in
track_filename = 'track'
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

# define base method to get a random angle
def get_rand_angle():
    '''
    returns a random angle from [0, 2pi)
    '''
    return np.random.uniform(0, 2*np.pi)


# define base method to create random colors
def get_rand_color():
    '''
    creates a random color via the rgb value type switched into hex formation
    '''
    rand_rgb = lambda: np.random.randint(0, 255)  # define method to generate random rgb value
    # create hex color %02X means convert to hexadecimal format
    hex_color = '#%02X%02X%02X' % (rand_rgb(),rand_rgb(),rand_rgb())
    return hex_color


# define base method to derive euclidean distance
def get_distance(xs, ys):
    '''
    assumes xs and ys are of equal length and calculates euclidean distance
    and they represent vector1 and vector2
    '''
    dist = 0
    for idx,x in enumerate(xs):
        dist += (x - ys[idx]) ** 2
    dist = np.sqrt(dist)  # to get sqrt((x2-x1)^2.....)
    return dist


# define base method to decide if a cell mutates
def get_spin_outcome(chance):
    '''
    using a given chance of something happening returns if it happens or not
    it's like spinning a spinner so we call it get_spin_outcome
    '''
    value = np.random.uniform(0, 1)
    if(value < chance):
        return True
    else:
        return False


# define generalizable method to adjust values
def adjust_value(value, lower_limit, upper_limit, continous):
    '''
    if continous adjust the value such that it is within lower limit and upper limit
    but it loops around, if it is not continous then bring it back up to min or max
    '''
    if(continous):
        if(value < lower_limit):
            value += upper_limit
        elif(value > upper_limit):
            value -= upper_limit
    else:
        if(value < lower_limit):
            value = lower_limit
        elif(value > upper_limit):
            value = upper_limit
    return value


# define base method to get x component of an angle and radius
def get_angle_xcomp(angle, radius):
    '''
    returns the x component via the cos function and scales it by the radius
    '''
    return np.cos(angle) * radius


# define base method to get y component of an angle and radius
def get_angle_ycomp(angle, radius):
    '''
    returns the y component via the sin function and scales it by the radius
    '''
    return np.sin(angle) * radius


# define base method to produce random coordinates within the canvas
def get_rand_coords(padding=None):
    '''
    create random coordinates within the canvas using the window constraints
    should there be padding given then assume it is radius-like and pad accordingly
    '''
    if(padding is None):
        padding = 0
    x = np.random.uniform(0 + padding, window_width - padding)
    y = np.random.uniform(0 + padding, window_height - padding)
    return x, y


# define generlizable method for deriving oval coordinates from center coordinates and a cell_radius
def get_oval_coords(center=None, radius=None):
    '''
    given a center x and y and a radius provide the corner oval coordinates
    if center is not given it'll generate random coordiantes, no radius --> radius = 1
    '''
    # generate randoms and set constants if needed
    if(radius is None):
        radius = 1
    x,y = get_rand_coords(padding=radius) if center is None else center
    # derive the corner coordinates
    tl_x,tl_y = x - radius, y - radius  # define top left
    br_x,br_y = x + radius, y + radius  # define bottom right
    return tl_x,tl_y,br_x,br_y


# define generlizable method for weighted average
def get_weighted_mean(value_list):
    '''
    computes weighted mean via list of tuples of value,weight assuming weights are comparable across values
    '''
    # create tracking variables
    value_total = 0  # instantiate angle
    weight_total = 0  # so we can divide by total to get weighted mean later
    # compute weighted average
    for value,weight in value_list:
        value_total += value * weight
        weight_total += weight
    value_total /= weight_total  # compute weighted average
    return value_total


# define method to adjust values for coordinates
def adjust_coords(center):
    '''
    adjusts the given x and y with the constants window_width and window_height
    '''
    # get x and y of center
    curr_x, curr_y = center
    # adjust x
    new_x = adjust_value(curr_x, 0, window_width, continous=True)
    # adjust y
    new_y = adjust_value(curr_y, 0, window_height, continous=True)
    return new_x, new_y


# define method to produce coordinates next to a given center using a randomized angle
def shift_coords(center, radius, angle=None):
    '''
    produces random coordinates next to a given x and y and radius
    can use a given angle if provided in radians
    '''
    # get x and y of center
    curr_x, curr_y = center
    # get angle
    angle = get_rand_angle() if angle is None else angle
    # get steps in x and y
    shift_x,shift_y = get_angle_xcomp(angle, radius), get_angle_ycomp(angle, radius)
    # add step to current location
    new_center = curr_x + shift_x, curr_y + shift_y
    # make sure new_x and new_y are within the bounds of the window if not shift them over
    new_center = adjust_coords(new_center)
    return new_center
