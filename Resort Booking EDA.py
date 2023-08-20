#!/usr/bin/env python
# coding: utf-8

# # Libraries Required to be imported

# In[89]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Importing the CSV Data Set

# In[90]:


hotel = pd.read_csv("C:/Users/Sumit Kumar/Desktop/PLACEMENT/PROJECTS/Resort Booking/hotel_booking.csv")


# # EDA and Data Cleaning

# In[91]:


# Returns first 10 rows
hotel.head(10)


# In[92]:


# Returns last 10 rows
hotel.tail(10)


# In[93]:


#Brief description of all the numerical type columns
hotel.describe()


# In[94]:


hotel.columns


# In[95]:


hotel.info()


# In[96]:


hotel.shape


# In[97]:


#Changing the reservation_status_date from object to date_time
hotel['reservation_status_date'] = pd.to_datetime(hotel['reservation_status_date'])


# In[98]:


# Confirming the data type change of 'reservation_status_date'
hotel.dtypes


# In[99]:


# Brief description of all the 'object' type columns
hotel.describe(include = 'object')


# In[100]:


# Printing all the unique values of each column
for col in hotel.describe(include = 'object').columns:
        print(col)
        print(hotel[col].unique())
        print("----------"*10)
    


# In[101]:


# Checking the missing values
hotel.isnull().sum()


# In[102]:


# Dropping the columns with relatively high number of missing values
hotel.drop(['company','agent'],axis = 1,inplace = True )


# In[103]:


# Removing the null values rows from the dataset
hotel.dropna(inplace = True)


# In[104]:


hotel.isnull().sum()


# In[105]:


hotel.describe(include='all')
# No of rows decreased from 119390 to 118898 as the null values rows were dropped.


# In[106]:


# Checking the outliers and removing them
hotel['adr'].plot(kind = 'box')


# In[107]:


# Dropping Outliers from 'adr' column
hotel = hotel[hotel.adr < 1000]


# In[108]:


hotel.describe()


# In[109]:


# Checking Outliers in 'stays_in_weekend_nights'
hotel['stays_in_weekend_nights'].plot(kind = 'box')


# In[110]:


# Removing the outliers in 'stays_in_weekend_nights'
hotel = hotel[hotel['stays_in_weekend_nights'] < 6]


# In[111]:


hotel['days_in_waiting_list'].plot(kind = 'box')


# In[112]:


hotel = hotel[hotel['days_in_waiting_list'] < 240]


# In[113]:


hotel['stays_in_week_nights'].plot(kind = 'box')


# In[114]:


hotel = hotel[hotel['stays_in_week_nights'] < 6]


# # Data Analysis and Visualisation

#  In 'is_cancelled' column,
# 1 -----> IS CANCELLED,
# 0 -----> IS NOT CANCELLED 

# In[115]:


# Calculating cancellation percentage 
cancellation_percentage = hotel['is_canceled'].value_counts(normalize = True)
cancellation_percentage


# In[117]:


# Plotting Cancelled Vs Non Cancelled
plt.figure(figsize = (5,5))
plt.title('Reservation Status')
plt.bar(['Not Cancelled','Cancelled'],hotel['is_canceled'].value_counts(),edgecolor='black',width=0.6)
plt.show()


# In[118]:


# Plotting cancelled and non cancelled booking in Resort hotel and City hotel
plt.figure(figsize = (6,4))
ax1 = sns.countplot(x ='hotel',hue = 'is_canceled',data = hotel,palette = 'cubehelix')
legend_labels,_ = ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation in different hotels',size = 20)
plt.xlabel('HOTEL')
plt.ylabel('Number of Reservation')
plt.legend(['not canceled','canceled'])


# In[119]:


