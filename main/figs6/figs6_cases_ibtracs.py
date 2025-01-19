# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 01:38:50 2024

@author: Jimmy Liu, UCAS&LZU
"""

import pandas as pd

ibt = pd.read_csv('../DataSets/IBTrACS/ibtracs.ALL.list.v04r01.csv',low_memory=False,keep_default_na=False,na_values=' ',
                  usecols=['SID','SEASON','BASIN','ISO_TIME','LAT','LON','USA_WIND','USA_SSHS'])
ibt.drop(index=0,inplace=True)
ibt = ibt.astype({'SEASON':'int32','ISO_TIME':'datetime64[ns]','LAT':'float32','LON':'float32','USA_WIND':'float32','USA_SSHS':'int32'})

sids = ['2004223N11301','2011270N18139','2013052S13126']

for i,isid in enumerate(sids):
    tc = ibt[ibt['SID'] == isid].reset_index(drop=True)
    tc.to_csv('ibtracs_'+isid+'.csv',index=False)