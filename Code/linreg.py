import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import linregress

housePrice = pd.read_csv('metroMelbHousePrices.csv',encoding = 'ISO-8859-1')
commute = pd.read_csv('metroMelbCommuteDistance.csv',encoding = 'ISO-8859-1')

df = pd.merge(commute,housePrice)
df = df.iloc[:,[2,3]]

df['zPrice'] = np.abs(stats.zscore(df['medPrice']))
df['zCommute'] = np.abs(stats.zscore(df['medCommute']))
df1 = df.iloc[np.where(df['zPrice'] < 2)]
df2 = df.iloc[np.where(df1['zCommute'] < 2)]
    
import matplotlib.pyplot as plt
res = linregress(list(df2['medCommute']), list(df2['medPrice']))
plt.plot(list(df2['medCommute']), list(df2['medPrice']), 'o', label='original data')
plt.plot(df2['medCommute'], res.intercept + res.slope*df2['medCommute'], 'r', label='fitted line')
print(res)
