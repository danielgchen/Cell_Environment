import os
import pickle
from .core import *
from collections import Counter

# changes given filename to default track filename if needed
def get_fname(given_filename=None):
    '''
    returns the default track filename if we don't specify a given filename
    '''
    if(given_filename is None):
        write_filename = track_filename
    else:
        write_filename = given_filename
    return write_filename


# record a pickled snapshot of the data
def record_snapshot(cells, total_rounds, given_filename=None):
    '''
    for a given list of cells records their attributes
    '''
    values = []  # set tracking variable
    # loop through each cell
    columns = ['color','radius','center','age','health','metabolic_cost']
    for cell in cells:
        # initial attributes
        row = [cell.color, cell.radius, cell.center, cell.age, cell.health, cell.get_metabolic_cost()]
        row = {columns[idx]:value for idx,value in enumerate(row)}
        for key,value in cell.genetics.items():
            row[key] = value
        values.append(row)
    # write the data
    if(not os.path.exists('outputs')):
        os.mkdir('outputs/')
    pickle.dump(values, open(f'outputs/{get_fname(given_filename)}.{total_rounds}.pkl', 'wb'))


# record the population heterogeneity at each time point
def record_population(cells, total_rounds, given_filename=None):
    '''
    this records the absolute number for each cell type at a certain round
    '''
    # count the cell colors
    colors = Counter([cell.color for cell in cells])
    # report it in a tracking file
    with open(f'outputs/{get_fname(given_filename)}.txt', 'at') as f:
        for color,count in colors.items():
            f.writelines(f'{total_rounds},{color},{count}\n')
