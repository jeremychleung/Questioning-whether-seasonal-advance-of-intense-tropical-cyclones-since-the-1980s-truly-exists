# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 15:21:10 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Helvetica'
rcParams['xtick.top'] = 'False'
rcParams['ytick.right'] = 'False'
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['hatch.color'] = 'k'
rcParams['hatch.linewidth'] = 0.6
rcParams['mathtext.fontset'] = 'stix'
rcParams['mathtext.default'] = 'regular'

#%%
yrsrt = 1981
yrend = 2017
years = np.arange(yrsrt,yrend+1)
nyear = years.size

oceanbasin = ['NA','EP','WP','SP','SI']

for isph,sph in enumerate(['NH','SH']):
    if sph == 'NH':
        df1 = pd.read_csv('itc_in_datasets.na.csv')
        df2 = pd.read_csv('itc_in_datasets.ep.csv')
        df3 = pd.read_csv('itc_in_datasets.wp.csv')
        df = df1 + df2 + df3
        df = df.reset_index(drop=True)
    elif sph == 'SH':
        df1 = pd.read_csv('itc_in_datasets.sp.csv')
        df2 = pd.read_csv('itc_in_datasets.si.csv')
        df = df1 + df2
        df = df.reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(5,3.7))
    fig.subplots_adjust(left=0.09, bottom=0.35, right=0.98, top=0.92)
    bottom = np.zeros(nyear)

    width = 0.5
    bcolors = ['#ED7D31','#A5A5A5','#FFC000','#70AD47','#4472C4']
    for i,icol in enumerate([4,5,6,7,3]):
        height = df.iloc[:,icol]
        p = ax.bar(years, height, width, color=bcolors[i], alpha=0.5, label=False, bottom=bottom)
        bottom += height

    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

    ax.set_xticks(np.arange(1980,yrend+1,10))
    ax.set_xticks(np.arange(1980,yrend+1,1),minor=True)
    ax.tick_params(labelsize=10)

    ax.set_xlabel('Year',fontsize=12,labelpad=0.8)
    ax.set_ylabel('Intense TC Counts',fontsize=12,labelpad=0.8)
    ax.set_title(sph,fontsize=13,pad=4.2)

    lg1 = ax.legend(loc=[-0.03,-0.62],labels=['Detected in IBTrACS, but not recorded in ADT-HURSAT',
                                             'Detected in ADT-HURSAT, but not recorded in IBTrACS',
                                             'Detected in IBTrACS, but not reaching intense TC category in ADT-HURSAT',
                                             'Detected in ADT-HURSAT, but not reaching intense TC category in IBTrACS',
                                             'Detected in both datasets'], frameon=False,mode='expand',ncol=1,prop={'size':9})

    ymin,ymax = ax.get_ylim()

    ax.set_xlim([1980,2018])
    if isph == 0:
        ax.set_yticks(np.arange(0,50,5))
        ax.set_ylim([0,24])
    elif isph == 1:
        ax.set_yticks(np.arange(0,50,5))
        ax.set_ylim([0,12])

    line1, = ax.plot(years, df.iloc[:,1],color='r',label='IBTrACS',linewidth=2.0)
    line2, = ax.plot(years, df.iloc[:,2],color='k',label='ADT-HURSAT',linewidth=2.0)
    lg2 = ax.legend([line1,line2],['IBTrACS','ADT-HURSAT'],loc='upper left',prop={'size':9})
    fig.gca().add_artist(lg1)

    ax.text(-0.09,1.01,chr(97+isph),transform=ax.transAxes,fontdict={'weight':'bold','size':24})

    fig.savefig('fig1_'+chr(97+isph)+'.png', dpi=600)
    plt.show()
    fig.clf()