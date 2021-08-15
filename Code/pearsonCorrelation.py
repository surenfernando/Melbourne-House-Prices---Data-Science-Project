import pandas as pd
import numpy as np
from scipy import stats

housePrice = pd.read_csv('metroMelbHousePrices.csv',encoding = 'ISO-8859-1')
commute = pd.read_csv('metroMelbCommuteDistance.csv',encoding = 'ISO-8859-1')

df = pd.merge(commute,housePrice)
df = df.iloc[:,[2,3]]

df['zPrice'] = np.abs(stats.zscore(df['medPrice']))
df['zCommute'] = np.abs(stats.zscore(df['medCommute']))
df1 = df.iloc[np.where(df['zPrice'] < 2)]
df2 = df.iloc[np.where(df1['zCommute'] < 2)]

print(df['medCommute'].corr(df['medPrice'],method='pearson'))
