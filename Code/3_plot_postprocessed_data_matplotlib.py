import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os

##################################
# DEFINITIONS
##################################

input_folder = "postprocessed_data"
input_ext = ".csv"
output_folder = os.path.join("dataplots","matplotlib")

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

df_comp_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_comp_gust_vs_mean_airp' + input_ext))
df_comp_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_comp_gust_vs_mean_city' + input_ext))

df_airp_m = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_mean_airp" + input_ext))
df_city_m = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_mean_city" + input_ext))

df_airp_g = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_gust_airp" + input_ext))
df_city_g = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_gust_city" + input_ext))

print("Ending importing data")

##########
# PLOTTING
##########
'''
# AVERAGE WINDS PER YEAR
plt.figure(figsize=(10.5,5))
plt.title('Average winds in Munich city and airport')

years = [np.arange(1997, 2023, 1),
         np.arange(1992, 2023, 1)]
yearly_winds1 = df_city_m.groupby(df_city_m.index.to_period('A')).mean()    # city
yearly_winds2 = df_airp_m.groupby(df_airp_m.index.to_period('A')).mean()    # airport

plt.subplot(121)
plt.bar(years[0], yearly_winds1['WindSpeed'])
plt.xlabel('Year')
plt.ylabel('[m/s]')
plt.title('Munich city')
plt.ylim([0,4])

plt.subplot(122)
plt.bar(years[1], yearly_winds2['WindSpeed'])
plt.xlabel('Year')
plt.ylabel('[m/s]')
plt.title('Munich airport')
plt.ylim([0,4])

plt.show()
'''

