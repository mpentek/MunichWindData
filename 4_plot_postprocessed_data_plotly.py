import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import os

##################################
# DEFINITIONS
##################################

input_folder = os.path.join("3_postprocessed_data", "general")
input_ext = ".csv"
output_folder = os.path.join("4_dataplots","plotly")

##################################
# IMPORTING DATA
##################################

print("\nStarting importing data")

df_ranges_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_monthly_airp' + input_ext))
df_ranges_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_monthly_city' + input_ext))

df_dir_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_coarse_airp' + input_ext))
df_dir_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_coarse_city' + input_ext))

df_dir2_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_fine_airp' + input_ext))
df_dir2_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_fine_city' + input_ext))

df_comp_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_comp_mean_vs_max_airp' + input_ext))
df_comp_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_comp_mean_vs_max_city' + input_ext))

df_airp_m = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_mean_airp" + input_ext))
df_city_m = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_mean_city" + input_ext))

df_airp_g = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_max_airp" + input_ext))
df_city_g = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_max_city" + input_ext))

print("Ending importing data")

##########
# PLOTTING
##########

print("\nStarting plotting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Wind speed ranges
ranges = [2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5]
range_labels = ["<" + str(ranges[0])]
range_labels.extend([str(ranges[i])+"-"+str(ranges[i+1]) for i in [*range(len(ranges)-1)]])
range_labels.append(str(ranges[-1]) + ">")

# MONTHLY WINDS (airport)
fig1 = px.bar(df_ranges_a, x=df_ranges_a.index, y=range_labels, title='Monthly winds in Munich airport', labels={'index':'Month','value':'Frequency'}, color_discrete_sequence= px.colors.sequential.Plasma_r)
fig1.write_html(os.path.join(output_folder,"01_MonthWinds_airp.html"))
fig1.write_image(os.path.join(output_folder,"01_MonthWinds_airp.png"))
fig1.write_image(os.path.join(output_folder,"01_MonthWinds_airp.svg"))

# MONTHLY WINDS (city)
fig2 = px.bar(df_ranges_c, x=df_ranges_c.index, y=range_labels, title='Monthly winds in Munich city', labels={'index':'Month','value':'Frequency'}, color_discrete_sequence= px.colors.sequential.Plasma_r)
fig2.write_html(os.path.join(output_folder,"02_MonthWinds_city.html"))
fig2.write_image(os.path.join(output_folder,"02_MonthWinds_city.png"))
fig2.write_image(os.path.join(output_folder,"02_MonthWinds_city.svg"))

# WINDROSE (airport)
fig3 = px.bar_polar(df_dir_a, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich airport', color_discrete_sequence= px.colors.sequential.gray_r)
fig3.write_html(os.path.join(output_folder,"03_WindRose_airp.html"))
fig3.write_image(os.path.join(output_folder,"03_WindRose_airp.png"))
fig3.write_image(os.path.join(output_folder,"03_WindRose_airp.svg"))

# WINDROSE (city)
fig4 = px.bar_polar(df_dir_c, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich city', color_discrete_sequence= px.colors.sequential.gray_r)
fig4.write_html(os.path.join(output_folder,"04_WindRose_city.html"))
fig4.write_image(os.path.join(output_folder,"04_WindRose_city.png"))
fig4.write_image(os.path.join(output_folder,"04_WindRose_city.svg"))

# PRECISE WINDROSE (airport)
fig5 = px.bar_polar(df_dir2_a, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich airport', color_discrete_sequence= px.colors.sequential.gray_r)
fig5.write_html(os.path.join(output_folder,"05_WindRose_precise_airp.html"))
fig5.write_image(os.path.join(output_folder,"05_WindRose_precise_airp.png"))
fig5.write_image(os.path.join(output_folder,"05_WindRose_precise_airp.svg"))

# PRECISE WINDROSE (city)
fig6 = px.bar_polar(df_dir2_c, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich city', color_discrete_sequence= px.colors.sequential.gray_r)
fig6.write_html(os.path.join(output_folder,"06_WindRose_precise_city.html"))
fig6.write_image(os.path.join(output_folder,"06_WindRose_precise_city.png"))
fig6.write_image(os.path.join(output_folder,"06_WindRose_precise_city.svg"))

# GUST vs MEAN (airport)
fig7 = px.line(df_comp_a, x=df_comp_a.index, y=["Mean", "Max"], title='Mean vs Gust intensity in Munich airport')
fig7.update_yaxes(range=[0,6])
fig7.write_html(os.path.join(output_folder,"07_MeanVsMax_airp.html"))
fig7.write_image(os.path.join(output_folder,"07_MeanVsMax_airp.png"))
fig7.write_image(os.path.join(output_folder,"07_MeanVsMax_airp.svg"))

# GUST vs MEAN (city)
fig8 = px.line(df_comp_c, x=df_comp_c.index, y=["Mean", "Max"], title='Mean vs Gust intensity in Munich city')
fig8.update_yaxes(range=[0,6])
fig8.write_html(os.path.join(output_folder,"08_MeanVsMax_city.html"))
fig8.write_image(os.path.join(output_folder,"08_MeanVsMax_city.png"))
fig8.write_image(os.path.join(output_folder,"08_MeanVsMax_city.svg"))

# WIND SPEED DISTRIBUTION (airport)
data = df_airp_m['WindVelocity']
binwidth = 1
fig9 = px.histogram(df_airp_m, x='WindVelocity', histnorm='probability density', title='Wind intensity distribution in Munich airport')
fig9.update_traces(xbins=dict( # bins used for histogram
        start=int(min(data)),
        end=int(max(data)),
        size=binwidth
    ))
shape, loc, scale = stats.weibull_min.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.weibull_min.pdf(x_line, shape, loc, scale)
df_line = pd.DataFrame({"x": x_line, "y": y_line})
fig9.add_scatter(x=df_line["x"], y=df_line["y"], mode="lines", name="Weibull Distribution")
fig9.write_html(os.path.join(output_folder,"09_Histogram_mean_airp.html"))
fig9.write_image(os.path.join(output_folder,"09_Histogram_mean_airp.png"))
fig9.write_image(os.path.join(output_folder,"09_Histogram_mean_airp.svg"))

# WIND SPEED DISTRIBUTION (city)
data = df_city_m['WindVelocity']
binwidth = 1
fig10 = px.histogram(df_city_m, x='WindVelocity', histnorm='probability density', title='Wind intensity distribution in Munich city')
fig10.update_traces(xbins=dict( # bins used for histogram
        start=int(min(data)),
        end=int(max(data)),
        size=binwidth
    ))
shape, loc, scale = stats.weibull_min.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.weibull_min.pdf(x_line, shape, loc, scale)
df_line = pd.DataFrame({"x": x_line, "y": y_line})
fig10.add_scatter(x=df_line["x"], y=df_line["y"], mode="lines", name="Weibull Distribution")
fig10.write_html(os.path.join(output_folder,"10_Histogram_mean_city.html"))
fig10.write_image(os.path.join(output_folder,"10_Histogram_mean_city.png"))
fig10.write_image(os.path.join(output_folder,"10_Histogram_mean_city.svg"))

# WIND GUST DISTRIBUTION (airport)
data = df_airp_g['WindVelocity']
binwidth = 1
fig11 = px.histogram(df_airp_g, x='WindVelocity', histnorm='probability density', title='Gust intensity distribution in Munich airport')
fig11.update_traces(xbins=dict( # bins used for histogram
        start=int(min(data)),
        end=int(max(data)),
        size=binwidth
    ))
shape, loc, scale = stats.weibull_min.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.weibull_min.pdf(x_line, shape, loc, scale)
df_line = pd.DataFrame({"x": x_line, "y": y_line})
fig11.add_scatter(x=df_line["x"], y=df_line["y"], mode="lines", name="Weibull Distribution")
fig11.write_html(os.path.join(output_folder,"11_Histogram_max_airp.html"))
fig11.write_image(os.path.join(output_folder,"11_Histogram_max_airp.png"))
fig11.write_image(os.path.join(output_folder,"11_Histogram_max_airp.svg"))

# WIND GUST DISTRIBUTION (city)
data = df_city_g['WindVelocity']
binwidth = 1
fig12 = px.histogram(df_city_g, x='WindVelocity', histnorm='probability density', title='Gust intensity distribution in Munich city')
fig12.update_traces(xbins=dict( # bins used for histogram
        start=int(min(data)),
        end=int(max(data)),
        size=binwidth
    ))
shape, loc, scale = stats.weibull_min.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.weibull_min.pdf(x_line, shape, loc, scale)
df_line = pd.DataFrame({"x": x_line, "y": y_line})
fig12.add_scatter(x=df_line["x"], y=df_line["y"], mode="lines", name="Weibull Distribution")
fig12.write_html(os.path.join(output_folder,"12_Histogram_max_city.html"))
fig12.write_image(os.path.join(output_folder,"12_Histogram_max_city.png"))
fig12.write_image(os.path.join(output_folder,"12_Histogram_max_city.svg"))

print("Ending plotting data")