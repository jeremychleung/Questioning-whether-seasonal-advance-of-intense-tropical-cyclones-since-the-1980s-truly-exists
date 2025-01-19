# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:11:07 2025

@author: meteo
"""

import pandas as pd

#%%
oceanbasin = ['NA','EP','WP','SI','SP']

df = pd.DataFrame()
for iob,ob in enumerate(oceanbasin):
    temp = pd.read_csv('../fig1/itc_in_datasets.'+ob.lower()+'.csv', index_col=False)
    temp['basin'] = ob
    df = pd.concat([df,temp], axis=0, ignore_index=True)
    del temp

df.drop('season', axis=1, inplace=True)

#%%
dfsum = df.groupby('basin').sum()
df_gl = dfsum.sum()
df_nh = dfsum.loc[['NA','EP','WP']].sum()
df_sh = dfsum.loc[['SI','SP']].sum()