# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 01:38:50 2024

@author: Jimmy Liu, UCAS&LZU
"""

import datetime
import numpy as np
import pandas as pd

#%%
adt = pd.read_csv('./ADT-HURSAT/pnas_adt-hursat.csv', low_memory=False, keep_default_na=False, na_values='')
adt = adt.astype({'year':'int32','month':'int32','day':'int32','hour':'int32','lat':'float32','lon':'float32','spd':'float32'})

#%%
sids = list(set(adt['sid']))
sids.sort()

df = pd.DataFrame(columns=['sid','basin','sphere','season','year','month','day','hour','lat','lon','lmi','occurtime'])

for i,sid in enumerate(sids):
    tc = adt[adt['sid'] == sid].reset_index(drop=True)

    if tc['spd'].isnull().all():
        bs = tc['basin'][0]
        if bs in ['NA','WP','EP','NI']:
            sph = 'NH'
        elif bs in ['SI','SP','SA']:
            sph = 'SH'

        ss = yr = mo = dy = hr = lat = lon = lmi = dday = np.nan

        temp = pd.DataFrame([[sid,bs,sph,ss,yr,mo,dy,hr,lat,lon,lmi,dday]],\
                            columns=['sid','basin','sphere','season','year','month','day','hour','lat','lon','lmi','occurtime'])
    else:
        lmi = tc['spd'].max()
        ind = np.where(tc['spd'] == lmi)[0][0]

        bs = tc['basin'][ind]
        if bs in ['NA','WP','EP','NI']:
            sph = 'NH'
        elif bs in ['SI','SP','SA']:
            sph = 'SH'

        yr = tc['year'][ind]
        mo = tc['month'][ind]
        dy = tc['day'][ind]
        hr = tc['hour'][ind]

        lat = tc['lat'][ind]
        lon = tc['lon'][ind]

        dt = datetime.datetime(yr,mo,dy,0,0,0)
        #north hemisphere
        if lat > 0:
            ss = yr
            ddt = datetime.datetime(yr,mo,dy,hr,0,0) - datetime.datetime(ss,1,1,0,0,0)
        #south hemisphere
        else:
            ss = yr
            if dt > datetime.datetime(yr,7,1,0,0,0):
                ss = yr+1
            ddt = datetime.datetime(yr,mo,dy,hr,0,0) - datetime.datetime(ss-1,7,1,0,0,0)

        dday = ddt.total_seconds()/(24*3600)
        print(f'SID:{sid:13s} WMAX:{lmi:5.1f} OCCURTIME:{dday:6.2f}')

        lmi = np.int32(lmi)
        temp = pd.DataFrame([[sid,bs,sph,ss,yr,mo,dy,hr,lat,lon,lmi,dday]],\
                            columns=['sid','basin','sphere','season','year','month','day','hour','lat','lon','lmi','occurtime'])

    df = pd.concat([df,temp])

df.reset_index(drop=True, inplace=True)
df.to_csv('ma_adt-hursat_lmi_time_leapyear.csv', index=False)