# -*- coding: utf-8 -*-
"""
Created on Tue May  7 18:41:51 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Helvetica'
rcParams['xtick.top'] = 'False'
rcParams['ytick.right'] = 'False'
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['hatch.color'] = 'k'
rcParams['hatch.linewidth'] = 0.6
rcParams['mathtext.fontset'] = 'stix'
rcParams['mathtext.default'] = 'regular'

#%%
datasets = ['ADT-HURSAT','IBTrACS']
colorlist = ['gray','#02BE5F','#8DDA63','#D1F186','#FFE286','#FFAF5A','#FE6C3B','#F82C21']
labellist = ['EX','TD','TS','CAT1','CAT2','CAT3','CAT4','CAT5']

tc_sids = ['2004223N11301','2011270N18139','2013052S13126']
tc_name = ['Charley(2004)','Nalgae(2011)','Rusty(2013)']
for i,isid in enumerate(tc_sids):
    if i!=0: continue
    ibt = pd.read_csv('IBTrACS_'+isid+'.csv',keep_default_na=False,na_values='')
    ibt = ibt.astype({'SEASON':'int32','ISO_TIME':'datetime64[ns]','LAT':'float32','LON':'float32','USA_WIND':'float32','USA_SSHS':'int32'})

    adt = pd.read_csv('ADT-HURSAT_'+isid+'.csv',keep_default_na=False,na_values='')
    adt = adt.astype({'ISO_TIME':'datetime64[ns]','WIND':'float32'})

    y_ibt = ibt['LAT'].values
    x_ibt = ibt['LON'].values
    w_ibt = ibt['USA_WIND'].values

    y_adt = adt['LAT'].values
    x_adt = adt['LON'].values
    w_adt = adt['WIND'].values

    fig,axs = plt.subplots(1,2,figsize=(6,2))
    fig.subplots_adjust(left=0.07, bottom=0.08, right=0.95, top=0.85,hspace=0.13)
    for k in range(2):
        ax = axs[k]
        ax.text(-0.10,1.06,chr(97+k), transform=ax.transAxes, fontdict={'weight':'bold','size':17})

        m = Basemap(llcrnrlon=-100.,llcrnrlat=10,urcrnrlon=-40.,urcrnrlat=45.01,projection='mill',\
                    rsphere=(6378137.00,6356752.3142),resolution ='l',ax=ax)
        m.drawcoastlines(linewidth=0.5, color='k')
        m.drawcountries(linewidth=0.5, color='k')
        #m.drawstates(linewidth=0.25, color='grey')
        #m.fillcontinents(color='g',lake_color='b',alpha=0.2)
        m.drawparallels(np.arange(-90,90,10),labels=[1,0,0,0], fontsize=8, linewidth=0.5)
        m.drawmeridians(np.arange(-180,180,20),labels=[0,0,0,1], fontsize=8, linewidth=0.5)

        marker_kwargs = {'markersize': 3, 'color': 'r', 'markeredgecolor': 'r'}
        if k==0:
            mx,my = m(x_adt,y_adt)
            for iw in np.arange(1,w_adt.size):
                x0 = mx[iw-1]
                y0 = my[iw-1]

                x1 = mx[iw]
                y1 = my[iw]
                if w_adt[iw]<34 or np.isnan(w_adt[iw]):
                    ic = -1
                elif w_adt[iw]<64:
                    ic = 0
                elif w_adt[iw]<83:
                    ic = 1
                elif w_adt[iw]<96:
                    ic = 2
                elif w_adt[iw]<113:
                    ic = 3
                elif w_adt[iw]<137:
                    ic = 4
                elif w_adt[iw]>=137:
                    ic = 5
                m.plot([x0,x1],[y0,y1], marker='.', markersize=5,color=colorlist[ic+2])
        else:
            mx,my = m(x_ibt,y_ibt)
            for iw in np.arange(1,w_ibt.size):
                x0 = mx[iw-1]
                y0 = my[iw-1]

                x1 = mx[iw]
                y1 = my[iw]
                if w_ibt[iw]<34 or np.isnan(w_ibt[iw]):
                    ic = -1
                elif w_ibt[iw]<64:
                    ic = 0
                elif w_ibt[iw]<83:
                    ic = 1
                elif w_ibt[iw]<96:
                    ic = 2
                elif w_ibt[iw]<113:
                    ic = 3
                elif w_ibt[iw]<137:
                    ic = 4
                elif w_ibt[iw]>=137:
                    ic = 5
                m.plot([x0,x1],[y0,y1], marker='.', markersize=5,color=colorlist[ic+2])

        ax.set_title(datasets[k],loc='left',fontdict={'size':8.5,'weight':'bold'},pad=4)
        ax.set_title(tc_name[i],loc='center',fontdict={'size':8.5,'weight':'normal'},pad=4)

        ax.plot([0.84,0.98,0.98,0.84,0.84],[0.5,0.5,0.98,0.98,0.5],color='k',linewidth=1.5,transform=ax.transAxes,zorder=5)
        ax.fill([0.84,0.98,0.98,0.84],[0.5,0.5,0.98,0.98],color='w',transform=ax.transAxes,zorder=6)
        for ii in range(len(colorlist)):
            ax.plot(0.86,0.95-ii*0.06,marker='.',markersize=5.5,color=colorlist[ii], transform=ax.transAxes,zorder=7)
            ax.text(0.89,0.95-ii*0.061-0.018,labellist[ii],fontsize=6,transform=ax.transAxes,zorder=8)

    fig.savefig(isid+'.png',dpi=600)
    plt.show()