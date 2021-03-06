from .core import *
from .detection import *


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
    valid_cells = membrane_to_center_objectlist_cell(cell['cell_center'], cell['cell_radius'], cells, 1, False)
    removed_origin_cell = False
    for cell_radius, cell_center in valid_cells:
        if(not removed_origin_cell):
            # get differences in position from the cell
            diff = np.array(cell['cell_center']) - np.array(cell_center)
            if(diff.sum() == 0):  # detect whether or not the original cell is in our state
                removed_origin_cell = True
                continue
            # add to the already seen stack
            seen = np.vstack([seen, diff])
            # get weight factor
            dist = np.linalg.norm(np.array(cell['cell_center']) - np.array(cell_center))
            weight = 1 / dist if dist != 0 else 1e10  # artifically large to prevent divide by zero errors
            weights.append(weight)
    diffs = []  # instantiate
    if(weights):  # if there were any seen food
        # compute final direction
        diffs = np.dot(weights, seen)
        # scale to cell step so we can use equally weight factors later on
        dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(cell['cell_step'], 2))
        diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # return the final movement
    return diffs, len(diffs) == 0


# TODO: get testing functions for this
# get the nearby food attraction vector
def get_attraction(cell, foods):
    '''
    computes weighted attraction directional vector based on nearby food objects
    '''
    # set tracking variables
    seen = np.empty((0,n_dims))  # manage an array of one-dimensional movements
    weights = []  # manage the relative weights of each of these movements
    # work through currently existing foods
    food_centers = membrane_to_center_objectlist(cell['cell_center'], cell['cell_radius'], foods, cell['cell_vision_scale'], False)
    for _, food_center in food_centers:
        # get differences in position from the cell
        diff = np.array(food_center) - np.array(cell['cell_center'])
        seen = np.vstack([seen, diff])
        # get weight factor
        dist = np.linalg.norm(np.array(cell['cell_center']) - np.array(food_center))
        weight = 1 / dist if dist != 0 else 1e10  # artifically large to prevent divide by zero errors
        weights.append(weight)
    diffs = []  # instantiate
    if(weights):  # if there were any seen food
        # sort the list of seen foods
        weights = np.array(weights)
        idx = np.argsort(weights)
        seen,weights = seen[idx], weights[idx]
        # filter for the top ones (i.e. min distance) that the cell considers
        n_seen = round(cell['cell_vision_nconsidered'])
        seen,weights = seen[:n_seen], weights[:n_seen]
        # compute final direction
        diffs = np.dot(weights, seen)
        # scale according to the cell step
        dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(cell['cell_step'], 2))
        diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # return the final movement
    return diffs, len(diffs) == 0


# TODO: what if we have global parameters tracking important cell attributes like radius, center and cells have pointers to these attributes that way we can avoid having to move cells around
# TODO: get testing functions for this
# get the combined directional vector
def get_direction(cell, food, cells):
    '''
    computes a combined direction based on attraction and repulsion
    '''
    # define the parameter to tell if anything has been detected
    detected = False
    # get the directional vectors
    in_cell = {'cell_center':cell.cell_center, 'cell_radius':cell.cell_radius, 'cell_step':cell.cell_step, 'cell_vision_scale':cell.genetics['cell_vision_scale'], 'cell_vision_nconsidered':cell.genetics['cell_vision_nconsidered']}
    # > process foods
    in_foods = [[0, food_obj[1]] for food_obj in food.foods]
    diffs_r, detected_r = get_repulsion(in_cell, cells)
    diffs_a, detected_a = get_attraction(in_cell, in_foods)
    # deal with possible zeros
    if(len(diffs_r) == 0):
        diffs_r = np.zeros(n_dims)
    if(len(diffs_a) == 0):
        diffs_a = np.zeros(n_dims)
    # multiply by weights
    diffs_r *= cell.genetics['cell_repulsion_weight']
    diffs_a *= cell.genetics['cell_attraction_weight']
    # fix to final vector
    diffs = diffs_r + diffs_a
    # TODO: pull this out into an outside function
    dividing_factor = np.sqrt(np.power(diffs, 2).sum() / np.power(cell.cell_step, 2))
    diffs /= dividing_factor if dividing_factor != 0 else 1  # no movement
    # return the final movement
    return diffs, detected

# TODO: decide whether or not we want to manage empty lists in the movement methods





# TODO: create a general repulsion and a general attraction, make movements something defined by attraction_weight * (attraction via food) + repulsion_weight (repulsion via neighbors) make sure that the weights are mutatable from -1 to 1
