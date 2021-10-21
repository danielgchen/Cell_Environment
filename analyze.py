# import packages
import pickle
import pandas as pd
import matplotlib.pyplot as plt
# import constants
from constants import *

'''
reads in the tracking file and outputs out a plot of the cells across time
'''

# TODO: deal with snapshots of data
def record_snapshot(cells):
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
    pickle.dump(values, open(track_filename + '.pkl','wb'))

def convert_cells():
    # read in data
    data = pickle.load(open(track_filename + '.pkl','rb'))
    # convert to dataframe
    df = pd.DataFrame(data)
    df.to_csv(track_filename + '.csv')

def analyze_history():
    # read in data
    df = pd.read_csv(track_filename + '.txt')
    # define clones present
    clones = df['clone'].unique()
    # plot lines
    fig,ax = plt.subplots(figsize=[8,4])
    for clone in clones:
        plot_df = df.loc[df['clone']==clone]
        ax.plot(plot_df.index, plot_df['count'], color=clone)
    fig.tight_layout()
    fig.savefig(track_filename + '_analysis.png', dpi=300)

if __name__ == '__main__':
    analyze_history()
    convert_cells()
