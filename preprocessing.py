# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:28:26 2016

@author: user
"""

import pandas as pd

def preprocess(train_data) :
    
    train_data['JOUR']= (train_data['TPER_TEAM']=='Jour')*1
    train_data['NUIT']= (train_data['TPER_TEAM']=='Nuit')*1
    train_data.drop('TPER_TEAM',axis=1,inplace=True)
    
    
    
    return 0