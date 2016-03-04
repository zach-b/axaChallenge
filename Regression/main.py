import pandas as pd
import numpy as np
import datetime
from preprocessing import preprocess
from preprocessing import processDate
import os
import time

from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.grid_search import RandomizedSearchCV
from sklearn.grid_search import GridSearchCV

os.chdir('..')
#==============================================================================
# Algo avec régression
#==============================================================================

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

submission = pd.read_csv('submission.txt',sep='\t',parse_dates=[0])

#Load Data
train_data = pd.read_csv('train_2011_2012.csv',header=0, sep=';',parse_dates=[0])
#train_data = pd.read_csv('train_data_short.csv',header=0, sep=';',parse_dates=[1])
#meteo2011 = pd.read_csv('meteo_2011.csv', sep=',',names=['date', 'dept_nb','city','temp_min','temp_max','wind_dir','precip','pressure_hPa'])
#meteo2012 = pd.read_csv('meteo_2012.csv', sep=',',names=['date', 'dept_nb','city','temp_min','temp_max','wind_dir','precip','pressure_hPa'])
#meteo = pd.read_csv('meteo_2011.csv', sep=',',names=['DATE', 'dept_nb','city','temp_min','temp_max','wind_dir','precip','pressure_hPa'], parse_dates=[0]).append(
#pd.read_csv('meteo_2012.csv', sep=',',names=['DATE', 'dept_nb','city','temp_min','temp_max','wind_dir','precip','pressure_hPa'],parse_dates=[0]))
meteo = pd.concat([pd.read_csv('meteo_2011.csv', sep=',',names=['date', 'dept_nb','city','temp_min','temp_max','wind_dir','precip','pressure_hPa'], parse_dates=[0]),(pd.read_csv('meteo_2012.csv', sep=',',names=['date', 'dept_nb','city','temp_min','temp_max','wind_dir','precip','pressure_hPa'], parse_dates=[0]))], ignore_index=True)


#%%
#==============================================================================
# Data Pre processing
#==============================================================================

data, labels, meteo = preprocess(train_data, meteo)
num_features = len(train_data.columns.values)


#%%
#==============================================================================
# Learning Algorithm
#==============================================================================
print "Training ..."
Regressors = {}

start_time = time.time()

for ass in data:
    print ass
#    data_train, data_test, labels_train, labels_test = cross_validation.train_test_split(data[ass].values, labels[ass])
    #Regressors[ass] = GaussianNB()
#    Regressors[ass] = LogisticRegression()    
#    Regressors[ass] = RandomForestRegressor()
    Regressors[ass] = GradientBoostingRegressor(n_estimators = 300, max_depth=7)
#    rgs = GradientBoostingRegressor()
#    GBRdict = {"n_estimators":[100,200,300],
#               "max_depth":[3,5]}

    # essayer de voir l'influence des paramètres
    # tester plusieurs valeurs

#    Regressors[ass] = GridSearchCV(rgs,param_grid=GBRdict,cv=5)
    Regressors[ass].fit(data[ass].values,labels[ass])    
        
#    Regressors[ass].fit(data_train,labels_train)
    

elapsed_time = time.time()-start_time
print elapsed_time

#%%
#==============================================================================
# Evaluation
#==============================================================================
#

X = submission.copy()

processDate(X,'DATE')
X = pd.merge(X,meteo,on=['month','day','weekday','weekend','time','night'],how='left')

for column in ['temp_min','temp_max','precip','pressure_hPa']:
    X[column].fillna(np.mean(X[column]), inplace = True)

for ass in data:
    submission.prediction[submission['ASS_ASSIGNMENT']==ass]=(Regressors[ass].predict(X[X['ASS_ASSIGNMENT']==ass].drop(['ASS_ASSIGNMENT','prediction'], axis=1)))

submission.prediction=submission.prediction.clip(lower = 0)
submission.to_csv('new_results.txt',sep='\t',date_format='%Y-%m-%d %H:%M:%S.000',index=False )




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

