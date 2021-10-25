# %matplotlib notebook  #NOTE:  this command works with Jupyter Notebook, uncomment to make interactive elements of chart work correctly
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
import pandas as pd
import numpy as np


# Create the DF and the columns used later for calculations

# randomly generated data
np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

# data processing steps:
# create a sample mean column with apply
# create a bar chart with height = sample mean for each year (index on the x-axis)
# create a confidence interval of 95%  ---> sotre CI min and CI max in dataframe ---> then use the yerr function to overlay
# z score to use for 95% CI is 1.96, -1.96 
    
N = 3650   # if this was unknown we coudl also use the len function
df['Sample Mean'] =  df.apply(np.mean, axis = 1)
df['Sample StDev'] = df.apply(np.std, axis = 1)
df['Standard Error'] = df['Sample StDev'] / (N**.5)
df['CI_Upper'] = df['Sample Mean'] + (1.96)*df['Standard Error']
df['CI_Lower'] = df['Sample Mean'] - (1.96)*df['Standard Error']
df['CI_Delta'] = (1.96)*df['Standard Error']
df['Bar Year'] = df.index

# creates a colormap object   
colors= cm.get_cmap('seismic', 12)    

# formula / process of mapping the probabilites to color value
def prob2color (df, y_value):
    relation_dict = {1992:0, 1993:0, 1994:0, 1995:0}
    maxes = list(df['CI_Upper'])
    mins = list(df['CI_Lower'])
    n= 0 
    for key,val in relation_dict.items():
        if (maxes[n] - y_value) >= (maxes[n] - mins[n]):
            relation_dict[key] = .99999  # strange fix but change this to a number that approaches 1 not 1 itself              
        elif (maxes[n] - y_value) < 0 :
            relation_dict[key] = 0
        else:
            relation_dict[key] = (maxes[n] - y_value) / (maxes[n] - mins[n])
        n += 1
    # map these probabilities to my colormap
    df['Relation2Value'] = df['Bar Year'].map(relation_dict)  # this line is not really necessary just adds the color relations to the dataframe
    relations = list(df['Relation2Value'])                    # convert back into a list for easier processing
    my_cmap = [colors(i) for i in relations]
    
    return my_cmap

# Render the baseline plot
y_value = 40000  # adapt this to allow user to input the y_value of interest

# plot a horizontal line at the target vlaue level
Axes = plt.gca()
Axes.axhline(y = y_value , alpha = .65, color = 'darkslategrey', linestyle = '--')
Axes.set_title("Proximity to True Population Mean by Each Sample \n Your Target Value = {}".format(y_value))

plt.bar(df.index, df['Sample Mean'], yerr = errors, capsize = 10, color = prob2color(df, y_value), picker = 5) 

# put in colorbar
sm = ScalarMappable(cmap=colors)    
sm.set_array([])                    
cb = plt.colorbar(sm).update_normal(sm)   # store this guy in a variable so it can be cleared form the plot upon each iteration

#fix x-axis labels
labels = [1992,1993,1994,1995]
plt.xticks(labels)

# what needs to be done is we need to move the colorbar outside of the onclick function 
# render the baseline plot first, and onclick does not need to change the colorbar part of the axes, just update the mappable

# Next cell plots the above figure but with the interactive features built in
# click to move the horizontal line and explore various target values 
# how does each value change the proximity of each separate sample mean ? 


def onclick(event):
    
    # clear leftover noise from what existed before
    #s = copy.copy( fig.canvas.toolbar._views )        # this will make a copy of the image so that may clear colorbar command doesn't return a totally blank image each time
    #p = copy.copy( fig.canvas.toolbar._positions )    # not exactly sure how this works so worth looking into
    #im = plt.gca().images[-1]
    
    # clear the old line to draw new line
    plt.cla()
    
    # target point: 
    y = int(event.ydata)
    
    # perform that same color probability map function
    my_cmap = prob2color(df,y)
    
    # Make the Plot
    plt.bar(df.index, df['Sample Mean'], yerr = errors, capsize = 10, color = my_cmap)   
    plt.gca().axhline(y = event.ydata , alpha = .65, color = 'darkslategrey', linestyle = '--')
    labels = [1992,1993,1994,1995]
    plt.xticks(labels)
    
    #cb.remove()  # prevent the colorbar from copying each time   
    
    # clean up the ydata and then format title
    y = int(event.ydata)
    plt.gca().set_title("Proximity to True Population Mean by Each Sample \n Your Target Value = {}".format(y))    
    #plt.xticks(np.arange(1992, 1996, 1.0))
  
plt.ion()  # turns on the interactive mode (this must be a new feature since it was nto mentioned in lectures)
cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)   # call the onlick function so user can now interact with graph    
plt.savefig('Assignment 3.png', transparent = 'True')
