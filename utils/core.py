import numpy as np

'''
define all of the constants needed for the simulatons
'''

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


# define base method to spin and see if it passes chance
def spin(chance):
    '''
    using a given chance of something happening returns if it happens or not
    it's like spinning a spinner so we call it spin
    '''
    # calculate the random probability
    value = np.random.uniform(0, 1)
    # return whether they passed
    return value < chance


# define generalizable method to adjust values
def adjust(value, lower_limit, upper_limit, continous):
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
    new_x = adjust(curr_x, 0, window_width, continous=True)
    # adjust y
    new_y = adjust(curr_y, 0, window_height, continous=True)
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


# define method to instantiate from a given distribution
def instantiate_from_distribution(**kwargs):
    '''
    using a given set of mean, std, distribution as well as limits to adjust by creates an initial value
    '''
    value = kwargs['distribution'](**kwargs['distribution_params'])  # retrieve value from the distribution
    value = adjust(value, kwargs['llimit'], kwargs['ulimit'], kwargs['continous'])  # adjust the value accordingly
    return value


# define method to derive metabolic cost
def get_metabolic_cost(base_cost, cell_age, cell_mutational_rate, cell_health):
    '''
    consider a negative feedback cycle where worse health increases metabolic cost
    which makes it more difficult to derive food, age and mutational rate both increase strain
    we take the average health / time unit to derive whether the cell leans towards starvation
    '''
    weights = [((cell_age / cell_age_of_death) ** 3,1)]  # add in the percent of lifespan (cubed for increased punishment with as we proceed towards death)
    weights += [(cell_mutational_rate,1)]  # add in mutational stress
    # starving is bad so as - health = starving and larger cost = bad we change signs
    # we add 1e-10 in case the cell_age == 0 which means it is the first step so cell_health also == 0
    weights += [((-1 * cell_health / (cell_age + 1e-10)),1)]  # average health / time unit
    metabolic_cost = get_weighted_mean(weights) * base_cost
    return metabolic_cost

# define base mutational rate mean
# > this represents the chance of mutation and the std represents the
#   max change of all mutational rates as if we hit the max twice we should
#   be able to exit the 95% confidence interval of normal mutations
cell_mutational_rate_mean = 0.25
cell_mutational_rate_std = 0.05
# define cell mutational rate limits
cell_mutational_rate_llimit = 1e-10
cell_mutational_rate_ulimit = 1
# define base cell cycle mean
cell_cycle_mean = 1
cell_cycle_std = 0.1
# define cell cycle limits
cell_cycle_llimit = 0.5 + 1e-10  # below one in case it wants to encode for a suppressive function
cell_cycle_ulimit = 5
# define base directional remembrance mean
cell_direction_remember_mean = 0.5
cell_direction_remember_std = 0.25
# define cell directional remembrance limits
cell_direction_remember_llimit = 0
cell_direction_remember_ulimit = 1
# define base vision radius mean
cell_vision_radius_mean = 2
cell_vision_radius_std = 0.5
# define cell vision radius limits
cell_vision_radius_llimit = 1.01
cell_vision_radius_ulimit = 20
# define base vision nconsidered mean
cell_vision_nconsidered_mean = 2
cell_vision_nconsidered_std = 0.5
# define cell vision nconsidered limits
cell_vision_nconsidered_llimit = 1
cell_vision_nconsidered_ulimit = 100
# define cell direction pause mean
# TODO: make it so cells only move if there is food nearby?
cell_direction_pause_mean = 0.1  # always moving
cell_direction_pause_std = 0.025
# define cell direction pause limits
cell_direction_pause_llimit = 0
cell_direction_pause_ulimit = 1
# define the cell's initial attributes and limitations
cell_instantiation_information = {
    'cell_direction_pause': [instantiate_from_distribution, {'distribution':np.random.normal, 'distribution_params':{'loc':cell_direction_pause_mean, 'scale':cell_direction_pause_std}, 'llimit':cell_direction_pause_llimit, 'ulimit':cell_direction_pause_ulimit, 'continous':False}],
    'cell_direction_angle': [get_rand_angle, {}],
    'cell_cycle': [instantiate_from_distribution, {'distribution':np.random.normal, 'distribution_params':{'loc':cell_cycle_mean, 'scale':cell_cycle_std}, 'llimit':cell_cycle_llimit, 'ulimit':cell_cycle_ulimit, 'continous':False}],
    'cell_direction_remember': [instantiate_from_distribution, {'distribution':np.random.normal, 'distribution_params':{'loc':cell_direction_remember_mean, 'scale':cell_direction_remember_std}, 'llimit':cell_direction_remember_llimit, 'ulimit':cell_direction_remember_ulimit, 'continous':False}],
    'cell_vision_radius': [instantiate_from_distribution, {'distribution':np.random.normal, 'distribution_params':{'loc':cell_vision_radius_mean, 'scale':cell_vision_radius_std}, 'llimit':cell_vision_radius_llimit, 'ulimit':cell_vision_radius_ulimit, 'continous':False}],
    'cell_vision_nconsidered': [instantiate_from_distribution, {'distribution':np.random.normal, 'distribution_params':{'loc':cell_vision_nconsidered_mean, 'scale':cell_vision_nconsidered_std}, 'llimit':cell_vision_nconsidered_llimit, 'ulimit':cell_vision_nconsidered_ulimit, 'continous':False}],
    'cell_mutational_rate': [instantiate_from_distribution, {'distribution':np.random.normal, 'distribution_params':{'loc':cell_mutational_rate_mean, 'scale':cell_mutational_rate_std}, 'llimit':cell_mutational_rate_llimit, 'ulimit':cell_mutational_rate_ulimit, 'continous':False}],
}
# define the filename to track data in
track_filename = 'track'
# define the number of dimensions
n_dims = 2
# define delay in time between rounds
round_delay = 0  # in seconds
# define canvas size
window_width,window_height = 500,500
# define initial amount of food
initial_num_food = 25  # number of starting pieces of food
# define food per round
food_per_round = 7  # get new pieces of food per round
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
