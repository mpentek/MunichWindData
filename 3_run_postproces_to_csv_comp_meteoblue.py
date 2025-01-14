import pandas as pd
import numpy as np
from datetime import datetime
import os

from dwd_data_info import dwd_data_info

##################################
# DEFINITIONS
##################################

input_folder = "2_filtered_data"
input_ext = ".csv"
output_folder = os.path.join("3_postprocessed_data", "comp_meteoblue")
output_ext = ".csv"

##################################
# READ DATA AND INITIALIZE PANDAS
##################################

print("\nStarting reading and initializing")
# City mean wind information
df_city_m = pd.read_csv(os.path.join(input_folder, 'wind_10min_mean_city' + input_ext), sep=",")

dataframes = [df_city_m]
print("Ending reading and intializing")

##################################
# FILTERING AND PROCESSING OF DATA
##################################

print("\nStarting filtering and postprocessing")

for i,df in enumerate(dataframes):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index(['Date'])
    dataframes[i] = df
[df_city_m] = dataframes[:]


### 1.- MEAN

# Wind speed ranges
# for comparison with MeteoBlue data:
# they have ranges in km/h: "<1","1-5","5-12","12-19","19-28","28-38","38-50","50-61",">61"
# the conversion factor is dividing by 3.6 to get to m/s
# km/h -> [1.00, 5.00, 12.00, 19.00, 28.00, 38.00, 50.00, 61.00]
# m/s  -> [0.28, 1.39,  3.33,  5.28,  7.78, 10.56, 13.89, 16.95]
ranges = [0.28, 1.39, 3.33, 5.28, 7.78, 10.56, 13.89, 16.95]
ranges_kmh = [1.00, 5.00, 12.00, 19.00, 28.00, 38.00, 50.00, 61.00]
range_labels = ["<" + str(ranges_kmh[0])]
range_labels.extend([str(ranges_kmh[i])+"-"+str(ranges_kmh[i+1]) for i in [*range(len(ranges_kmh)-1)]])
range_labels.append(str(ranges_kmh[-1]) + ">")

dataframes_c = []
dataframes_c.append(df_city_m[df_city_m.WindVelocity < ranges[0]])
for i in range(1, len(ranges)):
    dataframes_c.append(df_city_m[(df_city_m.WindVelocity > ranges[i-1]) & (df_city_m.WindVelocity < ranges[i])])
dataframes_c.append(df_city_m[df_city_m.WindVelocity > ranges[-1]])

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
directions2 = np.arange(0, 360, 10).tolist()     # 10-degree steps

# Wind speed ranges per month
nr_months = len(months)
ranges_c = np.zeros((nr_months,len(ranges)+1))
for i in range(nr_months):
    for j, df in enumerate(dataframes_c):
        ranges_c[i,j] = len(df.loc[df.index.month == i+1].WindVelocity)
df_ranges_c = pd.DataFrame(ranges_c, index=months, columns=range_labels)
df_ranges_c.index.name="Months"

for i,month in enumerate(months):       # Rescaling the frequency value to the number of days in each month
    if i==0 or i==2 or i==4 or i==6 or i==7 or i==9 or i==11:
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 31
    elif i==1:
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 28
    else:
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 30

# Wind ranges per direction (10-degree precision)
# 36 directions = 360/36 = 10 deg precision
total_range = 360.0
direction_nr = len(directions2) #36
slice_size = total_range / direction_nr #10
half_slice_size = slice_size / 2 #5
dir2_c = np.zeros((direction_nr,len(ranges)+1))
for j,df in enumerate(dataframes_c):
    dir2_c[0,j] = len(df[(df.WindDirection > total_range-half_slice_size) | (df.WindDirection < half_slice_size)])
for i in range(1,direction_nr):
    for j, df in enumerate(dataframes_c):
        dir2_c[i,j] = len(df[(df.WindDirection > (slice_size*i)-half_slice_size) & (df.WindDirection < (slice_size*i)+half_slice_size)])   

df_dir2_c = pd.DataFrame(dir2_c, index=directions2, columns=range_labels)
df_dir2_c = pd.melt(df_dir2_c.reset_index(), id_vars=['index'], var_name='SpeedRange [km/h]', value_name='Frequency')
df_dir2_c.rename(columns={'index': 'Direction'}, inplace=True)
df_dir2_c.index.name="RangeTimesDirCount"

### 2.- GUST

print("Ending filtering and postprocessing")

##################################
# EXPORTING DATA
##################################

print("\nStarting exporting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


df_ranges_c.to_csv(os.path.join(output_folder,'wind_velocity_mean_monthly_city' + output_ext))

df_dir2_c.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_fine_city' + output_ext))

print("Ending exporting data")