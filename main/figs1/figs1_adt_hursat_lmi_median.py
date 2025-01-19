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
import statsmodels.api as sm
from scipy import stats
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
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

df = pd.read_csv('../DataSets/ma_adt-hursat_lmi_time_leapyear.csv', index_col=False, keep_default_na=False, na_values='')

windlimit = np.array([34,64,80,90,100,110,120,130])
nwind = windlimit.size

#%%
fig = plt.figure(figsize=(7,4.5))
gs = GridSpec(2,2,width_ratios=[1,1],height_ratios=[1,1],
              left=0.11, bottom=0.10, right=0.98, top=0.95, wspace=0.30,hspace=0.45)

ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax4 = plt.subplot(gs[3])

ax1.text(-0.19,1.02,chr(97),fontdict={'weight':'bold','size':16}, transform=ax1.transAxes)
ax2.text(-0.19,1.02,chr(98),fontdict={'weight':'bold','size':16}, transform=ax2.transAxes)
ax3.text(-0.19,1.02,chr(99),fontdict={'weight':'bold','size':16}, transform=ax3.transAxes)
ax4.text(-0.19,1.02,chr(100),fontdict={'weight':'bold','size':16}, transform=ax4.transAxes)

#%%  1,top left
cond1 = df['basin'].isin(['NA','WP','EP'])
cond2 = df['month'].isin([6,7,8,9,10,11])
lc = ['r','k']
for iw,w in enumerate([110,115]):
    cond3 = df['lmi'] > w

    yr50th = np.full(nyear, fill_value=np.nan)
    for iyr,yr in enumerate(years):
        cond4 = df['season'] == yr
        cond = cond1 & cond2 & cond3 & cond4
        df50th = df[cond].copy()
        if df50th.shape[0] == 0: continue

        tvalue = df50th['occurtime'].values
        yr50th[iyr] = np.percentile(tvalue,50)

    # trend
    k = ~np.isnan(yr50th)
    x = years[k]
    y = yr50th[k]

    sns.regplot(x=x, y=y,ci=95,color=lc[iw],scatter=False,line_kws={'linewidth':2},ax=ax1)
    ax1.plot(years,yr50th,color=lc[iw],linestyle='--',linewidth=1)

    ax1.set_xticks(np.arange(1980,2030,10))
    ax1.set_xticks(np.arange(1980,2030,2), minor=True)
    ax1.set_yticks(nhdays)
    ax1.set_yticklabels(['1 January','1 February','1 March','1 April','1 May','1 June','1 July','1 August','1 September','1 October','1 November','1 December'])
    ax1.tick_params(labelsize=8)
    ax1.set_xlabel('Year', fontsize=10)
    ax1.set_xlim([1980,2021])
    ax1.set_ylim([224,287])
    ax1.invert_yaxis()
    ax1.set_title('ADT-HURSAT, NH', loc='left',fontsize=9,pad=3)

    slope, intercept, rvalue, pvalue_ls, std_err = stats.linregress(x,y)
    res = mk.original_test(yr50th,alpha=0.05)
    pvalue = res.p
    if pvalue<=0.01:
        star = '***'
    elif pvalue<=0.05:
        star = '**'
    elif pvalue<=0.10:
        star = '*'
    else:
        star = ''
    ax1.text(0.04,0.89-0.09*iw,f'slope$_{{{w}}}$: '+f'{slope*10:+.2f}d/decade{star:s}', fontsize=8, color=lc[iw], transform=ax1.transAxes)

    dof = x.size-2
    ppf = stats.t.ppf(1 - 0.05/2, dof)
    print('dof:',dof)
    print(f'ADT-NH slope:{slope*10:+.2f}±{ppf*std_err*10:.2f}, mk-test:{pvalue:.3f}, t-test:{pvalue_ls:.3f}')

#%% 3,bottom left
cond1 = df['basin'].isin(['SI','SP'])
cond2 = df['month'].isin([12,1,2,3,4])
lc = ['r','k']
for iw,w in enumerate([110,115]):
    cond3 = df['lmi'] > w

    yr50th = np.full(nyear, fill_value=np.nan)
    for iyr,yr in enumerate(years):
        cond4 = df['season'] == yr
        cond = cond1 & cond2 & cond3 & cond4
        df50th = df[cond].copy()
        if df50th.shape[0] == 0: continue

        tvalue = df50th['occurtime'].values
        yr50th[iyr] = np.percentile(tvalue,50)

    # trend
    k = ~np.isnan(yr50th)
    x = years[k]
    y = yr50th[k]

    sns.regplot(x=x, y=y,ci=95,color=lc[iw],scatter=False,line_kws={'linewidth':2},ax=ax3)
    ax3.plot(years,yr50th,color=lc[iw],linestyle='--',linewidth=1)

    ax3.set_xticks(np.arange(1980,2030,10))
    ax3.set_xticks(np.arange(1980,2030,2), minor=True)
    ax3.set_yticks(shdays)
    ax3.set_yticklabels(['1 July','1 August','1 September(-1)','1 October(-1)','1 November(-1)','1 December(-1)','1 January','1 February','1 March','1 April','1 May','1 June'])
    ax3.tick_params(labelsize=8)
    ax3.set_xlabel('Year', fontsize=10)
    ax3.set_xlim([1980,2021])
    ax3.set_ylim([155,278])
    ax3.invert_yaxis()
    ax3.set_title('ADT-HURSAT, SH', loc='left',fontsize=10,pad=3)

    slope, intercept, rvalue, pvalue_ls, std_err = stats.linregress(x,y)
    res = mk.original_test(yr50th,alpha=0.05)
    pvalue = res.p
    if pvalue<=0.01:
        star = '***'
    elif pvalue<=0.05:
        star = '**'
    elif pvalue<=0.10:
        star = '*'
    else:
        star = ''
    ax3.text(0.04,0.89-0.09*iw,f'slope$_{{{w}}}$: '+f'{slope*10:+.2f}d/decade{star:s}', fontsize=8, color=lc[iw], transform=ax3.transAxes)

    dof = x.size-2
    ppf = stats.t.ppf(1 - 0.05/2, dof)
    print('dof:',dof)
    print(f'ADT-SH slope:{slope*10:+.2f}±{ppf*std_err*10:.2f}, mk-test:{pvalue:.3f}, t-test:{pvalue_ls:.3f}')

