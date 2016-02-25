# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:28:26 2016

@author: user
"""

import pandas as pd

def preprocess(train_data) :
    
#    Pas de jours feriés ?
    train_data.drop('DAY_OFF', axis=1,inplace=True)
    train_data.drop('DAY_DS', axis=1,inplace=True)
    

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
    
#    ACD_COD = 1 tout le temps
    train_data.drop('ACD_COD', axis=1,inplace=True)
#    ACD_LIB = 'Entity1 G3RV6' tout le temps
    train_data.drop('ACD_LIB', axis=1,inplace=True)
    
    train_data.drop('ASS_DIRECTORSHIP', axis=1,inplace=True)
    train_data.drop('ASS_PARTNER', axis=1,inplace=True)
    train_data.drop('ASS_POLE', axis=1,inplace=True)
    train_data.drop('ASS_SOC_MERE', axis=1,inplace=True)
    
#    A quoi servent ces features ?
    train_data.drop('ASS_BEGIN', axis=1,inplace=True)
    train_data.drop('ASS_COMENT', axis=1,inplace=True)
    train_data.drop('ASS_END', axis=1,inplace=True)
    return 0