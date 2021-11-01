# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:54:54 2021

@author: guibd
"""
from tqdm import tqdm
import os
import pandas as pd    
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from path_ import data_path

def data_importation():

# path where files will be stored 
    data_p = data_path()
    path = data_p
    os.chdir(path) #changing current working directory to load csvs
    
    # cleaning old files
    
    dir = path
    for f in tqdm(os.listdir(dir)):
        os.remove(os.path.join(dir, f))
     
    # extract csvs from zip file into path

    
    zipurl = "http://ergast.com/downloads/f1db_csv.zip"
    
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(path)
    
    # importing data in python
    
    csvs = [x for x in os.listdir(path) if x.endswith('.csv')]
    # stats.csv -> stats
    fns = [os.path.splitext(os.path.basename(x))[0] for x in csvs]
    
    data = {}
    for i in tqdm(range(len(fns))):
        data[fns[i]] = pd.read_csv(csvs[i])
    
    data.keys()
    
    return data


