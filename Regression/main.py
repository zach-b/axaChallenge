import pandas as pd
import numpy as np
from preprocessing import preprocess
import os
os.chdir('..')
#==============================================================================
# Algo avec régression
#==============================================================================

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#Load Data
#train_data = pd.read_csv('train_2011_2012.csv',header=0, sep=';')
train_data = pd.read_csv('train_data_short.csv',header=0, sep=';')
#meteo2011 = pd.read_csv('meteo_2011.csv', sep=',',names=['date', 'dept_nb','city','temp_min','temp_max','wind_dir','precip','pressure_hPa'])
#meteo2012 = pd.read_csv('meteo_2012.csv', sep=',',names=['date', 'dept_nb','city','temp_min','temp_max','wind_dir','precip','pressure_hPa'])
print train_data.head()

#%%
#==============================================================================
# Data Pre processing
#==============================================================================

data, labels = preprocess(train_data)
num_features = len(train_data.columns.values)


#%%
#==============================================================================
# Learning Algorithm
#==============================================================================





#%%
#==============================================================================
# Evaluation
#==============================================================================
#
#print "EVALUATION"
#
#read = open('submission.txt', 'r')
#w = open('results.txt', 'w')
#
##12409 lignes dans le fichier
##test_data = np.zeros((12408,num_features))
#
##jours de la semaine pour les 12 jours concernés
#days = ['MARDI','MERCREDI','LUNDI','LUNDI','SAMEDI','LUNDI','DIMANCHE','MARDI','JEUDI','MERCREDI','LUNDI','VENDREDI']
#
#i=0
#for line in read :
#    print "line "+str(i)
#    if i!=0:
#        [date, ass, sub] = line.split('\t')
#        jour = days[int(date.split(' ')[0].split('-')[1])-1]
#        time = int(date.split(' ')[1].split(':')[0])+float(date.split(' ')[1].split(':')[1])/60
#        
#        temp = data[ass].loc[data[ass]['TPER_HOUR']==time]
#        temp = temp.loc[data[ass][jour]==1]
#        if len(np.unique(temp['DATE'].values))!=0:
#            moy = float(np.sum(temp['CSPL_RECEIVED_CALLS'].values))/len(np.unique(temp['DATE'].values))
#        else :
#            moy = 0
#        
#        w.write(date+'\t'+ass+'\t'+str(round(moy))+'\n')
#        
#    else :
#        w.write(line)
#        
#        
#    i=i+1
#    
#

