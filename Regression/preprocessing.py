# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:28:26 2016

@author: user
"""
#==============================================================================
# Algo avec régression
#==============================================================================

import pandas as pd
import numpy as np
import datetime
import time




def getmonth(date) :
    return date.month
    
def getday(date) : 
    return date.day
    
def getweekday(date) : 
    return date.dayofweek
    
def getweekend(date) : 
    return (getweekday(date) >= 5)
    
def gettime(date) :
    return(date.hour+date.minute/60.0)

def getnight(date) : 
    t = gettime(date)
    return (t >= 23.5 or t <= 7)
    
def processDate(data, date_index):
    data['month'] = data[date_index].map(getmonth)
    data['day'] = data[date_index].map(getday)
    data['weekday'] = data[date_index].map(getweekday)
    data['weekend'] = data[date_index].map(getweekend)
    data['time'] = data[date_index].map(gettime)    
    data['night'] = data[date_index].map(getnight)
    data.drop(date_index, axis=1, inplace=True)
    
    





def preprocess(train_data,meteo) :
    droplist =[]
    
    train_data.drop('DAY_WE_DS', axis=1,inplace=True)
    train_data.drop('TPER_TEAM', axis=1,inplace=True)
    train_data.drop('TPER_HOUR', axis=1,inplace=True)
    train_data.drop('WEEK_END', axis=1,inplace=True)
    
#    pas de jours feriés ?
    droplist.extend(['DAY_OFF','DAY_DS'])
    droplist.extend(['ACD_COD','ACD_LIB'])
    droplist.extend(['ASS_DIRECTORSHIP','ASS_PARTNER','ASS_POLE','ASS_SOC_MERE'])
    droplist.extend(['ASS_BEGIN','ASS_COMENT','ASS_END'])
    
#    data_time = [float(t.split(' ')[1].split(':')[1])/60 for t in train_data['DATE']]
    
#    train_data['TPER_HOUR'] = train_data['TPER_HOUR'] + data_time
    
    droplist.extend(['SPLIT_COD','CSPL_CALLSOFFERED','CSPL_OUTFLOWCALLS','CSPL_INFLOWCALLS','CSPL_NOANSREDIR','CSPL_ACDCALLS',
    'CSPL_ABNCALLS','CSPL_CONFERENCE','CSPL_TRANSFERED','CSPL_RINGCALLS','CSPL_DISCCALLS','CSPL_HOLDCALLS',
    'CSPL_ACDAUXOUTCALLS','CSPL_HOLDABNCALLS','CSPL_MAXINQUEUE','CSPL_DEQUECALLS','CSPL_ACWINCALLS',
    'CSPL_AUXINCALLS','CSPL_ACWOUTCALLS','CSPL_ACWOUTOFFCALLS','CSPL_ACWOUTADJCALLS','CSPL_AUXOUTCALLS',
    'CSPL_AUXOUTOFFCALLS','CSPL_AUXOUTADJCALLS','CSPL_INTRVL','CSPL_OUTFLOWTIME','CSPL_DEQUETIME','CSPL_I_ACDTIME',
    'CSPL_DISCTIME','CSPL_HOLDTIME','CSPL_ABNTIME','CSPL_I_STAFFTIME','CSPL_ANSTIME','CSPL_I_RINGTIME',
    'CSPL_RINGTIME','CSPL_ACDTIME','CSPL_I_AVAILTIME','CSPL_ACWTIME','CSPL_I_ACWTIME','CSPL_I_OTHERTIME',
    'CSPL_ACWINTIME','CSPL_I_ACWINTIME','CSPL_AUXINTIME','CSPL_I_AUXINTIME','CSPL_ACWOUTIME','CSPL_I_ACWOUTTIME',
    'CSPL_ACWOUTOFFTIME','CSPL_AUXOUTTIME','CSPL_I_AUXOUTTIME','CSPL_AUXOUTOFFTIME','CSPL_SERVICELEVEL',
    'CSPL_ACCEPTABLE','CSPL_SLVLOUTFLOWS','CSPL_SLVLABNS','CSPL_ABNCALLS1','CSPL_ABNCALLS2','CSPL_ABNCALLS3',
    'CSPL_ABNCALLS4','CSPL_ABNCALLS5','CSPL_ABNCALLS6','CSPL_ABNCALLS7','CSPL_ABNCALLS8','CSPL_ABNCALLS9',
    'CSPL_ABNCALLS10','CSPL_MAXSTAFFED','CSPL_INCOMPLETE','CSPL_ABANDONNED_CALLS','CSPL_CALLS'])
    train_data.drop(droplist, axis=1,inplace=True)
    
    if 'Unnamed: 0' in train_data.columns.values:
        train_data.drop('Unnamed: 0', axis=1,inplace=True)
        
    processDate(train_data,'DATE')
        
#%%
#   traitement de météo
    
    def addSemiHours(date) :
        return date + datetime.timedelta(minutes=30)
    
#    def formatDate(date) :
#        return date+":00.000"
        
    meteo = meteo[meteo['city']=='Paris-Montsouris']
    meteo.drop(['dept_nb','city','wind_dir'], axis=1,inplace=True)
    
    meteo_temp = meteo.copy(deep=True)
    meteo_temp['date'] = meteo['date'].map(addSemiHours)
    
    meteo = meteo.append(meteo_temp)
    meteo.sort(['date'], inplace = True)    
    del meteo_temp    
        
    processDate(meteo,'date')
    
    
    
#%%
#   Enlever les ass_assignment non traités     
        
    non_traite = ['A DEFINIR', 'AEVA', 'DOMISERVE', 'Divers','Evenements', 'FO Remboursement', 'Finances PCX',
       'IPA Belgique - E/A MAJ','Juridique', 'KPT', 'LifeStyle','Maroc - Génériques', 'Maroc - Renault',
       'Medicine', 'NL Médical', 'NL Technique','Réception', 'TAI - CARTES', 'TAI - PANNE MECANIQUE',
       'TAI - PNEUMATIQUES', 'TAI - RISQUE', 'TAI - RISQUE SERVICES','TAI - SERVICE', 'TPA',
       'Technical', 'Technique Belgique', 'Technique International','Truck Assistance']
    for ass in non_traite:
        train_data = train_data[train_data['ASS_ASSIGNMENT']!=ass]
        
        
#%%

    groups = train_data.groupby(['month','day','weekday','weekend','time','night','ASS_ASSIGNMENT']).sum().reset_index()
    
#%%
#Concaténer météo et groups
    
    groups = pd.merge(groups,meteo,on=['month','day','weekday','weekend','time','night'],how='left')
#%%    
    
    for column in ['temp_min','temp_max','precip','pressure_hPa']:
        groups[column].fillna(np.mean(groups[column]), inplace = True)
        
#%%
#  partitionner les données selon leur ass_assignment
    ass_list = np.unique(train_data['ASS_ASSIGNMENT'].values)
    data = {}
    labels = {}
    for ass in ass_list :
        data[ass] = groups.loc[groups['ASS_ASSIGNMENT']==ass]
        labels[ass] = groups['CSPL_RECEIVED_CALLS'].loc[groups['ASS_ASSIGNMENT']==ass]
        data[ass].drop(['ASS_ASSIGNMENT','CSPL_RECEIVED_CALLS'], axis=1, inplace = True)
    
    
#%%
    
    
#    train_data.drop('CSPL_RECEIVED_CALLS', axis=1,inplace=True)
    
    
    return data, labels, meteo