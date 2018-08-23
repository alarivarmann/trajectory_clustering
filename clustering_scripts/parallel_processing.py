# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 00:06:30 2018

@author: alari
"""
from multiprocessing import Process
from multiprocessing import Pool, cpu_count
import multiprocessing as mp
import os
import auxiliary as a
import json
import codecs
from main2 import doIt
import pickle
import numpy as np

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def writeDataList(data_list_json):
    data_json_100 = data_list_json[0:100]
    with open('data_list_json_100.txt', 'wb') as f:
        pickle.dump(data_json_100, f,protocol=2)
    return(data_json_100)

def readDataList(jsonfile):
    with open(jsonfile, 'rb') as f:
        data_list_json = pickle.load(f)
    return(data_list_json)
        
def saveFileInfo(ifexists,data_list_json,dataname,dumpneeded):
    if(ifexists==0):
        with open(dataname, 'rb') as f:
            data_list_json = pickle.load(f)
    
    settings = a.produceConfigs() # all clustering settings to test out
    maxidx = 20
    filenames =[None]*maxidx*len(settings)
    outnames =[None]*maxidx*len(settings)
    trajectory_list =[None]*maxidx*len(settings)
    cluster_list =[None]*maxidx*len(settings)
    
    multiplier = np.floor(len(data_list_json)/maxidx)
    for idx in range(0,maxidx): # chuncking into files for testing
    # ,"trajectories":cc}
        sub_prepared = data_list_json[int(idx*multiplier):int((idx+1)*multiplier)] # subset the data

        for setidx,se in enumerate(settings):
            se['trajectories']=sub_prepared # add the file to the setting dictionary
            param_and_traj = se
            # filenames for clustering
            filename = 'input'+str(idx)+'setting'+str(setidx)+'.txt'
            filenames[idx] = filename
            outnames[idx] =  'out'+str(idx)+'setting'+str(setidx)+'.txt'
            trajectory_list[idx] = 'trajectories'+str(idx)+'setting'+str(setidx)+'.txt'
            cluster_list[idx] = 'clusters'+str(idx)+'setting'+str(setidx)+'.txt'
            
            fullpath = 'testdata/'+ filename
            if (dumpneeded ==1):
                with open(fullpath, 'wb') as f:
                    json.dump(param_and_traj, codecs.getwriter('utf-8')(f), ensure_ascii=False)
        return(filenames,outnames,trajectory_list,cluster_list)

def doClustering(filenames):

   # info('function doClustering')
    problemidx = [None]*20
    for idx in range(0,len(filenames)):
 #        python main.py -i in[idx] -o out[idx]
        try: # -m timeit
            doIt(filenames[idx],outnames[idx],trajectory_list[idx],cluster_list[idx]) 
        except:
            problemidx[idx]=idx
            continue
        idx+=1
    return(problemidx) 
    
if __name__ == "__main__":
    #doClustering()
    data_json_100 = readDataList('data_list_json_100.txt')
    filenames,outnames,trajectory_list,cluster_list = saveFileInfo(1,data_json_100,'test',0) # file list

    pool = Pool(processes=int(4))
    problemidx = pool.map(doClustering, filenames,chunksize=5)
    print(problemidx)
# =============================================================================
#     with Pool(4) as p:
#         p.map(doClustering)
# =============================================================================
# =============================================================================
#     p = Process(target=doClustering) # , args=('filenames','outnames')
#     p.start()
#     p.join()
# =============================================================================
      
    
    
# =============================================================================
#  python main.py -i filenames[idx] -o outnames[idx]
# 
# python  main.py -i "input2.txt" -o "out2.txt"
# =============================================================================
# -m timeit
