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
