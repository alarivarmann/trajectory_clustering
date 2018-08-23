# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 17:37:56 2018

@author: alari
"""

#%% auxiliary functions
import numpy as np
import os

global distcol
global timecol
global velcol
global accol
distcol = 'dDist_km'
timecol = 'dTime_min'
velcol = 'velocity_km_min'
accol = 'acc_km_minsq'

def get_files(direc):
    full_files = []
    for root, dirs, files in os.walk(direc):
        for name in files:
            full_files.append(os.path.join(root, name))
        
    return(full_files)


def add_time_diff(data):
    '''float64'''
    data[timecol] =  (data['date_time'].shift(-1) - data['date_time'])/ np.timedelta64(1, 'm')
    return(data)
    
def add_dist_diff(data):

    '''float64'''
    data[distcol] =  np.append(pythagoras(data['latitude'], data['longitude']),0)
    return(data)

def add_acc_vel(data):
  

    ''' float64'''
    data[velcol]=np.divide(data[distcol],data[timecol])
    data[accol]=np.divide(data[velcol],data[timecol])

    return(data)

def doPipe(data):
# =============================================================================
#     if(quarterdata==1):
#         data = data.query('taxi_id<2501')
# =============================================================================
        
    data = data.pipe(add_time_diff)\
    .pipe(add_dist_diff)\
    .pipe(add_acc_vel)
    data_out = filterByTimeThreshold(data,-0.01,0)
    return(data_out)

def doPipeForEach(datalist):
    '''Apply the doPipe function for every element in the input datalist'''
    data_list = [doPipe(r) for r in datalist]
  
    return(data_list)

def produceFormat(data_list,ifrenamed):
    if(ifrenamed==0):
        data_list = [k.rename(index=str,columns={'latitude':'x','longitude':'y'}) for k in data_list]      
    cc = [o[['x','y']].to_dict(orient='records') for o in data_list]
    return(cc)
    
    
def doFeatureProc(data_list):
    data_list = [x.drop_duplicates(inplace=True) for x in data_list]
    data_list = [x.dropna(inplace=True) for x in data_list]  
    data_list = [doPipe(x,distcol,timecol,0) for x in data_list]
    return(data_list)

def doTimeDistCrosstab(data):
    import pandas as pd
    data['dist_ind'] = data[distcol]>5000.0
    data['time_ind'] = data[timecol]>300
    tab = pd.crosstab(data['dist_ind'],data['time_ind'])
    return(tab)

def filterByTimeThreshold(data,threshold,ifsmaller):

  if(ifsmaller==1):
      filtered = data[(data[timecol]< threshold) & (data[timecol]> -1*threshold)]
  else :
      filtered = data[data[timecol] > threshold]

  return(filtered)


def pythagoras(lat_in, lon_in):
    lat = np.array(lat_in)
    lon = np.array(lon_in)
    
    lat *= np.pi/180 # angles to radians
    lon *= np.pi/180
    
    lon1 = lon[0:-1] # all but last
    lon2 = lon[1:] # all but first
    
    lat1 = lat[0:-1] # all but last
    lat2 = lat[1:] # all but first
    
    x = (lon2-lon1) * np.cos((lat1+lat2)/2) # shift in lon 
    y = lat2-lat1 # shift in lat
    
    d = np.sqrt(x**2 + y**2) * 6371
    return d

def giveFilenames(settings):
    outnames = ['out'+str(idx)+'setting'+str(setidx)+'.txt' for idx in range(0,20) for setidx in range(0,len(settings))]
    filenames = ['input'+str(idx)+'setting'+str(setidx)+'.txt' for idx in range(0,20) for setidx in range(0,len(settings))]
    partitioned_trajectories = ['trajectory_list'+str(idx)+'setting'+str(setidx)+'.txt' for idx in range(0,20) for setidx in range(0,len(settings))]
    clusters = ['cluster_list'+str(idx)+'setting'+str(setidx)+'.txt' for idx in range(0,20) for setidx in range(0,len(settings))]
    #filenames= ['input'+str(i)+'.txt' for i in range(0,20)]
    # outnames= ['out'+str(i)+'.txt' for i in range(0,20)]
    #partitioned_trajectories = ['trajectory_list'+str(i)+'.txt' for i in range(0,20)]
  #  clusters =  ['cluster_list'+str(i)+'.txt' for i in range(0,20)]
    return(filenames,outnames,partitioned_trajectories,clusters)
    

def produceConfigs():
    idx = 0
    outconfs = [None]*5*3*4
    for eps in np.linspace(0.002,0.1,5):
        for min_neighbours in [2,8,10]:
           # for min_num_traj in [10,15,20]:
           for mp in [1E-7,1E-2,0.1,1]:
                outconfs[idx]={"epsilon": eps, "min_neighbors": min_neighbours, \
                       "min_num_trajectories_in_cluster": 5,\
                       "min_vertical_lines": 2,\
                       "min_prev_dist": mp}
                idx +=1
    return(outconfs)