print("\nStarting plotting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# # MONTHLY WINDS (airport)
# fig = plt.figure(1)
# plt.title("Monthly winds in Munich airport")
# for idx, range_label in enumerate(["<1","1-3","3-6","6-10",">10"]):
#     if idx == 0:
#         plt.bar(df_ranges_a["Months"],df_ranges_a[range_label], label=range_label)
#         prev_values = df_ranges_a[range_label]
#     else:
#         plt.bar(df_ranges_a["Months"],df_ranges_a[range_label], bottom=prev_values, label=range_label)
#         prev_values = np.add(prev_values,df_ranges_a[range_label])
# plt.grid()
# plt.legend()
# plt.savefig(os.path.join(output_folder,"01_MonthWinds_airp.png"))
# plt.savefig(os.path.join(output_folder,"01_MonthWinds_airp.pdf"))

# # MONTHLY WINDS (city)
# fig = plt.figure(2)
# plt.title("Monthly winds in Munich city")
# for idx, range_label in enumerate(["<1","1-3","3-6","6-10",">10"]):
#     if idx == 0:
#         plt.bar(df_ranges_c["Months"],df_ranges_a[range_label], label=range_label)
#         prev_values = df_ranges_a[range_label]
#     else:
#         plt.bar(df_ranges_c["Months"],df_ranges_a[range_label], bottom=prev_values, label=range_label)
#         prev_values = np.add(prev_values,df_ranges_a[range_label])
# plt.grid()
# plt.legend()
# plt.savefig(os.path.join(output_folder,"02_MonthWinds_city.png"))
# plt.savefig(os.path.join(output_folder,"02_MonthWinds_city.pdf"))

# Windrose needs: https://python-windrose.github.io/windrose/index.html
# pip install windrose

# WIP
# fig, ax = plt.subplots()
# from windrose import WindroseAxes

# ax = WindroseAxes.from_ax()
# ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
# ax.set_legend()

# # WINDROSE (airport)
# fig3 = px.bar_polar(df_dir_a, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich airport', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig3.write_html(os.path.join(output_folder,"03_WindRose_airp.html"))
# fig3.write_image(os.path.join(output_folder,"03_WindRose_airp.png"))
# fig3.write_image(os.path.join(output_folder,"03_WindRose_airp.svg"))

# # WINDROSE (city)
# fig4 = px.bar_polar(df_dir_c, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich city', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig4.write_html(os.path.join(output_folder,"04_WindRose_city.html"))
# fig4.write_image(os.path.join(output_folder,"04_WindRose_city.png"))
# fig4.write_image(os.path.join(output_folder,"04_WindRose_city.svg"))

# # PRECISE WINDROSE (airport)
# fig5 = px.bar_polar(df_dir2_a, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich airport', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig5.write_html(os.path.join(output_folder,"05_WindRose_precise_airp.html"))
# fig5.write_image(os.path.join(output_folder,"05_WindRose_precise_airp.png"))
# fig5.write_image(os.path.join(output_folder,"05_WindRose_precise_airp.svg"))

# # PRECISE WINDROSE (city)
# fig6 = px.bar_polar(df_dir2_c, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich city', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig6.write_html(os.path.join(output_folder,"06_WindRose_precise_city.html"))
# fig6.write_image(os.path.join(output_folder,"06_WindRose_precise_city.png"))
# fig6.write_image(os.path.join(output_folder,"06_WindRose_precise_city.svg"))

# # GUST vs MEAN (airport)
# fig = plt.figure(7)
# plt.title("Mean vs Gust intensity in Munich airport")
# plt.plot(df_comp_a["Months"],df_comp_a["Mean"], 'b-.', label="Mean")
# plt.plot(df_comp_a["Months"],df_comp_a["Gust"], 'r--', label="Gust")
# plt.grid()
# plt.legend()
# plt.savefig(os.path.join(output_folder,"07_GustvsMean_airp.png"))
# plt.savefig(os.path.join(output_folder,"07_GustvsMean_airp.pdf"))

# # GUST vs MEAN (city)
# fig = plt.figure(8)
# plt.title("Mean vs Gust intensity in Munich city")
# plt.plot(df_comp_c["Months"],df_comp_a["Mean"], 'b-.', label="Mean")
# plt.plot(df_comp_c["Months"],df_comp_a["Gust"], 'r--', label="Gust")
# plt.grid()
# plt.legend()
# plt.savefig(os.path.join(output_folder,"08_GustvsMean_city.png"))
# plt.savefig(os.path.join(output_folder,"08_GustvsMean_city.pdf"))

plt.show()

# # WIND SPEED DISTRIBUTION (airport)
# fig9 = px.histogram(df_airp_m, x='WindSpeed', nbins=100, title='Wind intenstiy distribution in Munich airport')
# fig9.update_layout(bargap = 0.05)
# fig9.update_xaxes(range=[0,20])
# shape, loc, scale = stats.weibull_min.fit(df_airp_m['WindSpeed'])     # Weibull distribution fit
# x_line = np.linspace(np.min(df_airp_m['WindSpeed']), np.max(df_airp_m['WindSpeed']), 100)
# y_line = stats.weibull_min.pdf(x_line, shape, loc, scale) * 125000
# df_line = pd.DataFrame({"x": x_line, "y": y_line})
# fig9.add_scatter(x=df_line["x"], y=df_line["y"], mode="lines", name="Weibull Distribution")
# fig9.write_html(os.path.join(output_folder,"09_Histogram_airp.html"))
# fig9.write_image(os.path.join(output_folder,"09_Histogram_airp.png"))
# fig9.write_image(os.path.join(output_folder,"09_Histogram_airp.svg"))

# # WIND SPEED DISTRIBUTION (city)
# fig10 = px.histogram(df_city_m, x='WindSpeed', nbins=100, title='Wind intenstiy distribution in Munich city')
# fig10.update_layout(bargap = 0.05)
# fig10.update_xaxes(range=[0,20])
# shape, loc, scale = stats.weibull_min.fit(df_city_m['WindSpeed'])     # Weibull distribution fit
# x_line = np.linspace(np.min(df_city_m['WindSpeed']), np.max(df_city_m['WindSpeed']), 100)
# y_line = stats.weibull_min.pdf(x_line, shape, loc, scale) * 40450
# df_line = pd.DataFrame({"x": x_line, "y": y_line})
# fig10.add_scatter(x=df_line["x"], y=df_line["y"], mode="lines", name="Weibull Distribution")
# fig10.write_html(os.path.join(output_folder,"10_Histogram_city.html"))
# fig10.write_image(os.path.join(output_folder,"10_Histogram_city.png"))
# fig10.write_image(os.path.join(output_folder,"10_Histogram_city.svg"))

# # WIND GUST DISTRIBUTION (airport)
# fig11 = px.histogram(df_airp_g, x='MaxSpeed', nbins=200, title='Gust intenstiy distribution in Munich airport')
# fig11.update_layout(bargap = 0.05)
# fig11.update_xaxes(range=[0,20])
# fig11.write_html(os.path.join(output_folder,"11_Histogram_gust_airp.html"))
# fig11.write_image(os.path.join(output_folder,"11_Histogram_gust_airp.png"))
# fig11.write_image(os.path.join(output_folder,"11_Histogram_gust_airp.svg"))

# # WIND GUST DISTRIBUTION (city)
# fig12 = px.histogram(df_city_g, x='MaxSpeed', nbins=200, title='Gust intensity distribution in Munich city')
# fig12.update_layout(bargap = 0.05)
# fig12.update_xaxes(range=[0,20])
# fig12.write_html(os.path.join(output_folder,"12_Histogram_gust_city.html"))
# fig12.write_image(os.path.join(output_folder,"12_Histogram_gust_city.png"))
# fig12.write_image(os.path.join(output_folder,"12_Histogram_gust_city.svg"))

print("\nEnding plotting data")