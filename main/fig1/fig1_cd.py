# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 02:59:35 2024

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

df = pd.read_csv('fig1_cd_wind_diff.csv', keep_default_na=False)

#%%
fig,axs = plt.subplots(1,2,figsize=(10.1,3.2))
fig.subplots_adjust(left=0.05, bottom=0.13, right=0.98, top=0.91, wspace=0.18)

for isph,sph in enumerate(['NH','SH']):
    ax = axs[isph]
    if sph == 'NH':
        cond1 = df['basin'].isin(['NA','EP','WP'])
    elif sph == 'SH':
        cond1 = df['basin'].isin(['SP','SI'])

    diff = np.full(nyear, fill_value=np.nan)
    sigma = np.full_like(diff, fill_value=np.nan)

    diff_lmi = np.full(nyear, fill_value=np.nan)
    sigma_lmi = np.full_like(diff_lmi, fill_value=np.nan)
    for iyr,yr in enumerate(years):
        cond2 = df['season'] == yr
        cond = cond1 & cond2

        n = np.sum(cond)
        if n==0: continue

        diff[iyr] = df[cond]['wdiff'].mean()
        sigma[iyr] = np.std(df[cond]['wdiff'])

        x = df[cond]['adt_lmi'].values
        y = df[cond]['ibt_lmi'].values
        z = x - y
        diff_lmi[iyr] = np.mean(z)
        sigma_lmi[iyr] = np.sqrt(np.var(z))

    line1, = ax.plot(years,diff,color='C0',linewidth=2,label='ALL')
    ub = diff + sigma
    lb = diff - sigma
    ax.fill_between(years,ub,lb,color='C0',alpha=0.2)

    line2, = ax.plot(years,diff_lmi,color='C3',linewidth=2,label='LMI')
    ub = diff_lmi + sigma_lmi
    lb = diff_lmi - sigma_lmi
    ax.fill_between(years,ub,lb,color='C3',alpha=0.2)

    lg = ax.legend([line1,line2],['ALL','LMI'])

    ax.hlines(0,1980,2020,color='gray',linestyle='--')

    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ax.set_xticks(np.arange(1980,yrend+1,10))
    ax.set_xticks(np.arange(1980,yrend+1,1),minor=True)

    ax.set_yticks(np.arange(-100,100,5),minor=True)
    ax.tick_params(labelsize=10)

    ax.set_xlim([1980,2017])
    ax.set_ylim([-20,28])

    ax.set_xlabel('Year',fontsize=12,labelpad=0.8)
    ax.set_ylabel('Difference [knot]',fontsize=12,labelpad=0.8)
    ax.set_title(sph,fontsize=13,pad=4.2)

    ax.text(-0.09,1.01,chr(99+isph), fontdict={'weight':'bold','size':24}, transform=ax.transAxes)

fig.savefig('fig1_cd.png', dpi=500)