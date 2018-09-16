
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[67]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[70]:


#find unique player id's
total_players = purchase_data['SN'].drop_duplicates().count()
total = pd.DataFrame({'Total_Players':[total_players]})
total


# In[2]:





# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[4]:


unique_item_count = purchase_data['Item ID'].drop_duplicates().count()
unique_item_count

avg_price = float("{0:.2f}".format(purchase_data['Price'].mean()))
avg_price

num_purchase = purchase_data['Purchase ID'].drop_duplicates().count()
num_purchase

total_rev = purchase_data['Price'].sum()
total_rev

pd.DataFrame({'Unique Items': [unique_item_count], 'Average Price': [avg_price], 'Number of Purchases': [num_purchase], 'Total Revenue': [total_rev]})


# In[3]:





# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[5]:


gender_df = purchase_data.drop_duplicates(subset='SN')

gender = pd.DataFrame(gender_df['Gender'].value_counts())
prop = gender.loc[:,'Gender']/total_players
gender['Proportion'] = prop * 100
gender


# In[4]:





# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[37]:


#renaming gender_df to be grouped by gender
#gender = purchase_data.groupby('Gender').nunique()
gender_df = purchase_data.groupby('Gender')

#Purchase count
purchase_ct_g = gender_df.Gender.count()

#Average Purcahse Price
avg_price_g = round(gender_df['Price'].sum() / purchase_ct, 2)

#Total Purchase Value
total_val_g = round(gender_df['Price'].sum(), 2)

#Average Total purchase per person
avg_val_g = round(total_val_g / gender['SN'] ,2)

#Summary by Gender
pd.DataFrame({'Purchase Count':purchase_ct_g, 'Average Purchase Price':avg_price_g, 
              'Total Purchase Value' :total_val_g, 'Avg Total per Person' :avg_val_g})


# In[5]:





# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[75]:


bins = [0,9,14,19,24,29,34,39,150]
lbls = ['<10','10-14','15-19','20-24','25-29','30-34','35-39','40+']

result_bin = pd.cut(purchase_data.drop_duplicates(subset='SN').Age, bins, labels=lbls)
#store results into data frame
bin_df = pd.DataFrame(result_bin).Age.value_counts()
bin_df = pd.DataFrame(bin_df)
bin_df['Percentage of Players'] = round(100 * (bin_df.Age / total_players), 2)
bin_df


# In[6]:





# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[116]:


#add bins col and groupby bin
bined_purchase_data = purchase_data
bined_purchase_data['Bin Label'] = pd.cut(purchase_data.Age, bins, labels = lbls)
bin_grouped_df = bined_purchase_data.groupby('Bin Label')

#purchase count
count_bin = bin_grouped_df['Age'].count()

#average price
price = round(bin_grouped_df['Price'].sum() / count_bin, 2)
pd.DataFrame(price)

#total purchase price
total_val = round(bin_grouped_df['Price'].sum(), 2)

#average per person
avg_purchase = round(total_val / pd.cut(purchase_data.drop_duplicates(subset='SN').Age, bins, labels=lbls).value_counts() ,2)

bin_df = pd.DataFrame({'Purchase Count': count_bin, 'Avg Purchase Price': price, 'Total Purchase Value': total_val, 'Average per Person': avg_purchase})
bin_df


# In[7]:





# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[159]:


#group by SN
sn_grouped = purchase_data.groupby(['SN'])
purchase_ct = sn_grouped['Purchase ID'].count()
avg_price_s = round(sn_grouped['Price'].mean(), 2)
total_val_s = sn_grouped['Price'].sum()
sum_sn_df = pd.DataFrame({'Purchase Count': purchase_ct, 'Average Purchase Price' :avg_price_s,
                         'Total Purchase Value' :total_val_s})
result = sum_sn_df.sort_values('Purchase Count', ascending=False)
result.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[180]:


items_grouped = purchase_data.groupby(['Item ID', 'Item Name'])

#purchase count 
purchase_ct = items_grouped['Item ID'].count()
#Item Price
item_price = items_grouped['Price'].mean()
item_price.head()
total_val = purchase_ct * item_price
#build the data frame of summary
sum_item = pd.DataFrame({'Purchase Count': purchase_ct, 'Item Price' :item_price, 
                         'Total Purchase Value' :total_val})
sum_item.sort_values('Purchase Count', ascending=False).head()


# In[9]:





# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[181]:


sum_item.sort_values('Total Purchase Value', ascending=False).head()


# In[10]:




