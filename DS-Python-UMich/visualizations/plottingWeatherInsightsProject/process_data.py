# following function splits out components from dates, 
def process_data(weather_df):
    
    # convert column to datetime then split out indivudal date components with strftime
    weather_df['DATE'] = pd.to_datetime(weather_df['DATE'])
    weather_df['Month'] = weather_df['DATE'].dt.strftime('%B')
    weather_df['Mon']   = weather_df['DATE'].dt.strftime('%b')
    weather_df['Year'] = weather_df['DATE'].dt.strftime('%Y')
    weather_df['Day'] = weather_df['DATE'].dt.strftime('%d')
    weather_df['MMDD'] = weather_df['Mon'] + "-"+ weather_df['Day']
    #lansing_df['month_index'] = lansing_df['DATE'].dt.strftime('%-m')
    weather_df['MMYY'] = weather_df['Mon'] + "-"+ weather_df['Year']
    weather_df['snow_flag'] = np.where(weather_df['SNOW'] > 0, 1, 0)
    
    # Datetime indexes
    weather_df['month_index'] = pd.DatetimeIndex(weather_df['DATE']).month
    weather_df['DOY'] = pd.DatetimeIndex(weather_df['DATE']).dayofyear
    #weather_df

    # create a dict for later, plotting on the axis and labelling data by month: 
    days_map = list(weather_df['MMDD'].unique())
    days_dict = {}
    n = 1
    for item in days_map: 
        days_dict[item] = n
        n = n+1

    mmyy_map = list(weather_df['MMYY'].unique())
    mmyy_dict = {}
    n = 1
    for item in mmyy_map: 
        mmyy_dict[item] = n
        n = n+1
        
   
    #weather_df['month_index'] = 0 
    #weather_df['DOY'] = 0
    weather_df['mmyy_index'] = 0
    #weather_df['month_index'] = weather_df['Month'].map(month_map)
    #weather_df['DOY'] = weather_df['MMDD'].map(days_dict)
    weather_df['mmyy_index']  =  weather_df['MMYY'].map(mmyy_dict)
    weather_df = weather_df[weather_df['DOY'] != 366]

  
    # I use this column to make flags marking where the snow season begins and ends
    weather_df['index'] = weather_df.index

    # the below for loop surprisingly was the only way I could figure out how to make snow flags
    # the idea here was to mark the first and last day of every year that it snowed -- though this is not used in final plot
    last_dict = {}
    first_dict = {}
    for year in weather_df['Year'].unique():
        # want to capture the first and last day it snowed each year 
        snow_df = weather_df[weather_df['Year'] == year]
        # approximately 180th day of the year shoud be in the middle of hot weather
        spring = snow_df.where(snow_df['DOY'] < 180).dropna()
        spring =  spring[spring['snow_flag'] == 1]
        fall =  snow_df.where(snow_df['DOY'] > 180 ).dropna()
        fall =  fall[fall['snow_flag'] == 1]
        
        # append the index of each day to dictionaries and save
        try: last = np.argmax(spring['DOY'])
        except: last = year
        try: first = np.argmin(fall['DOY'])
        except:  first = year
            
        last_dict[last] = 1
        first_dict[first] = 1 
        
    # now this should create two new columns where have flags for the first and last days of snow each year
    weather_df['last_snow'] = weather_df['index'].map(last_dict)
    weather_df['last_snow'] = weather_df['last_snow'].fillna(0)
    weather_df['first_snow'] = weather_df['index'].map(first_dict)
    weather_df['first_snow'] = weather_df['first_snow'].fillna(0)


    return (weather_df)