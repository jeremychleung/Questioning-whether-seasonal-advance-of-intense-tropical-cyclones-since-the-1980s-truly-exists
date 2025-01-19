# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 16:03:29 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd

#%%
Sid = pd.read_csv('pnas.1920849117.sd07.csv')
Basin = pd.read_csv('pnas.1920849117.sd01.csv', keep_default_na=False)
Year = pd.read_csv('pnas.1920849117.sd09.csv',  na_values=['NA','NaN',' '])
Month = pd.read_csv('pnas.1920849117.sd06.csv',  na_values=['NA','NaN',' '])
Day = pd.read_csv('pnas.1920849117.sd02.csv',  na_values=['NA','NaN',' '])
Hour = pd.read_csv('pnas.1920849117.sd03.csv',  na_values=['NA','NaN',' '])
Lat = pd.read_csv('pnas.1920849117.sd04.csv',  na_values=['NA','NaN',' '])
Lon = pd.read_csv('pnas.1920849117.sd05.csv',  na_values=['NA','NaN',' '])
Spd = pd.read_csv('pnas.1920849117.sd08.csv', na_values=['NA','NaN',' '])

#%%
df = pd.DataFrame(columns=['sid','basin','year','month','day','hour','lat','lon','spd'])
for i,isid in enumerate(Sid.values):
    nrow = np.argwhere(Year.iloc[i,:].isna())[0][0]
    temp = pd.DataFrame()
    temp['sid'] = list(isid)*nrow
    temp['basin'] = list(Basin.iloc[i])*nrow
    temp['year'] = Year.iloc[i,:nrow].values
    temp['month'] = Month.iloc[i,:nrow].values
    temp['day'] = Day.iloc[i,:nrow].values
    temp['hour'] = Hour.iloc[i,:nrow].values
    temp['lat'] = Lat.iloc[i,:nrow].values
    temp['lon'] = Lon.iloc[i,:nrow].values
    temp['spd'] = Spd.iloc[i,:nrow].values

    df = pd.concat([df,temp],ignore_index=True)

df.sort_values(by='sid')

df.to_csv('pnas_adt-hursat.csv', index=False)