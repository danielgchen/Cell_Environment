# import packages
import os
import time
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from tqdm import tqdm
# import constants
from utils import *

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
    # write the data
    if(not os.path.exists('outputs')):
        os.mkdir('outputs/')
    pickle.dump(values, open(f'outputs/{track_filename}.{round(time.time())}.pkl','wb'))


def convert_cells(fname):
    # read in data
    data = pickle.load(open(fname,'rb'))
    # convert to dataframe
    df = pd.DataFrame(data)
    # write the dataframe
    df.to_csv(fname.replace('.pkl','.csv'))


def analyze_history():
    # write the data
    if(os.path.exists('analysis')):
        os.system('rm -rf analysis/')
    os.mkdir('analysis/')
    # read in data
    df = pd.read_csv(track_filename + '.txt')
    # define clones present
    clones = df['clone'].unique()
    # plot lines
    fig,ax = plt.subplots(figsize=[8,4])
    for clone in clones:
        plot_df = df.loc[df['clone']==clone]
        ax.plot(plot_df.index, plot_df['count'], color=clone)
    ax.set(xlabel='Time', ylabel='Cell Count')
    fig.tight_layout()
    fig.savefig('analysis/population_dynamics.png', dpi=300)


def analyze_traits():
    # compile the dataframe
    columns = ['cell_color', 'cell_radius', 'cell_center', 'cell_age', 'cell_health', 'cell_metabolic_cost', 'cell_direction_pause', 'cell_direction_angle', 'cell_cycle', 'cell_direction_remember', 'cell_vision_scale', 'cell_vision_nconsidered', 'cell_mutational_rate', 'cell_mutation_information']
    ss_df = pd.DataFrame(columns = columns + ['timeshot'])
    for fname in tqdm(glob('outputs/*.csv')):
        ss_df_subset = pd.read_csv(fname, index_col=0)
        ss_df_subset['timeshot'] = int(fname.split('.')[-2])
        ss_df = ss_df.append(ss_df_subset)
    ss_df = ss_df.sort_values('timeshot')
    # get the timepoints
    def count(rows):
        return len(set(rows['cell_color']))
    timeshot_nctypes = ss_df[['cell_color','timeshot']].groupby('timeshot').apply(count)
    timeshot_b4domination = timeshot_nctypes[timeshot_nctypes > 1].index.max()
    # get the cell colors
    ss_mean_df = ss_df.groupby(['cell_color','timeshot']).mean()
    cell_colors = list(set([arr[0] for arr in ss_mean_df.index]))
    # get the plots
    for col in ss_mean_df.loc[cell_colors[0]].columns:
        # > plot all timepoints
        fig,ax = plt.subplots(figsize=[8,4])
        ax.grid(False)
        for cell_color in cell_colors:
            ss_mean_df_subset = ss_mean_df.loc[cell_color]
            ax.plot(ss_mean_df_subset.index, ss_mean_df_subset[col], color=cell_color)
        ax.set(xlabel='Time', ylabel=col.replace('_',' ').title(), title='All Timepoints')
        fig.savefig(f'analysis/trait_{col}.alltps.png', dpi=300)
        # > plot before cell type singularity
        fig,ax = plt.subplots(figsize=[8,4])
        ax.grid(False)
        for cell_color in cell_colors:
            ss_mean_df_subset = ss_mean_df.loc[cell_color]
            ss_mean_df_subset = ss_mean_df_subset[ss_mean_df_subset.index <= timeshot_b4domination]
            ax.plot(ss_mean_df_subset.index, ss_mean_df_subset[col], color=cell_color)
        ax.set(xlabel='Time', ylabel=col.replace('_',' ').title(), title='Time till Cell Type Singularity')
        fig.savefig(f'analysis/trait_{col}.tpb4sctype.png', dpi=300)


if __name__ == '__main__':
    analyze_history()
    for fname in tqdm(glob('outputs/*.pkl')):
        convert_cells(fname)
    analyze_traits()