#%%  2,top right
cond1 = df['basin'].isin(['NA','WP','EP'])
cond2 = df['month'].isin([6,7,8,9,10,11])

trend = np.full(nwind,fill_value=np.nan)
ptest = np.full_like(trend, fill_value=np.nan)

ci_l = []
ci_u = []

for iw,wind in enumerate(windlimit):
    cond3 = df['lmi'] > wind

    wind50th = np.full(nyear, fill_value=np.nan)
    for iyr,yr in enumerate(years):
        cond4 = df['season'] == yr
        cond = cond1 & cond2 & cond3 & cond4
        if np.sum(cond)==0: continue

        wind50th[iyr] = np.percentile(df[cond]['occurtime'],50)

    k = ~np.isnan(wind50th)
    x = years[k]
    y = wind50th[k]

    slope, intercept, r_value, pvalue_ls, std_err = stats.linregress(x,y)
    trend[iw] = slope*10

    res = mk.original_test(wind50th,alpha=0.05)
    ptest[iw] = res.p

    X = sm.add_constant(x)
    model = sm.OLS(y,X).fit()
    ci = model.conf_int()[1,:]
    ci_l.append(ci[0]*10)
    ci_u.append(ci[1]*10)

ax2.axhline(0,0,6,color='gray',linestyle='--')

ax2.plot(windlimit, trend, color='k', marker='o', markerfacecolor='w')
ax2.plot(windlimit[ptest<=0.05], trend[ptest<=0.05], color='k', linestyle='none',marker='o', markerfacecolor='k')
ax2.fill_between(windlimit,ci_l,ci_u,color='#deebfa')
ax2.set_xticks(np.arange(20,160,20))
ax2.set_xticklabels([str(w) for w in np.arange(20,160,20)])
ax2.set_xticks(np.arange(20,160,10), minor=True)
ax2.tick_params(labelsize=8)
ax2.set_xlabel('Intensity [knot]', fontsize=11)
ax2.set_ylabel('Trend [d/decade]', fontsize=11)
ax2.set_xlim([30,140])
ax2.set_ylim([-15,5])
ax2.set_title('ADT-HURSAT, NH', loc='left',fontsize=10,pad=3)

#%%  4,bottom right
cond1 = df['basin'].isin(['SI','SP'])
cond2 = df['month'].isin([12,1,2,3,4])

trend = np.full(nwind,fill_value=np.nan)
ptest = np.full_like(trend, fill_value=np.nan)

ci_l = []
ci_u = []

for iw,wind in enumerate(windlimit):
    cond3 = df['lmi'] > wind

    wind50th = np.full(nyear, fill_value=np.nan)
    for iyr,yr in enumerate(years):
        cond4 = df['season'] == yr
        cond = cond1 & cond2 & cond3 & cond4
        if np.sum(cond)==0: continue

        wind50th[iyr] = np.percentile(df[cond]['occurtime'],50)

    k = ~np.isnan(wind50th)
    x = years[k]
    y = wind50th[k]

    slope, intercept, r_value, pvalue_ls, std_err = stats.linregress(x,y)
    trend[iw] = slope*10

    res = mk.original_test(wind50th,alpha=0.05)
    ptest[iw] = res.p

    X = sm.add_constant(x)
    model = sm.OLS(y,X).fit()
    ci = model.conf_int()[1,:]
    ci_l.append(ci[0]*10)
    ci_u.append(ci[1]*10)

ax4.axhline(0,0,6,color='gray',linestyle='--')

ax4.plot(windlimit, trend, color='k', marker='o', markerfacecolor='w')
ax4.plot(windlimit[ptest<=0.05], trend[ptest<=0.05], color='k', linestyle='none',marker='o', markerfacecolor='k')
ax4.fill_between(windlimit,ci_l,ci_u,color='#deebfa')
ax4.set_xticks(np.arange(20,160,20))
ax4.set_xticklabels([str(w) for w in np.arange(20,160,20)])
ax4.set_xticks(np.arange(20,160,10), minor=True)
ax4.tick_params(labelsize=8)
ax4.set_xlabel('Intensity [knot]', fontsize=11)
ax4.set_ylabel('Trend [d/decade]', fontsize=11)
ax4.set_xlim([30,140])
ax4.set_ylim([-20,10])
ax4.set_title('ADT-HURSAT, SH', loc='left',fontsize=10,pad=3)

#%%
fig.savefig('figs1_adt_hursat_lmi_median.png', dpi=500)