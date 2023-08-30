import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
# import plotly.express as px

import os

from dwd_data_info import dwd_data_info

##################################
# DEFINITIONS
##################################

input_folder = "downloaded_data_files"
output_folder = "postprocessed_data"
output_ext = ".csv"

##################################
# READ DATA AND INITIALIZE PANDAS
##################################

print("\nStarting reading and initializing")
# City mean wind information
df_city_m = pd.read_csv(os.path.join(input_folder, dwd_data_info["CityMean"]["file_name"]), sep=";")    
# City gust wind information
df_city_g = pd.concat([pd.read_csv(os.path.join(input_folder, dwd_data_info["CityGust1"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["CityGust2"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["CityGust3"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["CityGust4"]["file_name"]), sep=";")])    

# Airport mean wind information
df_airp_m = pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpMean"]["file_name"]), sep=";")
# Airport gust wind information
df_airp_g = pd.concat([pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpGust1"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpGust2"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpGust3"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpGust4"]["file_name"]), sep=";")])    

dataframes = [df_airp_m, df_city_m, df_airp_g, df_city_g]
print("Ending reading and intializing")

##################################
# FILTERING AND PROCESSING OF DATA
##################################

print("\nStarting filtering and postprocessing")

for i, df in enumerate(dataframes):
    if i < 2:
        df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H')      # Converting to datetime format
    else:
        df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H%M')
    df = df.rename(columns={'MESS_DATUM':'Date',                                    # Renaming columns to more descriptive names
                            'STATIONS_ID':'Station',
                            'QN':'QualityLevel',
                            'QN_3':'QualityLevel',
                            '   F':'WindSpeed',
                            '   D':'WindDirection',
                            'FX_10':'MaxSpeed',
                            'DX_10':'MaxDir',
                            'FMX_10':'MaxMean',
                            'FNX_10':'MinSpeed'})
    df = df.set_index(['Date'])
    try:
        # NOTE: this throws and error, why?
        del df['eor'] # Deleting end Of Report column
    except:
        pass
    
    if i < 2:
        df = df[df.WindSpeed >= 0]                                                  # Keeping only positive values
        df = df[df.WindDirection >= 0]
    else:
        df = df[df.MaxSpeed >= 0]
        df = df.replace({-999.0: np.nan})                                           # Not available data are stored as "-999.0"
    dataframes[i] = df
[df_airp_m, df_city_m, df_airp_g, df_city_g] = dataframes[:]                              # Assigning the obtained values back to the original variables

date_lim = datetime(1997, 7, 1)                                                     # Using only data generated by automated stations (from 1997 for the city station)
df_city_m = df_city_m[df_city_m.index > date_lim]

### 1.- MEAN

# Wind speed ranges
ranges = [1, 3, 6, 10]      # Slices into which the wind intensity is to be divided into
dataframes_a = []           # Stores the different subsets of data based on the wind intensity. dataframes_a[0] will only have the entries where the wind was at lowest intensity
dataframes_c = []
dataframes_a.append(df_airp_m[df_airp_m.WindSpeed < ranges[0]])
dataframes_c.append(df_city_m[df_city_m.WindSpeed < ranges[0]])
for i in range(1, len(ranges)):
    dataframes_a.append(df_airp_m[(df_airp_m.WindSpeed > ranges[i-1]) & (df_airp_m.WindSpeed < ranges[i])])
    dataframes_c.append(df_city_m[(df_city_m.WindSpeed > ranges[i-1]) & (df_city_m.WindSpeed < ranges[i])])
dataframes_a.append(df_airp_m[df_airp_m.WindSpeed > ranges[-1]])
dataframes_c.append(df_city_m[df_city_m.WindSpeed > ranges[-1]])

months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
directions2 = np.arange(0, 360, 10).tolist()     # 10-degree steps

# Wind speed ranges per month
ranges_a = np.zeros((12,len(ranges)+1))             # Stores how often in month (i+1) the wind has been blowing with intensity j
ranges_c = np.zeros((12,len(ranges)+1))
for i in range(12):
    for j, df in enumerate(dataframes_a):
        ranges_a[i,j] = len(df.loc[df.index.month == i+1].WindSpeed)
    for j, df in enumerate(dataframes_c):
        ranges_c[i,j] = len(df.loc[df.index.month == i+1].WindSpeed)
df_ranges_a = pd.DataFrame(ranges_a, index=months, columns=["<1","1-3","3-6","6-10",">10"])
df_ranges_a.index.name="Months"
df_ranges_c = pd.DataFrame(ranges_c, index=months, columns=["<1","1-3","3-6","6-10",">10"])
df_ranges_c.index.name="Months"

for i,month in enumerate(months):       # Rescaling the frequency value to the number of days in each month
    if i==0 or i==2 or i==4 or i==6 or i==7 or i==9 or i==11:
        df_ranges_a.loc[month] = df_ranges_a.loc[month] / df_ranges_a.loc[month].sum() * 31
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 31
    elif i==1:
        df_ranges_a.loc[month] = df_ranges_a.loc[month] / df_ranges_a.loc[month].sum() * 28
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 28
    else:
        df_ranges_a.loc[month] = df_ranges_a.loc[month] / df_ranges_a.loc[month].sum() * 30
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 30

# Wind ranges per direction (8 Himmelrichtungen)
# 8 directions = 360/8 = 45 deg precision
total_range = 360.0
direction_nr = len(directions) #8
slice_size = total_range / direction_nr #45
half_slice_size = slice_size / 2 #22.5
dir_a = np.zeros((direction_nr,len(ranges)+1))
dir_c = np.zeros((direction_nr,len(ranges)+1))
for j, df in enumerate(dataframes_a):
    dir_a[0,j] = len(df[(df.WindDirection > total_range-half_slice_size) | (df.WindDirection < half_slice_size)])
