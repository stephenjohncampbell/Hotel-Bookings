#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import os


# In[ ]:





# In[8]:


os.chdir('C:/Users/steph/OneDrive/Other/Documents')
os.getcwd()


# In[ ]:


#read in data


# In[18]:


hotel_bookings = pd.read_csv('hotel_bookings.csv')
hotel_data_dictionary = pd.read_csv('hotel_data_dictionary.csv')
hotel_bookings = pd.DataFrame(hotel_bookings)


# In[13]:


#look at the data


# In[14]:


hotel_bookings.head()


# In[23]:


#look for missing values
df = hotel_bookings.copy()
df.isnull().sum().sort_values(ascending=False)[:10]

#look at the children
hotel_bookings['children'].head()


# In[27]:


#assume that the missing vaules for children are meant to be 0 the other missing values make sense

hotel_bookings['children'] = hotel_bookings['children'].fillna(0)
hotel_bookings['children'].unique()


# In[ ]:


#average number of adults 


# In[31]:


#look at canceled bookings

#total number of bookings
totalnumber = hotel_bookings['is_canceled'].count()
#total number of canceled bookings
canceled = hotel_bookings['is_canceled'].sum()


# In[56]:


#percenage canceled
percentage_canceled = (canceled / totalnumber)
not_canceled_percentage = (1 - percentage_canceled)
percentage_canceled = percentage_canceled*100
not_canceled_percentage = not_canceled_percentage*100


# In[70]:


# make a chart
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
names = ['Not canceled', 'Canceled']
data = [not_canceled_percentage,percentage_canceled]
ax.bar(names, data)
ax.set_ylabel('Booking percent %')
ax.set_title('percentage of canceled bookings')
plt.show()


# In[72]:


#has the number of canceled booking changed the year

year2015percentcanceled = ((hotel_bookings[hotel_bookings['arrival_date_year']== 2015]['is_canceled'].sum())/ (hotel_bookings[hotel_bookings['arrival_date_year']== 2015]['is_canceled'].count()))*100
year2016percentcanceled = ((hotel_bookings[hotel_bookings['arrival_date_year']== 2016]['is_canceled'].sum())/ (hotel_bookings[hotel_bookings['arrival_date_year']== 2016]['is_canceled'].count()))*100
year2017percentcanceled = ((hotel_bookings[hotel_bookings['arrival_date_year']== 2017]['is_canceled'].sum())/ (hotel_bookings[hotel_bookings['arrival_date_year']== 2017]['is_canceled'].count()))*100


# In[73]:


# make a chart
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
names = ['2015', '2016', '2017']
data = [year2015percentcanceled, year2016percentcanceled, year2017percentcanceled]
ax.bar(names, data)
ax.set_ylabel('Booking percent %')
ax.set_title('percentage of canceled bookings by year')
plt.show()


# In[81]:


#seasonality in the data 

new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
             'October', 'November', 'December']

sorted_months = hotel_bookings['arrival_date_month'].value_counts().reindex(new_order)

x = sorted_months.index
y = sorted_months/sorted_months.count()


# In[157]:


#what leads to cancelions
list(hotel_bookings)
hotel_bookings_can = hotel_bookings[['is_canceled' ,  'lead_time', 'is_repeated_guest', 'previous_cancellations', 'deposit_type']]

print(hotel_bookings_can['deposit_type'].unique())
hotel_bookings_can['No_Deposit'] = hotel_bookings_can['deposit_type'] == 'No Deposit'
hotel_bookings_can['Refundable'] = hotel_bookings_can['deposit_type'] == 'Refundable'
hotel_bookings_can['Non_Refund'] = hotel_bookings_can['deposit_type'] == 'Non Refund'
hotel_bookings_can.head()


# In[162]:


#regression
fit = sm.OLS.from_formula('is_canceled ~  + lead_time + is_repeated_guest + previous_cancellations + Refundable + Non_Refund', hotel_bookings_can).fit()
print(fit.summary())


# In[109]:


y = pd.DataFrame(y)
y[	arrival_date_month]


# In[121]:



month = x
number_of_bookings_by_month = y['arrival_date_month']
plt.figure(figsize=(12,4))  
plt.plot(month, number_of_bookings_by_month)
plt.title('Number of bookings by month')
plt.xlabel('Month')
plt.ylabel('Number of bookings')
plt.show()


# In[133]:


sorted_months2015 = hotel_bookings[hotel_bookings['arrival_date_year']== 2015]['arrival_date_month'].value_counts().reindex(new_order)
sorted_months2016 = hotel_bookings[hotel_bookings['arrival_date_year']== 2016]['arrival_date_month'].value_counts().reindex(new_order)
sorted_months2017 = hotel_bookings[hotel_bookings['arrival_date_year']== 2017]['arrival_date_month'].value_counts().reindex(new_order)


# In[143]:


month = x
plt.figure(figsize=(12,4))  
plt.plot(month, sorted_months2015, label = '2015')
plt.plot(month, sorted_months2016, label = '2016')
plt.plot(month, sorted_months2017, label = '2017')
plt.title('Number of bookings by month')
plt.xlabel('Month')
plt.ylabel('Number of bookings')
plt.legend()
plt.show()


# In[129]:


hotel_bookings[hotel_bookings['arrival_date_year']== 2017]['arrival_date_month']


# In[ ]:




