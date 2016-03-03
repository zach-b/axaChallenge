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
import time

def preprocess(train_data) :
    droplist =[]
    
    

    train_data['LUNDI']=(train_data['DAY_WE_DS']=='Lundi')*1
    train_data['MARDI']=(train_data['DAY_WE_DS']=='Mardi')*1
    train_data['MERCREDI']=(train_data['DAY_WE_DS']=='Mercredi')*1
    train_data['JEUDI']=(train_data['DAY_WE_DS']=='Jeudi')*1
    train_data['VENDREDI']=(train_data['DAY_WE_DS']=='Vendredi')*1
    train_data['SAMEDI']=(train_data['DAY_WE_DS']=='Samedi')*1
    train_data['DIMANCHE']=(train_data['DAY_WE_DS']=='Dimanche')*1
    train_data.drop('DAY_WE_DS', axis=1,inplace=True)
    
    train_data['JOUR']= (train_data['TPER_TEAM']=='Jours')*1
    train_data['NUIT']= (train_data['TPER_TEAM']=='Nuit')*1
    train_data.drop('TPER_TEAM', axis=1,inplace=True)
    
#    pas de jours feriés ?
    droplist.extend(['DAY_OFF','DAY_DS'])
    droplist.extend(['ACD_COD','ACD_LIB'])
    droplist.extend(['ASS_DIRECTORSHIP','ASS_PARTNER','ASS_POLE','ASS_SOC_MERE'])
    droplist.extend(['ASS_BEGIN','ASS_COMENT','ASS_END'])
    
    data_time = [float(t.split(' ')[1].split(':')[1])/60 for t in train_data['DATE']]
    train_data['TPER_HOUR'] = train_data['TPER_HOUR'] + data_time
    
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
        
        #%%
#   traitement de météo
    meteo = meteo[meteo['city']=='Paris-Montsouris']
    meteo.drop(['dept_nb','city','wind_dir'], axis=1,inplace=True)
    for column in meteo:
        meteo[column].fillna(np.mean(meteo[column]))
        
        
        
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
#   Rassembler les différentes lignes qui correspondent exactement à la même date et au même ass_assignment
#    
#    start_time = time.time()    
#    
#    date_list = np.unique(train_data['DATE'].values)
#    ass_list = np.unique(train_data['ASS_ASSIGNMENT'].values)
#    
#    for date in date_list:
#        for ass in ass_list:
#            print date +" "+ass
#            temp = (train_data['DATE']==date) & (train_data['ASS_ASSIGNMENT']==ass)
#            if not train_data[temp].empty:
#                first_index = train_data[temp].index.values[0]
#                train_data['CSPL_RECEIVED_CALLS'][first_index] = train_data['CSPL_RECEIVED_CALLS'][temp].sum()
#                
#                temp[first_index] = False
#                train_data = train_data[~temp]
#    
#    
#    elapsed_time = time.time() - start_time
#    print elapsed_time
#    
    #%%
#    partitionner les données selon leur ass_assignment
    ass_list = np.unique(train_data['ASS_ASSIGNMENT'].values)
    data = {}
    labels = {}
    for ass in ass_list :
        data[ass] = train_data.loc[train_data['ASS_ASSIGNMENT']==ass]
        labels[ass] = train_data['CSPL_RECEIVED_CALLS'].loc[train_data['ASS_ASSIGNMENT']==ass]
    
    
    #%%
    
    
#    train_data.drop('CSPL_RECEIVED_CALLS', axis=1,inplace=True)
    
    
    return data, labels