for j, df in enumerate(dataframes_c):
    dir_c[0,j] = len(df[(df.WindDirection > total_range-half_slice_size) | (df.WindDirection < half_slice_size)])
for i in range(1,direction_nr):
    for j, df in enumerate(dataframes_a):
        dir_a[i,j] = len(df[(df.WindDirection > (slice_size*i)-half_slice_size) & (df.WindDirection < (slice_size*i)+half_slice_size)])       
    for j, df in enumerate(dataframes_c):
        dir_c[i,j] = len(df[(df.WindDirection > (slice_size*i)-half_slice_size) & (df.WindDirection < (slice_size*i)+half_slice_size)]) 

df_dir_a = pd.DataFrame(dir_a, index=directions, columns=["<1","1-3","3-6","6-10",">10"])   # Creating a df from the arrays obtained
df_dir_c = pd.DataFrame(dir_c, index=directions, columns=["<1","1-3","3-6","6-10",">10"])
df_dir_a = pd.melt(df_dir_a.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')   # Changes df type from "wide" to "long"
df_dir_c = pd.melt(df_dir_c.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')
df_dir_a.rename(columns={'index': 'Direction'}, inplace=True)
df_dir_c.rename(columns={'index': 'Direction'}, inplace=True)
df_dir_a.index.name="RangeTimesDirCount"
df_dir_c.index.name="RangeTimesDirCount"

# Wind ranges per direction (10-degree precision)
# 36 directions = 360/36 = 10 deg precision
total_range = 360.0
direction_nr = len(directions2) #36
slice_size = total_range / direction_nr #10
half_slice_size = slice_size / 2 #5
dir2_a = np.zeros((direction_nr,len(ranges)+1))
dir2_c = np.zeros((direction_nr,len(ranges)+1))
for j,df in enumerate(dataframes_a):
    dir2_a[0,j] = len(df[(df.WindDirection > total_range-half_slice_size) | (df.WindDirection < half_slice_size)])
for j,df in enumerate(dataframes_c):
    dir2_c[0,j] = len(df[(df.WindDirection > total_range-half_slice_size) | (df.WindDirection < half_slice_size)])
for i in range(1,direction_nr):
    for j, df in enumerate(dataframes_a):
        dir2_a[i,j] = len(df[(df.WindDirection > (slice_size*i)-half_slice_size) & (df.WindDirection < (slice_size*i)+half_slice_size)])
    for j, df in enumerate(dataframes_c):
        dir2_c[i,j] = len(df[(df.WindDirection > (slice_size*i)-half_slice_size) & (df.WindDirection < (slice_size*i)+half_slice_size)])   

df_dir2_a = pd.DataFrame(dir2_a, index=directions2, columns=["<1","1-3","3-6","6-10",">10"])
df_dir2_c = pd.DataFrame(dir2_c, index=directions2, columns=["<1","1-3","3-6","6-10",">10"])
df_dir2_a = pd.melt(df_dir2_a.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')    
df_dir2_c = pd.melt(df_dir2_c.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')
df_dir2_a.rename(columns={'index': 'Direction'}, inplace=True)
df_dir2_c.rename(columns={'index': 'Direction'}, inplace=True)
df_dir2_a.index.name="RangeTimesDirCount"
df_dir2_c.index.name="RangeTimesDirCount"

### 2.- GUST

# Comparison mean vs gust speed per month
df_comp_a = pd.DataFrame(index=months, columns=["Mean", "Gust"])        # Stores monthly average of the mean and gust winds
df_comp_a.index.name="Months"
df_comp_a['Mean'] = df_airp_m.groupby(df_airp_m.index.month).mean().WindSpeed.to_list()
df_comp_a['Gust'] = df_airp_g.groupby(df_airp_g.index.month).mean().MaxSpeed.to_list()

df_comp_c = pd.DataFrame(index=months, columns=["Mean", "Gust"])
df_comp_c.index.name="Months"
df_comp_c['Mean'] = df_city_m.groupby(df_city_m.index.month).mean().WindSpeed.to_list()
df_comp_c['Gust'] = df_city_g.groupby(df_city_g.index.month).mean().MaxSpeed.to_list()

print("Ending filtering and postprocessing")

##################################
# EXPORTING DATA
##################################

print("\nStarting exporting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df_ranges_a.to_csv(os.path.join(output_folder,'wind_velocity_mean_monthly_airp' + output_ext))
df_ranges_c.to_csv(os.path.join(output_folder,'wind_velocity_mean_monthly_city' + output_ext))

df_dir_a.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_coarse_airp' + output_ext))
df_dir_c.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_coarse_city' + output_ext))

df_dir2_a.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_fine_airp' + output_ext))
df_dir2_c.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_fine_city' + output_ext))

df_comp_a.to_csv(os.path.join(output_folder,'wind_velocity_comp_gust_vs_mean_airp' + output_ext))
df_comp_c.to_csv(os.path.join(output_folder,'wind_velocity_comp_gust_vs_mean_city' + output_ext))

df_airp_m.to_csv(os.path.join(output_folder,"wind_velocity_distrib_mean_airp" + output_ext))
df_city_m.to_csv(os.path.join(output_folder,"wind_velocity_distrib_mean_city" + output_ext))

df_airp_g.to_csv(os.path.join(output_folder,"wind_velocity_distrib_gust_airp" + output_ext))
df_city_g.to_csv(os.path.join(output_folder,"wind_velocity_distrib_gust_city" + output_ext))

print("Ending exporting data")