# Cancellation % in City Hotel
city_hotel = hotel[hotel['hotel']=='City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[120]:


# Cancellation % in resort hotel
resort_hotel = hotel[hotel['hotel']=='Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)


# In[121]:


# Grouping by city and resort hotel based on booking days
resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[122]:


#Comparing average daily rate in City Hotel and Resort Hotel
plt.figure(figsize = (20,6))
plt.title('Average Daily Rate in City and Resort Hotel',fontsize = 30)
plt.plot(resort_hotel.index,resort_hotel['adr'],label = 'RESORT HOTEL')
plt.plot(city_hotel.index,city_hotel['adr'],label = 'CITY HOTEL')
plt.legend(fontsize = 20)
plt.show()


# In[123]:


# Reservation status of both the hotels month wise
hotel['month']= hotel['reservation_status_date'].dt.month
plt.figure(figsize = (16,6))
ax1 = sns.countplot(x='month',hue='is_canceled',data = hotel,palette='viridis')
legend_labels,_=ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('RESERVATION STATUS PER MONTH',size= 20)
plt.xlabel('MONTH')
plt.ylabel('NUMBER OF RESERVATIONS')
plt.legend(['Not Cancelled','Cancelled'])
plt.show()


# In[125]:


# Top 10 countries with highest cancellation rate
Cancelled_Data=hotel[hotel['is_canceled']==1]
TOP_10_COUNTRIES = Cancelled_Data['country'].value_counts()[:10]
plt.figure(figsize = (8,8))
plt.title('Highest Reservation Cancellation countries')
plt.pie(TOP_10_COUNTRIES,autopct = '%0.2f',labels=TOP_10_COUNTRIES.index)
plt.show()


# In[126]:


# Hotel booking sources
hotel['market_segment'].value_counts()


# In[127]:


hotel['market_segment'].value_counts(normalize=True)


# In[128]:


# Which booking sources has more cancellation
Cancelled_Data['market_segment'].value_counts(normalize=True)


# In[129]:


plt.figure(figsize = (10,4))
plt.title('Cancelled Booking')
plt.bar(['Online TA','Groups','Offline TA','Direct','Corporate','Complementary','Aviation'],Cancelled_Data['market_segment'].value_counts(normalize=True),edgecolor='black',width=0.6)
plt.xlabel('BOOKING SOURCE')
plt.ylabel('CANCELLATION RATIO')
plt.show()


# In[130]:


#Lets examine whether days in waiting list is impacting cancellation or not?
Cancelled_Data['days_in_waiting_list'].value_counts(normalize=True)


# In[131]:


#Examinig which type of customers mostly cancel their booking
Cancelled_Data['customer_type'].value_counts(normalize=True)


# In[132]:


hotel['customer_type'].value_counts(normalize=True)
plt.figure(figsize = (16,4))
ax1 = sns.countplot(x='customer_type',hue='is_canceled',data = hotel,palette='coolwarm')
legend_labels,_=ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('CANCELLATION AS PER CUSTOMER TYPE',size= 20)
plt.xlabel('CUSTOMER TYPE')
plt.ylabel('NUMBER OF CANCELLATION')
plt.legend(['Not Cancelled','Cancelled'])
plt.show()


# In[133]:


#Analyzing whether Diposite type has any impact on room cancellation or not?
Cancelled_Data['deposit_type'].value_counts(normalize=True)


# In[134]:


#Checking whether room is assigned as per the choice or not?
hotel['room_assigned_as_per_reserved'] = hotel['reserved_room_type'] == hotel['assigned_room_type']
hotel['room_assigned_as_per_reserved'].value_counts(normalize=True)


# In[135]:


#Creating a column named 'room_assigned_as_per_reserved' category.
hotel['room_assigned_as_per_reserved']=hotel['room_assigned_as_per_reserved']


# In[136]:


hotel['room_assigned_as_per_reserved']


# In[137]:


Cancelled_Data=hotel[hotel['is_canceled']==1]


# In[138]:


#Impact of 'room_assigned_as_per_reserved' category on cancellation.
Cancelled_Data['room_assigned_as_per_reserved'].value_counts(normalize=True)


# In[139]:


plt.figure(figsize = (16,4))
ax1 = sns.countplot(x='room_assigned_as_per_reserved',hue='is_canceled',data = hotel,palette='plasma')
legend_labels,_=ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Cancellation Based on Reserved and alloted Room being same or not',size= 20)
plt.xlabel('Room assigned as Reserved')
plt.ylabel('Customer number')
plt.legend(['Not Cancelled','Cancelled'])
plt.show()


# In[96]:


#Exporting data in csv format for further analysis.
hotel.to_csv("C:/Users/Sumit Kumar/Desktop/PLACEMENT/PROJECTS/Resort Booking/hotel_booking_for_POWERBI.csv")


# In[ ]:




