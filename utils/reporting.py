import os
import pickle
from .core import *
from collections import Counter

# record a pickled snapshot of the data
# TODO: create a method to get manage given filename in this file
def record_snapshot(cells, total_rounds, given_filename=None):
    '''
    for a given list of cells records their attributes
    '''
    values = []  # set tracking variable
    # loop through each cell
    columns = ['cell_color','cell_radius','cell_center','cell_age','cell_health','cell_metabolic_cost']
    for cell in cells:
        # initial attributes
        row = [cell.cell_color, cell.cell_radius, cell.cell_center, cell.cell_age, cell.cell_health, cell.get_cell_metabolic_cost()]
        row = {columns[idx]:value for idx,value in enumerate(row)}
        for key,value in cell.genetics.items():
            row[key] = value
        values.append(row)
    # write the data
    if(not os.path.exists('outputs')):
        os.mkdir('outputs/')
    if(given_filename is None):
        write_filename = f'outputs/{track_filename}.{total_rounds}.pkl'
    else:
        write_filename = f'outputs/{given_filename}.{total_rounds}.pkl'
    pickle.dump(values, open(write_filename,'wb'))


# record the population heterogeneity at each time point
def record_population(cells, total_rounds, given_filename=None):
    '''
    this records the absolute number for each cell type at a certain round
    '''
    # count the cell colors
    cell_colors = Counter([cell.cell_color for cell in cells])
    # report it in a tracking file
    if(given_filename is None):
        write_filename = f'outputs/{track_filename}.txt'
    else:
        write_filename = f'outputs/{given_filename}.txt'
    with open(write_filename, 'at') as f:
        for cell_color,count in cell_colors.items():
            f.writelines(f'{total_rounds},{cell_color},{count}\n')
