# -*- coding: utf-8 -*-
"""
Created on Sun May  3 03:15:55 2026

@author: user
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#STEP 1: Plot the pollution heatmap
#1: Load the file
df = pd.read_csv('C:/Users/user/Downloads/Anu/CRM/AQI_EDA/archive (2)/data_date.csv')

df['Date'] =  pd.to_datetime(df['Date'])

df['Day_of_Week'] = df['Date'].dt.day_name()
df['Month'] = df['Date'].dt.month_name()
df['Year'] = df['Date'].dt.year

#We organize data into a grid: Months on the side, Days on the top
seasonal_pivot =  df.pivot_table(values = 'AQI Value', index = 'Month', columns = 'Day_of_Week', aggfunc = 'mean')

#Re order so the calendar flows naturally(Jan-Dec, Mon-Sun)
months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

seasonal_pivot = seasonal_pivot.reindex(index =  months_order, columns =  days_order)

plt.figure(figsize = (12,10))
sns.heatmap(seasonal_pivot, cmap = 'YlOrRd', annot = True, fmt = ".1f")

plt.title('Seasonal Pollution Heatmap: Average AQI by Month & Day')
plt.savefig('plots/seasonal_pollution_heatmap.png', bbox_inches='tight')
plt.close()
plt.show()

#STEP 2: The top 10 most polluted countries chart
#1. Calculate the average AQI for each country
#We group by country and take the mean of the AQI Value
country_avg = df.groupby('Country') ['AQI Value'].mean().sort_values(ascending = False)

#2. Select the Top 10
top_10_countries =  country_avg.head(10)

#3. Plotting
plt.figure(figsize = (10,8))
sns.barplot(x = top_10_countries.values, y = top_10_countries.index, palette = 'Reds_r')

#4. Adding information
plt.title('Top 10 Countries with Highest Average Pollution(AQI)')
plt.xlabel('Average AQI Value')
plt.ylabel('Country')
plt.savefig('plots/top_10_countries.png', bbox_inches='tight')
plt.close()
plt.show()

#STEP 3: The time-series trend. Are the AQI values getting better or worse?
#1. Group the data by Date abd calculate the global average for each day
global_trend = df.groupby('Date') ['AQI Value'].mean()

#2. Plotting the Line Chart
plt.figure(figsize = (12,6))
plt.plot(global_trend.index, global_trend.values, color = 'darkgreen', linewidth = 2)

#3. Customizing the look
plt.title('Global Air Quality Trend(2022-2026)')
plt.xlabel('Date')
plt.ylabel('Average AQI Value')
plt.grid(True, linestyle = '--', alpha = 0.7) #Adds a subtitle grid for easier reading
plt.savefig('plots/global_AQ_trend.png', bbox_inches='tight')
plt.close()
plt.show()