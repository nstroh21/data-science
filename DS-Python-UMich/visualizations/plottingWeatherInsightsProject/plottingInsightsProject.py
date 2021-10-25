#https://www.ncdc.noaa.gov/cdo-web/datatools/findstation
#https://www.ncdc.noaa.gov/cdo-web/search
import pandas as pd
import numpy as np


annarbor_df = pd.read_csv('NCEI_AnnArbor_2000-2019.csv')
siouxcity_df = pd.read_csv('NCEI_SiouxCity_2000-2019.csv')
umich_df = pd.read_csv('NCEI_UMich_2000-2019.csv')
umich_df = umich_df[['DATE', 'SNOW']]

annarbor_df  = pd.merge(annarbor_df, umich_df, on = 'DATE')

annarbor_df['SNWD'] = annarbor_df['SNWD'].fillna(0)
annarbor_df['SNOW'] = annarbor_df['SNOW'].fillna(0)

#drop tsun metric as it seems to just be null anyway:
annarbor_df = annarbor_df.drop('TSUN', axis = 1)
siouxcity_df = siouxcity_df.drop('TSUN', axis = 1)

# In excel this was a good estimate, fill null values with this estimate
annarbor_df['TAVG']  = (annarbor_df['TMAX'] + annarbor_df['TMIN'])  / 2

# drop 2020 from siouxcity_df
siouxcity_df = siouxcity_df.iloc[:7305]

siouxcity_df.tail(20)


# test lines
#process_data(siouxcity_df)
#annarbor_df['last_snow'] = annarbor_df['index'].map(last_dict2).fillna(0)
#annarbor_df['first_snow'] = annarbor_df['index'].map(first_dict2).fillna(0)
#aa_snow_season = [ int(np.mean(annarbor_df[annarbor_df['first_snow'] == 1]['DOY'])), int(np.mean(annarbor_df[annarbor_df['last_snow'] == 1]['DOY']) )  ]

# this function processes a datafram into a series that can be charted on an x,y plot. Offers multiple agg_types (just sum adn avg here)
def create_series(weather_df, agg_type):

    mid_month_ticks = [15, 47, 75, 105, 136, 166, 197, 227, 258, 288, 319, 350]
    
    # various types of aggregations
    monthagg_df = weather_df.groupby(['month_index']).agg({'PRCP': ['mean', 'sum'], 'SNOW' : ['mean', 'sum'],  'TAVG' : ['mean' , 'sum'], 'AWND': ['mean', 'sum']})   
    doyagg_df   = weather_df.groupby(['DOY']).agg({'PRCP': ['mean', 'sum'], 'SNOW' : ['mean', 'sum'], 'TAVG' : ['mean' , 'sum'], 'AWND': ['mean', 'sum']})
    mmyyagg_df  = weather_df.groupby(['mmyy_index']).agg({'PRCP': ['mean', 'sum'], 'SNOW' : ['mean', 'sum'], 'TAVG' : ['mean' , 'sum'], 'AWND': ['mean', 'sum']})
    #yearagg_df  = weather_df.groupby()
    
    # try one more special type of aggregation to get smoother graphing
    even_days = list(weather_df['DOY'].unique())
    even_dict = {}
    for j in even_days:
        if j % 15 == 0:
            even_dict[j] = 1
        else:
            even_dict[j] = 0
            
    weather_df['even_days'] = weather_df['DOY'].map(even_dict)
    evens_only = weather_df[weather_df['even_days'] == 1]
    
    semiagg_df = evens_only.groupby(['DOY']).agg({'PRCP': ['mean', 'sum'], 'SNOW' : ['mean', 'sum'],  'TAVG' : ['mean' , 'sum'], 'AWND': ['mean', 'sum']})
    
    # idea of how to add functionality to user of this function -- multiple keywords/aggreagtions are accepted
    if agg_type.lower() == 'sum' : 
        rain = monthagg_df['PRCP']['sum'] 
        snow = monthagg_df['SNOW']['sum']
        #temp = mmyyagg_df['TAVG']['sum']
        #wind = doyagg_df['AWND']['sum']
       
    elif (agg_type.lower() == 'average' or agg_type.lower() == 'avg' or agg_type.lower() == 'mean'):
        rain = semiagg_df['PRCP']['mean'] 
        snow = semiagg_df['SNOW']['mean']
        #temp = mmyyagg_df['TAVG']['mean'] / 10
        #wind = doyagg_df['AWND']['mean']
      
    else: 
        print(str(agg_type)  + " is not a valid entry")

    
    return (rain, snow)

