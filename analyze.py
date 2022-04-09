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
    df = pd.read_csv(f'outputs/{track_filename}.txt')
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
    columns = ['color', 'radius', 'center', 'age', 'health', 'metabolic_cost', 'direction_pause', 'direction_angle', 'cycle', 'direction_remember', 'vision_scale', 'vision_nconsidered', 'mutational_rate', 'mutation_information']
    ss_df = pd.DataFrame(columns = columns + ['timeshot'])
    for fname in tqdm(glob('outputs/*.csv')):
        ss_df_subset = pd.read_csv(fname, index_col=0)
        ss_df_subset['timeshot'] = int(fname.split('.')[-2])
        ss_df = ss_df.append(ss_df_subset)
    ss_df = ss_df.sort_values('timeshot')
    # get the timepoints
    def count(rows):
        return len(set(rows['color']))
    timeshot_nctypes = ss_df[['color','timeshot']].groupby('timeshot').apply(count)
    timeshot_b4domination = timeshot_nctypes[timeshot_nctypes > 1].index.max()
    # get the cell colors
    ss_mean_df = ss_df.groupby(['color','timeshot']).mean()
    colors = list(set([arr[0] for arr in ss_mean_df.index]))
    # get the plots
    for col in ss_mean_df.loc[colors[0]].columns:
        # > plot all timepoints
        fig,ax = plt.subplots(figsize=[8,4])
        ax.grid(False)
        for color in colors:
            ss_mean_df_subset = ss_mean_df.loc[color]
            ax.plot(ss_mean_df_subset.index, ss_mean_df_subset[col], color=color)
        ax.set(xlabel='Time', ylabel=col.replace('_',' ').title(), title='All Timepoints')
        fig.savefig(f'analysis/trait_{col}.alltps.png', dpi=300)
        # > plot before cell type singularity
        fig,ax = plt.subplots(figsize=[8,4])
        ax.grid(False)
        for color in colors:
            ss_mean_df_subset = ss_mean_df.loc[color]
            ss_mean_df_subset = ss_mean_df_subset[ss_mean_df_subset.index <= timeshot_b4domination]
            ax.plot(ss_mean_df_subset.index, ss_mean_df_subset[col], color=color)
        ax.set(xlabel='Time', ylabel=col.replace('_',' ').title(), title='Time till Cell Type Singularity')
        fig.savefig(f'analysis/trait_{col}.tpb4sctype.png', dpi=300)


if __name__ == '__main__':
    analyze_history()
    for fname in tqdm(glob('outputs/*.pkl')):
        convert_cells(fname)
    analyze_traits()
