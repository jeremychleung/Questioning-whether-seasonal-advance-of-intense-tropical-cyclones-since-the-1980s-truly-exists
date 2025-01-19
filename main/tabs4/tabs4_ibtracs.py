# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 00:18:54 2025

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats

yrbeg = 2000
yrend = 2017
years = np.arange(yrbeg,yrend+1)
nyear = years.size

df = pd.read_csv('../DataSets/ma_ibtracs_lmi_time_leapyear.csv', index_col=False, keep_default_na=False, na_values='')

#%%
oceanbasin = ['NH','SH','NA','EP','WP','SI','SP']

cond1 = df['lmi'] > 110
for iob,ob in enumerate(oceanbasin):
    if ob == 'NH':
        cond2 = df['basin'].isin(['NA','EP','WP'])
    elif ob == 'SH':
        cond2 = df['basin'].isin(['SI','SP'])
    else:
        cond2 = df['basin'] == ob

    if ob in ['NH','NA','EP','WP']:
        cond3 = df['month'].isin([6,7,8,9,10,11])
    else:
        cond3 = df['month'].isin([12,1,2,3,4])

    sr = pd.Series(np.nan, index=years)
    for iyr,yr in enumerate(years):
        cond4 = df['season'] == yr
        cond = cond1 & cond2 & cond3 & cond4

        if cond.sum():
            sr[yr] = np.percentile(df[cond]['occurtime'].values, 50)

    sr = sr.dropna()
    x = sr.index.values
    y = sr.values
    slope, intercept, rvalue, pvalue_ls, std_err = stats.linregress(x,y)
    res = mk.original_test(y, alpha=0.05)
    pvalue = res.p

    dof = x.size-2
    ppf = stats.t.ppf(1 - 0.05/2, dof)
    print(f'{ob:2s}-> dof:{dof:2d}, slope:{slope*10:+.2f}±{ppf*std_err*10:.2f}, mk-test:{pvalue:.3f}, t-test:{pvalue_ls:.3f}')