import pandas as pd
from math import radians, cos, sin, asin, sqrt

# geocoordinates of Melbourne
Mlong = 144.970267
Mlat = -37.814563


##### from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(row):
    lon1 = Mlong
    lat1 = Mlat
    lon2 = row['lon']
    lat2 = row['lat']
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
##### end function

# From https://www.coronavirus.vic.gov.au/sites/default/files/2020-10/Metro-Melb-Postcodes-Factsheet.pdf
metroMelbPostcodes = list(range(3000,3212)) + [3335,3336,3338,3980] + list(range(3427,3430)) + list(range(3750,3753)) + list(range(3754,3756)) + list(range(3759,3762)) + list(range(3765,3776)) + list(range(3781,3787)) + list(range(3788,3816)) + list(range(3910,3921)) + list(range(3926,3945)) + list(range(3975,3979))
metroMelbPostcodesDF = pd.DataFrame({'postcodes': metroMelbPostcodes})

# Filter in only suburbs which are in metro Melbourne.

## Inner join australianPostCodes.csv and metroMelbPostcodes to find suburbs in Metropolitan Melbourne
australianPostCodes = pd.read_csv('australianPostCodes.csv',encoding = 'ISO-8859-1')
melbPostcodes=pd.merge(australianPostCodes,metroMelbPostcodesDF,left_on='postcode',right_on='postcodes')

## Create new dataset, distance to cbd from longitude and latitude of each suburb to Melbourne
melbPostcodes['distance'] = melbPostcodes.apply(lambda r: haversine(r), axis=1)
melbSuburbs = melbPostcodes.loc[:,['postcode','suburb']]
melbSuburbs['suburb'] = melbSuburbs['suburb'].str.lower()
melbPostcodes = melbPostcodes.loc[:,['postcode', 'suburb', 'distance']]
melbPostcodes = melbPostcodes.groupby('suburb').agg('min')
melbPostcodes = melbPostcodes.groupby('postcode').agg('mean').round(2)
melbPostcodes = melbPostcodes.sort_values(by=['postcode'])

melbPostcodes.to_csv('distanceToCBD.csv', index='false')

## Inner join Melbourne suburbs and distanceToWork.csv to find the average and median commute distance per suburb in metro Melbourne
distanceToWork = pd.read_csv('distanceToWork.csv',encoding = 'ISO-8859-1')
distanceToWork['Statistical Area Level 2 label'] = distanceToWork['Statistical Area Level 2 label'].str.lower()
commuteDistancePerSuburb = pd.merge(melbSuburbs,distanceToWork,left_on='suburb',right_on='Statistical Area Level 2 label')
commuteDistancePerSuburb = commuteDistancePerSuburb.iloc[:,[0,5,6]]
commuteDistancePerSuburb = commuteDistancePerSuburb.groupby('postcode').agg('mean').round(2)
commuteDistancePerSuburb = commuteDistancePerSuburb.rename(columns={'Average commuting distance (kms)':'meanCommute', 'Median commuting distance (kms)': 'medCommute'})
commuteDistancePerSuburb.to_csv('metroMelbCommuteDistance.csv', index='false')


## Filter out only metro Melbourne house prices.
housePrices = pd.read_csv('housingPrices.csv',encoding = 'ISO-8859-1')
metroMelbHousePrices = pd.merge(melbSuburbs,housePrices,left_on='postcode',right_on='Postcode')
metroMelbHousePrices = metroMelbHousePrices.loc[:,['postcode','Price']]

# Groupby and find the mean and median house price per suburb 
metroMelbHousePricesMED = metroMelbHousePrices.groupby('postcode').median().dropna()
metroMelbHousePricesMEAN = metroMelbHousePrices.groupby('postcode').agg('mean').round(1).dropna()
metroMelbHousePricesFINAL = pd.merge(metroMelbHousePricesMED,metroMelbHousePricesMEAN,on='postcode', how='inner')
metroMelbHousePricesFINAL = metroMelbHousePricesFINAL.rename(columns={'Price_x': 'medPrice', 'Price_y': 'meanPrice'})
metroMelbHousePricesFINAL.to_csv('metroMelbHousePrices.csv', index='false')
melbPostcodes
