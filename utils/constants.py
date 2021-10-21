from .core import *

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
