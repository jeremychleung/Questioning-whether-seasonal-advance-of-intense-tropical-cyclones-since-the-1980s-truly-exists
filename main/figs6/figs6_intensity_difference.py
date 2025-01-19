# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 00:43:10 2024

@author: meteo
"""

import re
import datetime
import numpy as np
import pandas as pd
from scipy import stats

#%%
yrsrt = 1981
yrend = 2017
years = np.arange(yrsrt,yrend+1)
nyear = years.size

#ADT-HURSAT
adt = pd.read_csv('../0#/0.adt_hursat_occurrence_time.csv',keep_default_na=False)

otime = []
for i in range(adt.shape[0]):
    ss = adt['season'][i]
    yr = adt['year'][i]
    mo = adt['month'][i]
    dy = adt['day'][i]
    hr = adt['hour'][i]
    lmilat = adt['lmilat'][i]

    if lmilat > 0:
        ddt = datetime.datetime(yr,mo,dy,hr,0,0) - datetime.datetime(ss,1,1,0,0,0)
    else:
        ddt = datetime.datetime(yr,mo,dy,hr,0,0) - datetime.datetime(ss-1,7,1,0,0,0)

    dday = ddt.total_seconds()/(24*3600)
    otime.append(dday)

adt['occurtime'] = otime

#IBTrACS
ibt = pd.read_csv('../0#/0.ibtracs_occurrence_time.csv',keep_default_na=False)

otime = []
for i in range(ibt.shape[0]):
    ss = ibt['season'][i]
    yr = ibt['year'][i]
    mo = ibt['month'][i]
    dy = ibt['day'][i]
    hr = ibt['hour'][i]
    lmilat = ibt['lmilat'][i]

    if lmilat > 0:
        ddt = datetime.datetime(yr,mo,dy,hr,0,0) - datetime.datetime(ss,1,1,0,0,0)
    else:
        ddt = datetime.datetime(yr,mo,dy,hr,0,0) - datetime.datetime(ss-1,7,1,0,0,0)

    dday = ddt.total_seconds()/(24*3600)
    otime.append(dday)

ibt['occurtime'] = otime


#%%
basins = ['NA','EP','WP','SP','SI']

for ib,basin in enumerate(basins):
    #ADT-HURSAT
    cond1 = adt['basin'] == basin
    if basin in ['NA','WP','EP']:
        cond2 = (adt['month'] >= 6) & (adt['month'] <= 11)
    else:
        cond2 = (adt['month'] == 12) | ((adt['month'] >= 1) & (adt['month'] <= 4))
    cond3 = adt['lmi'] > 110
    cond = cond1 & cond2 & cond3

    adt_intense = adt[cond].reset_index(drop=True)

    #IBTrACS
    cond1 = ibt['basin'] == basin
    if basin in ['NA','WP','EP']:
        cond2 = (ibt['month'] >= 6) & (ibt['month'] <= 11)
    else:
        cond2 = (ibt['month'] == 12) | ((ibt['month'] >= 1) & (ibt['month'] <= 4))
    cond3 = ibt['lmi'] > 110
    cond = cond1 & cond2 & cond3

    ibt_intense = ibt[cond].reset_index(drop=True)

    #percentile
    p50 = np.full([nyear,3], fill_value=np.nan)
    p50[:,0] = years

    for iyr,yr in enumerate(years):
        cond = ibt_intense['season'] == yr
        ibtset = set(ibt_intense[cond]['sid'])

        cond = adt_intense['season'] == yr
        adtset = set(adt_intense[cond]['sid'])

        diffset = ibtset - adtset

        if len(diffset)==0:continue

        print(basin,yr,len(diffset),diffset)
    print('-'*70)

'''
        ibtlist = []
        adtlist = []
        for i,isid in enumerate(bothset):
            ody = ibt_intense[ibt_intense['sid'] == isid]['occurtime'].values[0]
            ibtlist.append(ody)

            ody = adt_intense[adt_intense['sid'] == isid]['occurtime'].values[0]
            adtlist.append(ody)

        p50[iyr,1] = np.percentile(ibtlist,50)
        p50[iyr,2] = np.percentile(adtlist,50)

    k = ~np.isnan(p50[:,1])
    x = p50[k,0]
    y = p50[k,1]
    slope_ibt, intercept, r, p_ibt, se = stats.linregress(x, y)
    print(f'{basin} IBT slope:{slope_ibt*10:.2f}/dec 1.96se:{1.96*se*10:.2f} p-value:{p_ibt:.3f}')

    k = ~np.isnan(p50[:,2])
    x = p50[k,0]
    y = p50[k,2]
    slope_adt, intercept, r, p_adt, se = stats.linregress(x, y)
    print(f'{basin} ADT slope:{slope_adt*10:.2f}/dec 1.96se:{1.96*se*10:.2f} p-value:{p_adt:.3f}')

    p50 = pd.DataFrame(data=p50, columns=['year','ibt','adt'])
    p50.to_csv('common_'+basin.lower()+'.csv', index=False)

    cond = p50['ibt'].notnull() & p50['adt'].notnull()
    x = p50[cond]['ibt'].values
    y = p50[cond]['adt'].values

    n_elements = x.size

    corr = np.corrcoef(x,y)[0,1]
    slope, intercept, r, p, se = stats.linregress(x, y)
    print(f'{basin} n_elements:{n_elements:2d} corrcoef:{corr:.2f} p-value:{p:.2e}')
    print('-'*30)
'''