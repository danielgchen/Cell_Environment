# import packages
import pandas as pd
import matplotlib.pyplot as plt
# import constants
from constants import *

'''
reads in the tracking file and outputs out a plot of the cells across time
'''

def analyze_history():
    # read in data
    df = pd.read_csv(track_filename)
    # define clones present
    clones = df['clone'].unique()
    # plot lines
    fig,ax = plt.subplots(figsize=[8,4])
    for clone in clones:
        plot_df = df.loc[df['clone']==clone]
        ax.plot(plot_df.index, plot_df['count'], color=clone)
    fig.tight_layout()
    fig.savefig(track_filename.replace('.txt','_analysis.png'), dpi=300)

if __name__ == '__main__':
    analyze_history()
