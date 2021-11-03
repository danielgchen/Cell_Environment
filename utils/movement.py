from .core import *
from .detection import *

# TODO: get testing functions for these
# gets the new cell center based on movement differentials
def move_cell_center(cell, diffs):
    '''
    based on the dimensional differences outputs the new cell center
    '''
    # compute new locations
    if(len(diffs) > 0):
        record = spin(cell.genetics['cell_direction_remember'])  # whether to record it for next time
        if(record):
            cell.cell_diffs = diffs
    else:
        diffs = cell.cell_diffs
    # get coordinates
    cell.cell_center = adjust_coords(np.array(diffs) + np.array(cell.cell_center))

# TODO: pull out something for cell to food movements to incorporate this as well
# TODO: make sure to test this
# TODO: create a general repulsion and a general attraction, make movements something defined by attraction_weight * (attraction via food) + repulsion_weight (repulsion via neighbors) make sure that the weights are mutatable from -1 to 1
# computes the repulsion from neighbors if there is any
def get_neighbor_repulsion(curr_cell, cells, max_dist):
    # set tracking variables
    seen = np.empty((0,n_dims))  # manage an array of one-dimensional movements
    weights = []  # manage the relative weights of each of these movements
    # work through currently existing foods
    cell_centers = [(cell.cell_radius, cell.cell_center) for cell in cells]
    valid_cells = membrane_to_center_objectlist(curr_cell.cell_center, curr_cell.cell_radius, cell_centers, 0.5, False)
    for cell_radius, cell_center in valid_cells:
        # get differences in position from the cell
        diff = np.array(curr_cell.cell_center) - np.array(cell_center)
        # scale according to the cell step
        true_dist = cell_radius - center_to_center_distance(curr_cell.cell_center, cell_center)   # true distance we want to move
        true_dist = true_dist if true_dist <= max_dist else max_dist
        dividing_factor = np.sqrt(np.power(diff, 2).sum() / np.power(true_dist, 2))
        diff /= dividing_factor if dividing_factor != 0 else 1  # no movement
        # add to the already seen stack
        seen = np.vstack([seen, diff])
        # get weight factor
        dist = np.linalg.norm(np.array(curr_cell.cell_center) - np.array(cell_center))
        weight = 1 / dist if dist != 0 else 1e10  # artifically large to prevent divide by zero errors
        weights.append(weight)
    diffs = []  # instantiate
    if(weights):  # if there were any seen food
        # sort the list of seen foods
        weights = np.array(weights) / sum(weights)
        # compute final direction
        diffs = np.dot(weights, seen)
    # return the final movement
    return diffs


# TODO: get testing functions for these
# adjust the current position for neighboring cells
def adjust_for_neighbors(cell, cells, max_dist):
    '''
    takes the given new center and moves it back a bit given the positions of the old center
    and the neighboring cells, pulls on detection mechanisms
    '''
    # TODO: maybe get a loop for repulsion for how squishy the cell is
    # get the repulsion vector
    diffs = get_neighbor_repulsion(cell, cells, max_dist)
    # adjust the new center for the repulsion
    if(len(diffs) > 0):
        cell.cell_center = np.array(cell.cell_center) + diffs  # TODO: make new_center always np array
