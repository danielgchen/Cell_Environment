from .core import *

# TODO: add a testing function
# defines a method to add a new cell
def add_to_env(new_cell, cells, cells_attrs):
    '''
    given a new cell it adds it to the cellular environment
    '''
    # add to the list of tkinter cells
    cells.append(new_cell)
    # add to the list of attributes
    cells_attrs = np.append(cells_attrs, [np.append(new_cell.cell_radius, new_cell.cell_center)], 0)


# TODO: add a testing function
# defines a method to remove an old cell
def remove_from_env(cell, idx, cells, cells_attrs):
    '''
    given an old cell it removes it from the cellular enviroment
    '''
    # remove it from the list of tkinter cells
    cells = cells.remove(cell)
    # remove it from the list of attributes
    cells_attrs = np.delete(cells_attrs, idx)
