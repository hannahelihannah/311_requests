# Import packages
import codecs
import json
from typing import Callable, Coroutine, List
import asyncio
from os import path

import aiohttp
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
sns.set_palette('PuBu')

import matplotlib.ticker as ticker
import pandas as pd
from matplotlib.pyplot import figure
from datetime import datetime

# Import the data export from the previous phase
all_311 = pd.read_csv('all_311.csv')

# EDA on NaNs by tract

# Get a count of rows where the final tract is nan
# TODO based on these values - identify if there are other numeric checks that can be added before the
# TODO join to improve the quality of the matches that are found

def hue_order(source_df, colorcol):
    for cls in source_df['nullcol'].unique():
        temp_df = source_df[source_df['nullcol'] == cls]
        order = temp_df.sort_values('Count', ascending = False)[colorcol]
        return order


def create_barplot(source_df, nulltestcol, title, xtitle, ytitle, colorcol=None):
    fig, ax = plt.subplots(figsize=(7,5))

    if colorcol == None:
        nans = pd.DataFrame(pd.DataFrame(np.where(pd.isnull(source_df[nulltestcol].values), 'Null', 'Not Null')).value_counts())
        nans.columns = [xtitle]
        nans = nans.reset_index()
        nans.columns = [ytitle, xtitle]

        # Plot the NaNs
        sns.barplot(x=xtitle, y=ytitle, data=nans, palette="Blues")
        ax.set(xlim=(0, 1500000))
        ax.set_ylabel('Tract Join Status', fontsize=12, alpha=0.75)
        ax.set_xlabel('311 Request Count', fontsize=12, alpha=0.75)
        ax.xaxis.set_major_formatter(ticker.EngFormatter())
        for p in ax.patches:
            width = p.get_width()
            ax.text(width + 1000,
                    p.get_y() + p.get_height() / 2,
                    '{:,} ({:.0%})'.format(int(width), int(width)/len(source_df)),
                    ha='left',
                    va='center',
                    fontsize=10)
        ax.text(x=0.5, y=1.10, s=title, fontsize=16,
                ha='center', va='bottom', transform=ax.transAxes, fontweight='bold')
        ax.text(x=0.5, y=1.05, s='Labels are formatted as "N (% of total 311 requests)"',
                fontsize=10, alpha=0.75, ha='center',
                va='bottom', transform=ax.transAxes)

    else:
        source_df['nullcol'] = pd.DataFrame(np.where(pd.isnull(source_df[nulltestcol].values), 'Null', 'Not Null'))
        nans = source_df[['nullcol', colorcol]]
        nangroup = nans.groupby(['nullcol'])[colorcol].value_counts().reset_index(name='Count')
        nangroup[colorcol] = nangroup[colorcol].astype(int)
        sns.barplot(x='Count', y='nullcol', data=nangroup, hue=colorcol,
                    hue_order=hue_order(nangroup, colorcol), palette="Blues")
        ax.set(xlim=(0, 250000))
        ax.text(x=0.5, y=1.10, s=title, fontsize=16,
                ha='center', va='bottom', transform=ax.transAxes, fontweight='bold')
        ax.text(x=0.5, y=1.05, s='Labels are formatted as "N (% of total 311 requests)"',
                fontsize=10, alpha=0.75, ha='center',
                va='bottom', transform=ax.transAxes)
        h, l = ax.get_legend_handles_labels()
        ax.legend(h, l, bbox_to_anchor=(1.05, 1), loc=2, fontsize=10)
        ax.set_ylabel('Tract Join Status', fontsize=12, alpha=0.75)
        ax.set_xlabel('311 Request Count', fontsize=12, alpha=0.75)

        ax.xaxis.set_major_formatter(ticker.EngFormatter())

        for p in ax.patches:
            width = p.get_width()
            ax.text(width + 1000,
                    p.get_y() + p.get_height() / 2,
                    '{:,} ({:.0%})'.format(int(width), int(width)/len(nans)),
                    ha='left',
                    va='center',
                    fontsize=10)

    ax.tick_params(labelsize=10)
    fig.tight_layout()
    ax.figure.savefig(f'{title}.png')
    plt.show()
    print(f'Finished creating barplot {title}.')

# Import ACS Data Files
acs_demo = pd.read_csv('ACS_Demographic_Characteristics_DC_Census_Tract.csv')
acs_soc = pd.read_csv('ACS_Social_Characteristics_DC_Census_Tract.csv')
acs_econ = pd.read_csv('ACS_Economic_Characteristics_DC_Census_Tract.csv')
acs_hous = pd.read_csv('ACS_Housing_Characteristics_DC_Census_Tract.csv')
print('Finished importing ACS files by ward and tract.')


def main():
    # Create bar plot for Nans Overall
    create_barplot(all_311, 'tract', 'Tract Non-Matches (Overall)', 'Count', 'Status')
    # Bar plot for nans by Ward
    create_barplot(all_311, 'tract', 'Tract Non-Matches (Ward)', 'Status', 'Count', colorcol='WARD')
    print('Created overall null tract barplot.')



if __name__ == '__main__':
    main()