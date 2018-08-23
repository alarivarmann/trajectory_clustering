# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 10:26:52 2018

@author: alari
"""


#%% READING IN DATA
import pandas as pd
import numpy as np
import os 
# pip install traclus_impl
# pip install Rtree
import traclus_impl as ti

import auxiliary as aux

from datetime import datetime

def get_files(direc):
    full_files = []
    for root, dirs, files in os.walk(direc):
        for name in files:
            full_files.append(os.path.join(root, name))
        
    return(full_files)


# full_files = get_files('/data')          
test_files = get_files('data2')

print("Reading in the .txt files...")
# dtypes = [int,datetime.datetime,float,float]
to_datetime = lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S')

data_list = []
for index, file_path in enumerate(test_files):
    data_list.append(pd.read_csv(file_path, \
            parse_dates = True,\
            names = ['taxi_id', 'date_time', 'longitude', 'latitude'],\
             # header=None, # infer_datetime_format=True,
            dtype={'taxi_id':'int','longitude':'float','latitude':'float'},\
            converters={'date_time': to_datetime}))


#%% FEATUREPROCESSING AS DESCRIBED in the auxiliary module -- PIPING AND QUICK FEATURE CLEANING
''' In the test files we have 65 taxi files'''

data_list = aux.doPipeForEach(data_list)
data_list_json_test = aux.produceFormat(data_list,0)

test_data = pd.concat(data_list, ignore_index=True)


#%% FROM NOW ON, WORK WITH THE SUBSAMPLED DATA due to computational limitations
# Remove outliers from the subsample

def countunique(feature): return(len(np.unique(feature)))
print('We will analyze  %d unique taxis'% countunique(test_data['taxi_id'])) # verify that it is the shape[0] of test data



#%% FEATURE ENGINEERING AND PROCESSING

tab = aux.doTimeDistCrosstab(test_data)
# =============================================================================
# on main data
# time_ind     False  True 
# dist_ind                 
# False     17625145  32902
# True          4815    122
# =============================================================================

# =============================================================================
# Out[93]:   on test data

# time_ind   False  True 
# dist_ind               
# False     100650    186
# True           2      0
# =============================================================================
'From the crosstable we see that there is a relatively large group with high times but low distances, before filtering'
'Lets see if this number coincides with the amount of taxis'

# =============================================================================
# countunique(data['taxi_id'])
# Out[402]: 10336
# 
# =============================================================================

'So most of the high times cannot be explained by the shifts between the taxi files. This means that we have identified a'
'probable traffic jam + parkers+waiters cluster'
