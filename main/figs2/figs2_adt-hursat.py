# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 19:53:02 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
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
yrbeg = 1981
yrend = 2017
years = np.arange(yrbeg,yrend+1)
nyear = years.size

adt = pd.read_csv('../DataSets/ma_adt-hursat_lmi_time_leapyear.csv', index_col=False, keep_default_na=False, na_values='')

#%%
fig,axs = plt.subplots(1,2,figsize=(12,4.1))
fig.subplots_adjust(left=0.08, bottom=0.25, right=0.95, top=0.92,wspace=0.25)

months = np.arange(1,13)
for isph,sph in enumerate(['NH','SH']):
    counts = np.zeros([nyear,12], dtype=np.int32)
    regb = np.full(12,fill_value=np.nan)
    regp = np.full_like(regb, fill_value=np.nan)
    regse = np.full_like(regb, fill_value=np.nan)

    if sph == 'NH':
        cond1 = adt['basin'].isin(['NA','EP','WP'])
    elif sph == 'SH':
        cond1 = adt['basin'].isin(['SI','SP'])

    cond2 = adt['lmi'] > 110
    for imo,mo in enumerate(months):
        cond3 = adt['month'] == mo
        for iyr,yr in enumerate(years):
            cond4 = adt['year'] == yr

            cond = cond1 & cond2 & cond3 & cond4

            df = adt[cond].reset_index(drop=True)
            counts[iyr,imo] = df.shape[0]

        x = years
        y = counts[:,imo]
        slope,intecept,rvalue,pvalue,std_err = stats.linregress(x,y)

        res = mk.original_test(y,alpha=0.05)
        pvalue = res.p

        regb[imo] = slope*10
        regp[imo] = pvalue

        dof = x.size-2
        ppf = stats.t.ppf(1 - 0.05/2, dof)
        regse[imo] = ppf*std_err*10

    #output
    df_counts = pd.DataFrame(data=counts,index=years,columns=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])
    df_counts.to_csv('count_'+sph.lower()+'.csv')

    counts_sum = np.sum(counts,axis=0)

    #
    if sph == 'SH':
        temp = regb.copy()
        regb[:6] = temp[6:]
        regb[6:] = temp[:6]

        temp = regp.copy()
        regp[:6] = temp[6:]
        regp[6:] = temp[:6]

        temp = regse.copy()
        regse[:6] = temp[6:]
        regse[6:] = temp[:6]

        temp = counts_sum.copy()
        counts_sum[:6] = temp[6:]
        counts_sum[6:] = temp[:6]

    #plot
    blab = []
    for imo,mo in enumerate(months):
        if regp[imo]<=0.01:
            star = '***'
        elif regp[imo]<=0.05:
            star = '**'
        elif regp[imo]<=0.10:
            star = '*'
        else:
            star = ''
        blab.append(star)
    blab = np.array(blab)

    colors = ['#FF5E48' if v > 0 else '#6BCCFF' for v in regb]
    colors = np.array(colors)

    ax = axs[isph]
    ind = regb<0
    bb = ax.bar(months[ind],regb[ind],yerr=regse[ind],color=colors[ind],edgecolor='k',capsize=6,label='Trend')
    ax.bar_label(bb, labels=blab[ind], fontsize=25, padding=2)
    ind = ~ind
    bb = ax.bar(months[ind],regb[ind],yerr=regse[ind],color=colors[ind],edgecolor='k',capsize=6,label='Trend')
    ax.bar_label(bb, labels=blab[ind], fontsize=25, padding=-13)

    ax.hlines(0,-1,13,color='k',linewidth=1)

    ax.set_xlim([0.5,12.5])
    if sph == 'NH':
        ax.set_xticks(months-0.5)
        ax.set_xticklabels(['January','February','March','April','May','June',
                            'July','August','September','October','November','December'],rotation=45)
        ax.set_yticks(np.arange(-1,1.5,0.5))
        ax.set_ylim([-1,1])
        ax.set_ylabel('Trend in annual number of \n intense TCs (per decade)', fontsize=13)
    else:
        ax.set_xticks(months-0.5)
        ax.set_xticklabels(['July(-1)','August(-1)','September(-1)','October(-1)','November(-1)','December(-1)',
                            'January(0)','February(0)','March(0)','April(0)','May(0)','June(0)',],rotation=45)
        ax.set_yticks(np.arange(-0.5,0.7,0.2))
        ax.set_ylim([-0.5,0.5])

    ax.tick_params(labelsize=12)

    ax2 = ax.twinx()
    line2, = ax2.plot(months,counts_sum,marker='.',markersize=14,color='k',label='Climatology')

    lg = plt.legend(loc=[0.032,0.79],frameon=False,prop={'size':12})
    ax.hlines(0.8485,0.03,0.131,color='k',transform=ax.transAxes)

    ax.plot([0.03,0.13,0.13,0.03,0.03],[0.90,0.90,0.96,0.96,0.90],color='k',linewidth=1,transform=ax.transAxes)
    ax.text(0.15,0.91,'Trend',fontsize=12,transform=ax.transAxes)

    if sph == 'NH':
        ax2.set_ylim([0,130])
    else:
        ax2.set_ylim([0,55])
        ax2.set_ylabel('Total number of intense TCs',fontsize=13)

    ax2.tick_params(labelsize=12)

    ax.text(-0.15,1.01,chr(97+isph),transform=ax.transAxes,fontdict={'weight':'bold','size':25})

fig.savefig('figs2_adt-hursat.png', dpi=500)