import pandas as pd
import re
doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
df.head()

import numpy as np
df1 = pd.DataFrame(df, columns = ['text'])
def date_sorter():
    
    df1 = pd.DataFrame(df, columns = ['text'])
    df1['index'] = df1.index
    # df1['standard']  = re.search('\d{1,2}[-/]\d{1,2}[-/]\d{2,4}' , df1['text'])
    #instead it might be better when working with dataframes to use the "contains" function
    
        # create one regular expression for all dates that might be in the mm/dd/yyyy format   
    def split_standard(df):
        
        df['standard'] = df['text'].str.contains('\d{1,2}[-/]\d{1,2}[-/]\d{2,4}')
    
        # Now these are going to go in one category, sub-dataframe (do I need to do this?  Does this actually help in any way?)
        dff = df[df['standard'] == False].copy()
        dft = df[df['standard'] == True].copy()
    
        #Extract standard date convert to datetime type
        # also, we will simply assume that the first match is the date of the event
        dft['date2'] = pd.to_datetime(dft['text'].str.extract('(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'))
    
        #save the original index as a column when for final sorting
        dft['index'] = dft.index
        
        return(dft, dff)


    def split_monthyear(df2) :

        # part 1:   month-year where month is int ... 
        #because we already did standard format we don't have to worry about any of these having days as well (assume)
       
        df2['mynum'] = df2['text'].str.contains('\d{1,2}/\d{2,4}')
        dffal = df2[df2['mynum'] == False].copy()
        mynum = df2[df2['mynum'] == True].copy()
        mynum['date'] = mynum['text'].str.extract('(\d{1,2}/\d{2,4})')
        mynum['month'] = mynum['date'].str.extract('(\d{1,2})/')
        mynum['day'] = 1
        mynum['year'] =  mynum['date'].str.extract('/(\d{2,4})')
        mynum['date2'] = pd.to_datetime(mynum[['month', 'day', 'year']]) 
        mynum['index'] = mynum.index
    
       
        
        # part 2: month - year where month is a string
    
        month_map_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 
                                          'Aug':8, 'Sep':9, 'Oct': 10, 'Nov':11, 'Dec' : 12 }
       
        # consistently changing the names of these dataframe copies is getting around the dead kernel issue
        # making the copies solved the problem in the first place
        #maybe it is getting overwhlemed by making several assignments to the same variable name (although that seems weird)
        
        
        #this ends up being a convoluted solution but because when the date is at the start of string it wasn't matching ... 
        # i added | (^repeat same regex)
        # the reason it didnt capture start of string is because I negated digits at the beggining 9to prevent day-month-year matches
    
        dffal['my'] = dffal['text'].str.contains('([^0-9].(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[,]?.\d{4})|(^(.)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[,]?.\d{4})')
        
        my = dffal[dffal['my'] == True].copy()
        not_my = dffal[dffal['my'] == False].copy()
        my['date'] = my['text'].str.extract('((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[,]?.\d{4})')
        my['text month'] = my['date'].str.extract('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)')
        my['day'] = 1
        my['year'] = my['date'].str.extract('(\d{4})')
        my['month'] = my['text month'].map(month_map_dict).fillna(1)
        my['date2'] = pd.to_datetime(my[['month', 'day', 'year']]) 
        my['index'] = my.index
    
    
        # final = pd.merge(mynum, not_my, on = 'index', how = 'inner')
        # use this merge test to ensure these sets are now all distinct
    
        mynum2 = mynum[['text', 'date2', 'index']]
        my2    = my[['text', 'date2', 'index']]
        my_final  = pd.concat([mynum2, my2] )
    
    
        return (my_final, not_my)
       
    
    def mdy_text(not_my):
        
        #we'll be needing this dict again
        month_map_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 
                                          'Aug':8, 'Sep':9, 'Oct': 10, 'Nov':11, 'Dec' : 12 }
    
        # (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* ---> this is the regex to match any month name
        # we also have period or hyphen potentially   --- > (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.-]?[a-z]* 
        # For day ---- > ('\d{1,2}[a-z]{0,2}[,]?') could be followed by th, st, nd or a comma (i think \w* would also work but this way feels more specific
        # I'll try the wildcard after day just to try to capture all variants at once    
        # I was actually undable to catch all month-year combinations but I'm going to move on and try the submission anyway
        # ( they were at the beginning of the string so we'd use ^ to match them but this was causing kernel to die again)
    
        not_my['mdy'] = not_my['text'].str.contains('(\d{1,2}[a-z]{0,2}.{1,2})?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.-]?[a-z]*.? )(\d{1,2}[a-z]{0,2}.{1,2})?(\d{2,4})')
        mdy = not_my[not_my['mdy'] == True]
        not_mdy = not_my[not_my['mdy'] == False]
        #remember to put in ?: in each () group because that tells the extract function not to treat that as an extract group
        mdy['date'] = mdy['text'].str.extract('((?:\d{1,2}[a-z]{0,2}.{1,2})?(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*.? )(?:\d{1,2}[a-z]{0,2}.{1,2})?(?:\d{4}))')
        # to prevent a day match ... we have to extract only the year out of the whole thing  ?: = don't extract
        mdy['year'] = mdy['date'].str.extract('(\d{4})')
        mdy['text_month'] = mdy['date'].str.extract('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)')
        mdy['day'] = mdy['date'].str.extract('(\d{1,2})')
        mdy['month'] = mdy['text_month'].map(month_map_dict)
        mdy['date2'] = pd.to_datetime(mdy[['month' , 'day' , 'year']])
        mdy['index'] = mdy.index
        
        mdy_final = mdy[['text', 'date2', 'index']]
        
        return  (mdy_final, not_mdy)
    
    def year(not_mdy):
        not_mdy['yr'] = not_mdy['text'].str.contains('\d{4}')
        yrdf = not_mdy[not_mdy['yr'] == True]
        #notyr = not_mdy[not_mdy['yr'] == False]   # sweet this is empty whihc is exactly what we expect/want
        yrdf['year'] = yrdf['text'].str.extract('(\d{4})')
        yrdf['month'] = 1
        yrdf['day'] = 1
        yrdf['date2'] = pd.to_datetime(yrdf[['year', 'month', 'day']])
        yrdf['index'] = yrdf.index
        yrdf_final = yrdf[['text', 'date2', 'index']]

        #mynum = split_monthyear(dff)
        return yrdf_final

    
    dft, dff = split_standard(df1)
    dft = dft[['text', 'date2', 'index']]
    #final0 = pd.merge(df1, dft, on = 'index', how = 'inner')
    my_final, not_my = split_monthyear(dff)
    mdy_final, not_mdy = mdy_text(not_my)
    yrdf_final = year(not_mdy)
    
    df_list = [dft, my_final, mdy_final, yrdf_final]
    
    date_df = pd.concat(df_list)
    
    sort_date = date_df.sort_values(by = 'date2', ascending = True).reset_index(drop =True)
    #sort_date['rank'] = sort_date.index
    #sort_index = sort_date.sort_values(by = 'index', ascending = True)
    #sort_index = sort_index.set_index('index', drop =False)
    
    # i formatted the answer wrongly, what we actually want to do is keep it in chronological order, just with the original indices tagging each date
    
    
    return sort_date['index']
    

    
date_sorter()
    
#answer = date_sorter()

#answer.to_csv('answer.csv')
#df1.to_csv('dates_basis.csv')

# test with these missing null values:
# where do they originate? [233,240,244,273,311,317,328,329,338,339]

# start of string month-year issue:
#[235, 341, 270 ,281, 306,266, 321, 251, 333, 245, 256, 276, 285, 247, 294, 283, 299]


# i formatted the answer wrongly, what we actually want to do is keep it in chronological order, just with the original indices tagging each date
    