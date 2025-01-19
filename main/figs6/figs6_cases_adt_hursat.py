# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:22:50 2024

@author: Jimmy Liu, UCAS&LZU
"""

import datetime
import pandas as pd

Sid = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd07.csv')
Basin = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd01.csv', keep_default_na=False)
Year = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd09.csv')
Month = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd06.csv')
Day = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd02.csv')
Hour = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd03.csv')
Lat = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd04.csv')
Lon = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd05.csv')
Wind = pd.read_csv('../DataSets/ADT-HURSAT/pnas.1920849117.sd08.csv')

sids = ['2004223N11301','2011270N18139','2013052S13126']

for i,isid in enumerate(sids):
    k = Sid[Sid['StormID'] == isid].index[0]

    n = Year.iloc[k,:].notnull().sum()
    c1 = Year.iloc[k,:n].values.astype('int32')
    c2 = Month.iloc[k,:n].values.astype('int32')
    c3 = Day.iloc[k,:n].values.astype('int32')
    c4 = Hour.iloc[k,:n].values.astype('int32')
    c5 = Lat.iloc[k,:n].values
    c6 = Lon.iloc[k,:n].values
    c7 = Wind.iloc[k,:n].values

    dtlist = []
    for i in range(n):
        dtlist.append(datetime.datetime(c1[i],c2[i],c3[i],c4[i],0,0))
    df = pd.DataFrame(columns=['SID','BASIN','ISO_TIME','LAT','LON','WIND'])
    df['SID'] = [isid]*n
    df['BASIN'] = [Basin.iloc[k,0]]*n
    df['ISO_TIME'] = dtlist
    df['LAT'] = c5
    df['LON'] = c6
    df['WIND'] = c7

    df.to_csv('adt-hursat_'+isid+'.csv',index=False)