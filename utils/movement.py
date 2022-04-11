from .core import *
from .detection import *

# TODO: get testing functions for this and a lot of other things
def get_food_diffusion(food_center, vent_center, rng=None):
    '''
    computes a random movement for the food and weights the diff vector by the
    distance from the origin of the vent normalized to halt at a min and max
    '''
    rng = rng if rng is not None else core_rng
    # define the difference vector
    diffs = np.array([rng.integers(-food_step_res, food_step_res) for _ in range(n_dims)], dtype='float')
    # scale the difference vector to the max step possible
    dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(max_food_step, 2))
    diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # scale the dividing vector by it's distance from the vent
    scaling_factor = (window_diagonal + np.linalg.norm(food_center - vent_center)) / window_diagonal
    diffs = scaling_factor * diffs
    # up to the minimum food step if needed
    if(min_food_step > np.linalg.norm(diffs)):
        dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(min_food_step, 2))
        diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # perform the delta
    food_center += diffs
    return food_center


# TODO: get testing functions for this
# get the neighboring cell repulsion vector
def get_repulsion(cell, cells):
    '''
    computes weighted repulsion directional vector based on neighboring cells
    '''
    # set tracking variables
    seen = np.empty((0,n_dims))  # manage an array of one-dimensional movements
    weights = []  # manage the relative weights of each of these movements
    # TODO: make the radius of cell cell detection variable like in attraction
    # TODO: make a negative movement counter if a cell get's too close so it has to figure out itself how to weight this properly
    # TODO: do a complete overhaul of the membrane to center system so it inputs centers
    valid_cells = membrane_to_center_objectlist_nparray(cell['center'], cell['radius'], cells, 1, False)
    removed_origin_cell = False
    for radius, center in valid_cells:
        if(not removed_origin_cell):
            # get differences in position from the cell
            diff = np.array(cell['center']) - np.array(center)
            if(diff.sum() == 0):  # detect whether or not the original cell is in our state
                removed_origin_cell = True
                continue
            # add to the already seen stack
            seen = np.vstack([seen, diff])
            # get weight factor
            dist = np.linalg.norm(np.array(cell['center']) - np.array(center))
            weight = 1 / dist if dist != 0 else 1e10  # artifically large to prevent divide by zero errors
            weights.append(weight)
    diffs = []  # instantiate
    if(weights):  # if there were any seen food
        # compute final direction
        diffs = np.dot(weights, seen)
        # scale to cell step so we can use equally weight factors later on
        dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(cell['step'], 2))
        diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # return the final movement
    return diffs, len(diffs) == 0


# TODO: get testing functions for this
# get the nearby food attraction vector
def get_attraction(cell, foods_attrs):
    '''
    computes weighted attraction directional vector based on nearby food objects
    '''
    # set tracking variables
    seen = np.empty((0,n_dims))  # manage an array of one-dimensional movements
    weights = []  # manage the relative weights of each of these movements
    # work through currently existing foods
    food_centers = membrane_to_center_objectlist_nparray(cell['center'], cell['radius'], foods_attrs, cell['vision_scale'], False)
    for _, food_center in food_centers:
        # get differences in position from the cell
        diff = np.array(food_center) - np.array(cell['center'])
        seen = np.vstack([seen, diff])
        # get weight factor
        dist = np.linalg.norm(np.array(cell['center']) - np.array(food_center))
        weight = 1 / dist if dist != 0 else 1e10  # artifically large to prevent divide by zero errors
        weights.append(weight)
    diffs = []  # instantiate
    if(weights):  # if there were any seen food
        # sort the list of seen foods
        weights = np.array(weights)
        idx = np.argsort(weights)
        seen,weights = seen[idx], weights[idx]
        # filter for the top ones (i.e. min distance) that the cell considers
        n_seen = round(cell['vision_nconsidered'])
        seen,weights = seen[:n_seen], weights[:n_seen]
        # compute final direction
        diffs = np.dot(weights, seen)
        # scale according to the cell step
        dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(cell['step'], 2))
        diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # return the final movement
    return diffs, len(diffs) == 0


# TODO: what if we have global parameters tracking important cell attributes like radius, center and cells have pointers to these attributes that way we can avoid having to move cells around
# TODO: get testing functions for this
# get the combined directional vector
def get_direction(cell, vents, cells):
    '''
    computes a combined direction based on attraction and repulsion
    '''
    # define the parameter to tell if anything has been detected
    detected = False
    # get the directional vectors
    in_cell = {'center':cell.center, 'radius':cell.radius, 'step':cell.step, 'vision_scale':cell.genetics['vision_scale'], 'vision_nconsidered':cell.genetics['vision_nconsidered']}
    # > process foods
    in_foods = np.concatenate([vent.foods_attrs for vent in vents], axis=0)
    diffs_r, detected_r = get_repulsion(in_cell, cells)
    diffs_a, detected_a = get_attraction(in_cell, in_foods)
    # deal with possible zeros
    if(len(diffs_r) == 0):
        diffs_r = np.zeros(n_dims)
    if(len(diffs_a) == 0):
        diffs_a = np.zeros(n_dims)
    # multiply by weights
    diffs_r *= cell.genetics['repulsion_weight']
    diffs_a *= cell.genetics['attraction_weight']
    # fix to final vector
    diffs = diffs_r + diffs_a
    # TODO: pull this out into an outside function
    dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(cell.step, 2))
    diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # return the final movement
    return diffs, detected

# TODO: decide whether or not we want to manage empty lists in the movement methods





# TODO: create a general repulsion and a general attraction, make movements something defined by attraction_weight * (attraction via food) + repulsion_weight (repulsion via neighbors) make sure that the weights are mutatable from -1 to 1
