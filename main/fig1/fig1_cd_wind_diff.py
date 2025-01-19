# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 13:02:06 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd

#%%
yrbeg = 1981
yrend = 2017
years = np.arange(yrbeg,yrend+1)
nyear = years.size

adt = pd.read_csv('../DataSets/ma_adt-hursat_lmi_time_leapyear.csv', index_col=False, keep_default_na=False, na_values='')
ibt = pd.read_csv('../DataSets/ma_ibtracs_lmi_time_leapyear.csv', index_col=False, keep_default_na=False, na_values='')

ibt_all = ibt.copy()

#%%
oceanbasin = ['NA','WP','EP','SP','SI']

bothsid = []
for iob,ob in enumerate(oceanbasin):
    #ADT-HURSAT
    cond1 = adt['basin'] == ob
    cond2 = adt['season'].isin(years)
    if ob in ['NA','WP','EP']:
        cond3 = adt['month'].isin([6,7,8,9,10,11])
    else:
        cond3 = adt['month'].isin([12,1,2,3,4])
    cond4 = adt['lmi'] > 110
    cond = cond1 & cond2 & cond3 & cond4

    adt_intense = adt[cond].reset_index(drop=True)

    #IBTrACS
    cond1 = ibt['basin'] == ob
    cond2 = ibt['season'].isin(years)
    if ob in ['NA','WP','EP']:
        cond3 = ibt['month'].isin([6,7,8,9,10,11])
    else:
        cond3 = ibt['month'].isin([12,1,2,3,4])
    cond4 = ibt['lmi'] > 110
    cond = cond1 & cond2 & cond3 & cond4

    ibt_intense = ibt[cond].reset_index(drop=True)

    #common intense TC
    ibtset = set(ibt_intense['sid'])
    adtset = set(adt_intense['sid'])
    bothset = ibtset & adtset

    bothsid.extend(list(bothset))

bothsid.sort()

#%%
#ADT-HURSAT
adt = pd.read_csv('../DataSets/ADT-HURSAT/pnas_adt-hursat.csv', low_memory=False, keep_default_na=False, na_values='')
adt = adt.astype({'year':'int32','month':'int32','day':'int32','hour':'int32','lat':'float32','lon':'float32','spd':'float32'})
adt['ISO_TIME'] = pd.to_datetime(adt[['year','month','day','hour']])

#IBTrACS
ibt = pd.read_csv('../DataSets/IBTrACS/ibtracs.ALL.list.v04r01.csv', low_memory=False, keep_default_na=False, na_values=' ',
                  usecols=['SID','SEASON','BASIN','ISO_TIME','IFLAG','USA_LAT','USA_LON','USA_WIND','USA_SSHS'])
ibt.drop(index=0,inplace=True)
ibt = ibt.astype({'SEASON':'int32','ISO_TIME':'datetime64[ns]','USA_LAT':'float32','USA_LON':'float32','USA_WIND':'float32','USA_SSHS':'int32'})

cond1 = ibt['ISO_TIME'].dt.hour%6 == 0   #6-hour intervals
cond2 = ibt['IFLAG'].str.startswith('O') #observed data
cond = cond1 & cond2
ibt = ibt[cond].reset_index(drop=True)

#%%
wind_diff = pd.DataFrame(columns=['sid','season','basin','wdiff','adt_lmi','ibt_lmi'])

for i,isid in enumerate(bothsid):
    adt_tc = adt[adt['sid'] == isid][['ISO_TIME','spd']].reset_index(drop=True)
    ibt_tc = ibt[ibt['SID'] == isid][['ISO_TIME','USA_WIND']].reset_index(drop=True)

    adt_tc = adt_tc.dropna(axis='index')
    ibt_tc = ibt_tc.dropna(axis='index')

    w1_max = adt_tc['spd'].max()
    w2_max = ibt_tc['USA_WIND'].max()

    adt_tc_timeset = set(adt_tc['ISO_TIME'].values)
    ibt_tc_timeset = set(ibt_tc['ISO_TIME'].values)
    both_timeset = adt_tc_timeset & ibt_tc_timeset
    both_timeset = list(both_timeset)

    w1 = []
    w2 = []
    for idt in both_timeset:
        w1.append(adt_tc[adt_tc['ISO_TIME'] == idt]['spd'].values[0])
        w2.append(ibt_tc[ibt_tc['ISO_TIME'] == idt]['USA_WIND'].values[0])
    w1 = np.array(w1)
    w2 = np.array(w2)
    wdiff = np.mean(w1 - w2)

    ob = ibt_all[ibt_all['sid'] == isid]['basin'].values[0]
    season = ibt_all[ibt_all['sid'] == isid]['season'].values[0]
    temp = pd.DataFrame([[isid,season,ob,wdiff,w1_max,w2_max]],columns=['sid','season','basin','wdiff','adt_lmi','ibt_lmi'])

    wind_diff = pd.concat([wind_diff,temp], ignore_index=True)

wind_diff.to_csv('fig1_cd_wind_diff.csv', index=False)