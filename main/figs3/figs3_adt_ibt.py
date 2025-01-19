# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:20:05 2023

@author: Jimmy Liu, UCAS&LZU
"""

import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import pymannkendall as mk
from scipy import stats
from matplotlib import pyplot as plt
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
#north hemishpere days
nhdays = []
for mo in np.arange(1,13):
    dtdiff = datetime.datetime(2023,mo,1,0,0,0) - datetime.datetime(2023,1,1,0,0,0)
    nhdays.append(dtdiff.total_seconds()/(24*60*60))

#south hemishpere days
shdays = []
for mo in np.arange(7,13):
    dtdiff = datetime.datetime(2022,mo,1,0,0,0) - datetime.datetime(2022,7,1,0,0,0)
    shdays.append(dtdiff.total_seconds()/(24*60*60))
for mo in np.arange(1,7):
    dtdiff = datetime.datetime(2023,mo,1,0,0,0) - datetime.datetime(2022,7,1,0,0,0)
    shdays.append(dtdiff.total_seconds()/(24*60*60))

#%%
yrbeg = 1981
yrend = 2017
years = np.arange(yrbeg,yrend+1)
nyear = years.size

bstmedian = pd.read_csv('../tabs1/oceanbasin_median.csv', index_col=0, keep_default_na=False, na_values='')

#%%
oceanbasin = ['NA','EP','WP','SP','SI']

for ida,da in enumerate(['adt','ibt']):
    fig,axs = plt.subplots(5,1,figsize=(3.7,7.5))
    fig.subplots_adjust(left=0.20, bottom=0.05, right=0.96, top=0.97, hspace=0.3)

    for iob,ob in enumerate(oceanbasin):
        ax = axs[iob]

        sr = bstmedian[da+'_'+ob.lower()]

        # trend
        x = sr.index.values
        y = sr.values

        sns.regplot(x=x, y=y,ci=95,color='k',scatter=False,line_kws={'linewidth':2},seed=10,ax=ax)
        ax.plot(x,y,color='k',linestyle='--',linewidth=1)

        ax.set_xticks(np.arange(1980,2030,10))
        ax.set_xticks(np.arange(1980,2030,2),minor=True)
        ax.set_xlabel('Year', fontsize=10)
        if iob!=4:
            ax.set_xticklabels([])
            ax.set_xlabel('', fontsize=10)

        if ob in ['NA','EP','WP']:
            ax.set_yticks(nhdays)
            ax.set_yticklabels(['1 January','1 February','1 March','1 April','1 May','1 June','1 July','1 August','1 September','1 October','1 November','1 December'])
        elif ob in ['SP','SI']:
            ax.set_yticks(shdays)
            ax.set_yticklabels(['1 July','1 August','1 September','1 October','1 November','1 December','1 January','1 February','1 March','1 April','1 May','1 June'])

        ax.tick_params(labelsize=8)

        ax.set_xlim([1980,2020])
        if ob == 'NA':
            ax.set_ylim([224,312])
        elif ob == 'EP':
            ax.set_ylim([165,300])
        elif ob == 'WP':
            ax.set_ylim([195,305])
        elif ob == 'SP':
            ax.set_ylim([160,310])
        elif ob == 'SI':
            ax.set_ylim([145,298])

        ax.invert_yaxis()
        ax.set_title(f'ADT-HURSAT, {ob:2s}' if ida==0 else f'IBTrACS, {ob:2s}', loc='left',fontsize=9,pad=3)

        sr = sr.dropna()
        x = sr.index.values
        y = sr.values
        slope, intercept, rvalue, pvalue, std_err = stats.linregress(x,y)
        res = mk.original_test(y,alpha=0.05)
        pvalue = res.p
        if pvalue<=0.01:
            star = '***'
        elif pvalue<=0.05:
            star = '**'
        elif pvalue<=0.10:
            star = '*'
        else:
            star = ''
        ax.text(0.06,0.85,f'{slope*10:+.2f}d/decade{star:s}', fontdict={'weight':'normal','color':'k'},fontsize=9, transform=ax.transAxes)

        ax.text(-0.10,1.04,chr(97+iob*2+ida), transform=ax.transAxes, fontdict={'weight':'bold','size':17})

    fig.savefig('figs3_'+da+'.png', dpi=500)