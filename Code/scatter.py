import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

housePrice = pd.read_csv('metroMelbHousePrices.csv',encoding = 'ISO-8859-1')
commute = pd.read_csv('metroMelbCommuteDistance.csv',encoding = 'ISO-8859-1')
distance = pd.read_csv('distanceToCBD.csv',encoding = 'ISO-8859-1')

df = pd.merge(housePrice,commute,on='postcode')
df = df.sort_values('medPrice')
plt.scatter(df['medCommute'], df['medPrice'])
plt.xlabel('medCommute (km)')
plt.ylabel('medPrice ($)')
plt.grid(True)

x = np.array(df['medCommute'])
y = np.array(df['medPrice'])
m,b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)
plt.savefig('withOutliers.png')

##Outlier Detection using IQR
# Keep only values inside the IQR
Q1 = df['medPrice'].quantile(0.25)
Q3 = df['medPrice'].quantile(0.75)

Q1b = df['medCommute'].quantile(0.25)
Q3b = df['medCommute'].quantile(0.75)

df1 = df.loc[df['medPrice'] > Q1]
df1 = df1.loc[df1['medCommute'] > Q1b]
df2 = df1.loc[df1['medPrice'] < Q3]
df2 = df2.loc[df2['medCommute'] < Q3b]

# re-plot
plt.clf()
plt.scatter(df2['medCommute'], df2['medPrice'])
plt.xlabel('medCommute (km)')
plt.ylabel('medPrice ($)')
plt.grid(True)
x = np.array(df2['medCommute'])
y = np.array(df2['medPrice'])
m,b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)
plt.savefig('noOutliersIQR.png')

# z-score outlier detection #########################################################################
from scipy import stats

df['zPrice'] = np.abs(stats.zscore(df['medPrice']))
df['zCommute'] = np.abs(stats.zscore(df['medCommute']))
df1 = df.iloc[np.where(df['zPrice'] < 2)]
df2 = df.iloc[np.where(df1['zCommute'] < 2)]

# re-plot
plt.clf()
plt.scatter(df2['medCommute'], df2['medPrice'])
plt.xlabel('medCommute (km)')
plt.ylabel('medPrice ($)')
plt.grid(True)
x = np.array(df2['medCommute'])
y = np.array(df2['medPrice'])
m,b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)
plt.savefig('noOutliersZSCORE2STD.png')


df1 = df.iloc[np.where(df['zPrice'] < 1)]
df2 = df.iloc[np.where(df1['zCommute'] < 1)]
# re-plot
plt.clf()
plt.scatter(df2['medCommute'], df2['medPrice'])
plt.xlabel('medCommute (km)')
plt.ylabel('medPrice ($)')
plt.grid(True)
x = np.array(df2['medCommute'])
y = np.array(df2['medPrice'])
m,b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)
plt.savefig('noOutliersZSCORE1STD.png')


################################################################################
plt.clf()
df = pd.merge(housePrice,distance,on='postcode')
df = df.sort_values('medPrice')
plt.scatter(df['distance'], df['medPrice'])
plt.xlabel('distance (km)')
plt.ylabel('medPrice ($)')
plt.grid(True)

df['zPrice'] = np.abs(stats.zscore(df['medPrice']))
df['zDistance'] = np.abs(stats.zscore(df['distance']))
df1 = df.iloc[np.where(df['zPrice'] < 2)]
df2 = df.iloc[np.where(df1['zDistance'] < 2)]

# re-plot
plt.clf()
plt.scatter(df2['distance'], df2['medPrice'])
plt.xlabel('distance (km)')
plt.ylabel('medPrice ($)')
plt.grid(True)
x = np.array(df2['distance'])
y = np.array(df2['medPrice'])
m,b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)
plt.savefig('DISTANCEnoOutliersZSCORE2STD.png')
