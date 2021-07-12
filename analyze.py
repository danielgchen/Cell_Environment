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
def convert_cells():
    # read in data
    data = pickle.load(open(track_filename + '.pkl','rb'))
    # separate out the genetics from attributes
    annos = [{'cell_color':val[0],'cell_age':val[1],'cell_center':val[2], 'cell_radius':val[3]} for val in data]
    data = [val[4] for val in data]
    # convert to dataframe
    df_data = pd.DataFrame(data)
    df_annos = pd.DataFrame(annos)
    # combine and write
    df = pd.concat([df_annos, df_data], axis=1)
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
