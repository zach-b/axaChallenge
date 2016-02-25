import pandas as pd
from preprocessing import preprocess


#Load Data
#train_data = pd.read_csv('train_2011_2012.csv',header=0, sep=';')
train_data = pd.read_csv('train_data_short.csv',header=0, sep=';')
print train_data.head()

#%%
#Data Pre processing

preprocess(train_data)