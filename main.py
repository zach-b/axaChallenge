import pandas as pd
from preprocessing import preprocess


#Load Data
train_data = pd.read_csv('train_2011_2012.csv',header=0, sep=';')    
print train_data.head()

#%%
#Data Pre processing

preprocessed_train_data = preprocess(train_data)