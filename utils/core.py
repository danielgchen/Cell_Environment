import numpy as np
from multiprocessing import Pool, cpu_count
from matplotlib import cm

'''
define all of the constants needed for the simulatons
'''

# create pseudo random number bit generator that will used for this entire process
core_rng = np.random.default_rng()  # set the seed as 0

# define base method for calling any function
# TODO: creating testing function for this
def call_func(func, kwargs):
    return func(**kwargs)


# define a multiprocessing pooling method to use inputted functions and parameters
# TODO: creating testing function for this
def mp_pool(params, unordered=None):
    '''
    given a list of functions with parameters as in list of lists and outputs results
    '''
    # assign no async unless specified
    if(unordered is None):
        unordered = False
    # set up pool of cpus
    pool = Pool(cpu_count())
    # get results
    if(unordered):
        mapper = pool.starmap_async(call_func, params)
        results = mapper.get()
    else:
        results = pool.starmap(call_func, params)
    pool.close()
    return results


# define base method to get a random angle
def get_rand_angle(rng=None):
    '''
    returns a random angle from [0, 2pi)
    '''
    # set random generator defaults to core
    if(rng is None): rng = core_rng
    return rng.uniform(0, 2*np.pi)


# define base method to create random colors
def get_rand_color(rng=None):
    '''
    creates a random color via the rgb value type switched into hex formation
    '''
    # set random generator defaults to core
    if(rng is None): rng = core_rng
    # define method to generate random rgb value
    rand_rgb = lambda: rng.integers(0, 256)
    # create hex color %02X means convert to hexadecimal format
    hex_color = '#%02X%02X%02X' % (rand_rgb(),rand_rgb(),rand_rgb())
    return hex_color


# define base method to spin and see if it passes chance
def spin(chance, rng=None):
    '''
    using a given chance of something happening returns if it happens or not
    it's like spinning a spinner so we call it spin
    '''
    # set random generator defaults to core
    if(rng is None): rng = core_rng
    # calculate the random probability
    value = rng.uniform(0, 1)
    # return whether they passed
    return value < chance


# define generalizable method to adjust values
def adjust(value, lower_limit, upper_limit, continous):
    '''
    if continous adjust the value such that it is within lower limit and upper limit
    but it loops around, if it is not continous then bring it back up to min or max
    '''
    if(continous):
        while(value > upper_limit or value < lower_limit):
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


# define base method to produce random coordinates within the canvas
def get_rand_coords(padding=None, rng=None):
    '''
    create random coordinates within the canvas using the window constraints
    should there be padding given then assume it is radius-like and pad accordingly
    '''
    # set random generator defaults to core
    if(rng is None): rng = core_rng
    # perform padding
    if(padding is None):
        padding = 0
    x = rng.uniform(0 + padding, window_width - padding)
    y = rng.uniform(0 + padding, window_height - padding)
    return np.array([x, y])


# define generlizable method for deriving oval coordinates from center coordinates and a radius
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
    # adjust x
    new_x = adjust(center[0], 0, window_width, continous=True)
    # adjust y
    new_y = adjust(center[1], 0, window_height, continous=True)
    return np.array([new_x, new_y])


# define method to constrain dimensions to a certain magnitude
def scale_vector(vector, magnitude):
    '''
    uses the distance formula to backcalculate the value to scale the magnitude
    '''
    # calculate the dividing vector to scale the magnitude
    dividing_factor = np.sqrt(np.power(vector, 2).sum() / np.power(magnitude, 2))
    # compute the final division
    vector /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # return the new vector
    return vector


# define method to produce coordinates next to a given center using a randomized angle
def shift_coords(center, radius, shifts=None, rng=None):
    '''
    produces random coordinates next to a given x and y and radius
    can use a given angle if provided in radians
    '''
    # set random generator defaults to core
    if(rng is None): rng = core_rng
    # get the shift_vector
    shifts = [rng.uniform(-1,1) for _ in range(n_dims)] if shifts is None else shifts
    shifts = scale_vector(shifts, radius)
    # add step to current location
    new_center = center + shifts
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
# TODO: change this so it is based on the cell and we pull factors here
def get_metabolic_cost(base_cost, age, mutational_rate, health):
    '''
    consider a negative feedback cycle where worse health increases metabolic cost
    which makes it more difficult to derive food, age and mutational rate both increase strain
    we take the average health / time unit to derive whether the cell leans towards starvation
    '''
    weights = [((1 + age / age_of_death) ** 2 - 1, 1)]  # add in the percent of lifespan (squared for increased punishment with as we proceed towards death)
    weights += [(mutational_rate, 1)]  # add in mutational stress
    weights += [(-1 if health > 0 else 1, 1)]  # binary health metric
    metabolic_cost = get_weighted_mean(weights) * base_cost
    return metabolic_cost

