import pandas as pd
from preprocessing import preprocess

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#Load Data
#train_data = pd.read_csv('train_2011_2012.csv',header=0, sep=';', encoding='utf-8')
train_data = pd.read_csv('train_data_short.csv',header=0, sep=';')
print train_data.head()

#%%
#==============================================================================
# Data Pre processing
#==============================================================================

data, train_labels = preprocess(train_data)



#%%
#==============================================================================
# Learning Algorithm
#==============================================================================





#%%
#==============================================================================
# Evaluation
#==============================================================================




