# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 00:43:10 2024

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

#%%
oceanbasin = ['NA','EP','WP','SI','SP']

counts_tol = np.zeros([nyear,7], dtype=np.int32)

for iob,ob in enumerate(oceanbasin):
    #--------------------------------------------------------------------------
    #ADT-HURSAT
    cond1 = adt['basin'] == ob
    if ob in ['NA','EP','WP']:
        cond2 = adt['month'].isin([6,7,8,9,10,11])
    else:
        cond2 = adt['month'].isin([12,1,2,3,4])
    cond3 = adt['lmi'] > 110
    cond = cond1 & cond2 & cond3

    adt_intense = adt[cond].reset_index(drop=True)

    #--------------------------------------------------------------------------
    #IBTrACS
    cond1 = ibt['basin'] == ob
    if ob in ['NA','EP','WP']:
        cond2 = ibt['month'].isin([6,7,8,9,10,11])
    else:
        cond2 = ibt['month'].isin([12,1,2,3,4])
    cond3 = ibt['lmi'] > 110
    cond = cond1 & cond2 & cond3

    ibt_intense = ibt[cond].reset_index(drop=True)

    #--------------------------------------------------------------------------
    #Comparison
    counts = np.zeros([nyear,8], dtype=np.int32)
    counts[:,0] = years

    for iyr,yr in enumerate(years):
        cond = ibt_intense['season'] == yr
        ibtset = set(ibt_intense[cond]['sid'])

        cond = adt_intense['season'] == yr
        adtset = set(adt_intense[cond]['sid'])

        bothset = ibtset & adtset
        onlyibt = ibtset - adtset
        onlyadt = adtset - ibtset

        counts[iyr,1] = len(ibtset)
        counts[iyr,2] = len(adtset)
        counts[iyr,3] = len(bothset)

        for sid in onlyibt:
            if sid not in set(adt['sid']):
                counts[iyr,4] += 1  #not recorded in ADT-HURSAT, Type2
            else:
                counts[iyr,6] += 1  #recorded in ADT-HURSAT, but LMI is less than 110knot.

        for sid in onlyadt:
            if sid not in set(ibt['sid']):
                counts[iyr,5] += 1  #not recorded in IBTrACS, Type1
            else:
                counts[iyr,7] += 1  #recorded in IBTrACS, but LMI is less than 110knot.

    counts_df = pd.DataFrame(counts,columns=['season','ibt','adt','both','ibt_rec_only','adt_rec_only','ibt_lmi_only','adt_lmi_only'])
    counts_df.to_csv('itc_in_datasets.'+ob.lower()+'.csv',index=False)

    print(f'{ob}')
    print(counts.sum(axis=0))

    counts_tol += counts[:,1:]

print('-'*50)
print(counts_tol.sum(axis=0))