# define pseudocount
pseudocount = 1e-10
# define base mutational rate mean
# > this represents the chance of mutation and the std represents the
#   max change of all mutational rates as if we hit the max twice we should
#   be able to exit the 95% confidence interval of normal mutations
mutational_rate_mean = 0.25
mutational_rate_std = 0.05
# define cell mutational rate limits
mutational_rate_llimit = pseudocount
mutational_rate_ulimit = 1
# define base cell cycle mean
cycle_mean = 1
cycle_std = 0.1
# define cell cycle limits
cycle_llimit = 0.5 + pseudocount  # below one in case it wants to encode for a suppressive function
cycle_ulimit = 5
# define base repulsion weight mean
# TODO: deprecate all  prefixs
repulsion_weight_mean = 0.5
repulsion_weight_std = 0.25
# define cell repulsion weight limits
repulsion_weight_ulimit = 1
repulsion_weight_llimit = -1
# define base attraction weight mean
attraction_weight_mean = 0.5
attraction_weight_std = 0.25
# define cell attraction weight limits
attraction_weight_ulimit = 1
attraction_weight_llimit = -1
# define base vision radius mean
vision_scale_mean = 2
vision_scale_std = 0.5
# define cell vision radius limits
vision_scale_llimit = 1.01
vision_scale_ulimit = 20
# define base vision nconsidered mean
vision_nconsidered_mean = 2
vision_nconsidered_std = 0.5
# define cell vision nconsidered limits
vision_nconsidered_llimit = 1
vision_nconsidered_ulimit = 100
# define cell direction pause mean
# TODO: make it so cells only move if there is food nearby?
direction_pause_mean = 0.1  # always moving
direction_pause_std = 0.025
# define cell direction pause limits
direction_pause_llimit = 0
direction_pause_ulimit = 1
# define the cell's initial attributes and limitations
# TODO: make this a function with an inputable rng
instantiation_information = {  # TODO: rename it pause
    'direction_pause': [instantiate_from_distribution, {'distribution':core_rng.normal, 'distribution_params':{'loc':direction_pause_mean, 'scale':direction_pause_std}, 'llimit':direction_pause_llimit, 'ulimit':direction_pause_ulimit, 'continous':False}],
    'cycle': [instantiate_from_distribution, {'distribution':core_rng.normal, 'distribution_params':{'loc':cycle_mean, 'scale':cycle_std}, 'llimit':cycle_llimit, 'ulimit':cycle_ulimit, 'continous':False}],
    'repulsion_weight': [instantiate_from_distribution, {'distribution':core_rng.normal, 'distribution_params':{'loc':repulsion_weight_mean, 'scale':repulsion_weight_std}, 'llimit':repulsion_weight_llimit, 'ulimit':repulsion_weight_ulimit, 'continous':False}],
    'attraction_weight': [instantiate_from_distribution, {'distribution':core_rng.normal, 'distribution_params':{'loc':attraction_weight_mean, 'scale':attraction_weight_std}, 'llimit':attraction_weight_llimit, 'ulimit':attraction_weight_ulimit, 'continous':False}],
    'vision_scale': [instantiate_from_distribution, {'distribution':core_rng.normal, 'distribution_params':{'loc':vision_scale_mean, 'scale':vision_scale_std}, 'llimit':vision_scale_llimit, 'ulimit':vision_scale_ulimit, 'continous':False}],
    'vision_nconsidered': [instantiate_from_distribution, {'distribution':core_rng.normal, 'distribution_params':{'loc':vision_nconsidered_mean, 'scale':vision_nconsidered_std}, 'llimit':vision_nconsidered_llimit, 'ulimit':vision_nconsidered_ulimit, 'continous':False}],
    'mutational_rate': [instantiate_from_distribution, {'distribution':core_rng.normal, 'distribution_params':{'loc':mutational_rate_mean, 'scale':mutational_rate_std}, 'llimit':mutational_rate_llimit, 'ulimit':mutational_rate_ulimit, 'continous':False}],
}
# define the filename to track data in
track_filename = 'track'
# define the number of dimensions
n_dims = 2
# define delay in time between rounds
round_delay = 0.1  # in seconds
# define canvas size
window_width,window_height = 500,500
window_diagonal = np.linalg.norm([window_width, window_height])
# define colors
background_color = '#ffffff'
vent_fillcolor = vent_edgecolor = 'forestgreen'
# define initial populations
initial_num_vents = 1  # how many vents we start with
food_per_vent_per_round = 10  # get new pieces of food per round for each vent
initial_num_cells = 1  # how many cells do we start with
# define object radius
food_radius = min(window_width,window_height) * 0.01 / 2  # diameter is 1% of the smallest dimension
cell_radius = min(window_width,window_height) * 0.025 / 2  # diameter is 2.5% of the smallest dimension
vent_radius = min(window_width,window_height) * 0.075 / 2  # diameter is 7.5% of the smallest dimension
# define cell characteristics
age_of_death = 25  # number of rounds total
step = min(window_width,window_height) * 0.01 / 2  # take 1% of the smallest dimension
health = 0  # basically the handicap for the cell to divide
threshold_to_divide = 1  # eaten one more food than movement
metabolic_cost = 0.05  # a movement has X% metabolic cost so moving costs X% of the step size
threshold_to_die = -10  # has moved ten times more than it has eaten food
# define vent characteristics
vent_random_overlap = False  # whether or not it is okay to have overlap
# define food characteristics
food_step_res = 4  # resolution of the food
init_food_step = vent_radius  # basically lets consider the equivalent push is at the one step away
max_food_step = vent_radius * 5  # basically lets consider the equivalent push is at the one step away
food_lifespan = 10
food_cmap = cm.get_cmap('RdYlGn_r')
