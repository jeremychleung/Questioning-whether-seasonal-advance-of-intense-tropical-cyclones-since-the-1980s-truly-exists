# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 17:23:00 2025

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats

#%%
yrbeg = 1981
yrend = 2017
years = np.arange(yrbeg,yrend+1)
nyear = years.size

adt = pd.read_csv('../DataSets/ma_adt-hursat_lmi_time_leapyear.csv', index_col=False, keep_default_na=False, na_values='')
ibt = pd.read_csv('../DataSets/ma_ibtracs_lmi_time_leapyear.csv', index_col=False, keep_default_na=False, na_values='')

#%%
oceanbasin = ['NA','EP','WP','SP','SI']

df = pd.DataFrame(np.nan, index=years, columns=['adt_'+x.lower() for x in oceanbasin] + ['ibt_'+x.lower() for x in oceanbasin])
for iob,ob in enumerate(oceanbasin):
    #ADT-HURSAT
    cond1 = adt['basin'] == ob
    if ob in ['NA','EP','WP']:
        cond2 = adt['month'].isin([6,7,8,9,10,11])
    else:
        cond2 = adt['month'].isin([12,1,2,3,4])
    cond3 = adt['lmi'] > 110
    cond4 = adt['season'].isin(years)
    cond = cond1 & cond2 & cond3 & cond4

    adt_ob = adt[cond].reset_index(drop=True)

    #IBTrACS
    cond1 = ibt['basin'] == ob
    if ob in ['NA','EP','WP']:
        cond2 = ibt['month'].isin([6,7,8,9,10,11])
    else:
        cond2 = ibt['month'].isin([12,1,2,3,4])
    cond3 = ibt['lmi'] > 110
    cond4 = ibt['season'].isin(years)
    cond = cond1 & cond2 & cond3 & cond4

    ibt_ob = ibt[cond].reset_index(drop=True)

    #--------------------------------------------------------------------------
    adtset = set(adt_ob['sid'])
    ibtset = set(ibt_ob['sid'])
    comset = adtset & ibtset
    comsid = list(comset)
    comsid.sort()

    adtcom = adt[adt['sid'].isin(comsid)].reset_index(drop=True)
    ibtcom = ibt[ibt['sid'].isin(comsid)].reset_index(drop=True)

    for iyr,yr in enumerate(years):
        adt_yr = adtcom[adtcom['season'] == yr].reset_index(drop=True)
        if adt_yr.shape[0]:
            df.loc[yr,'adt_'+ob.lower()] = np.percentile(adt_yr['occurtime'].values, 50)

        ibt_yr = ibtcom[ibtcom['season'] == yr].reset_index(drop=True)
        if ibt_yr.shape[0]:
            df.loc[yr,'ibt_'+ob.lower()] = np.percentile(ibt_yr['occurtime'].values, 50)

    #--------------------------------------------------------------------------
    #ADT-HURSAT
    sr1 = df['adt_'+ob.lower()].dropna(axis='index')

    slope, intercept, rvalue, pvalue_ls, std_err = stats.linregress(sr1.index.values, sr1.values)
    res = mk.original_test(sr1.values, alpha=0.05)
    pvalue = res.p

    dof = sr1.size-2
    ppf = stats.t.ppf(1 - 0.05/2, dof)
    print(f'ADT-HURSAT->{ob:2s}, dof:{dof:2d}, slope:{slope*10:+.2f}±{ppf*std_err*10:.2f}, mk-test:{pvalue:.3f}, t-test:{pvalue_ls:.3f}')
    del sr1

    #IBTrACS
    sr2 = df['ibt_'+ob.lower()].dropna(axis='index')

    slope, intercept, rvalue, pvalue_ls, std_err = stats.linregress(sr2.index.values, sr2.values)
    res = mk.original_test(sr2.values, alpha=0.05)
    pvalue = res.p

    dof = sr2.size-2
    ppf = stats.t.ppf(1 - 0.05/2, dof)
    print(f'   IBTrACS->{ob:2s}, dof:{dof:2d}, slope:{slope*10:+.2f}±{ppf*std_err*10:.2f}, mk-test:{pvalue:.3f}, t-test:{pvalue_ls:.3f}')
    del sr2

    #corr coef between ADT-HURSAT and IBTrACS
    df12 = df[['adt_'+ob.lower(),'ibt_'+ob.lower()]].dropna(axis='index')
    slope, intercept, rvalue, pvalue_ls, std_err = stats.linregress(df12.iloc[:,0], df12.iloc[:,1])
    print(f' Corr.coef->{ob:2s}, r:{rvalue:+.2f}, t-test:{pvalue_ls:.3f}')

    print()

df.to_csv('oceanbasin_median_common.csv', index=True)