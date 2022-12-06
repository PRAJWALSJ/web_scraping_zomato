#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import time

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# In[2]:


start = time.time()


# In[3]:


#not required if you are using web driver
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}


# In[4]:


#web driver path. varies for each user
driver = webdriver.Chrome(executable_path=r"/Users/prajwalsj/Downloads/chromedriver")


# In[5]:


#link of the location which the data has to be extracted
driver.get("https://www.zomato.com/bhubaneswar/delivery-in-patia?delivery_subzone=13053&place_name=Patia%2C+Bhubaneswar%2C++India")


# In[6]:


time.sleep(2)  # Allow 2 seconds for the web page to (open depends on you)
scroll_pause_time = 10  # You can set your own pause time. dont slow too slow that might not able to load more data.
#need to experiment with the value of scroll_pause_time and see which works better as it depends on multiple factors like internet speed, traffic etc
screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break


# In[9]:


product_links = []


# In[10]:


soup = BeautifulSoup(driver.page_source, 'lxml')
product_list = soup.find_all('div', class_='jumbo-tracker')
    #print(product_list)
    
for item in product_list:
    for link in item.find_all('a', href=True):
        product_links.append(link['href'])

print(product_links)
print(len(product_links))


# In[11]:


url = 'https://www.zomato.com'
new_links2 = [url + x for x in product_links]
print(len(new_links2))


# In[12]:


new_links = list( dict.fromkeys(new_links2) )
print(len(new_links))


# In[13]:


name_list = []
contact_list = []
address_list = []
fssai_list = []
#menu_container = []
menu_list = []
#restaurents_list = []


# In[14]:


for link in new_links:
    try:
        test_url_overview = link.replace('order', '')
        r = requests.get(test_url_overview, headers = headers)
        soup3 = BeautifulSoup(r.content, 'lxml')
        name = soup3.find('h1', class_="sc-7kepeu-0 sc-kZmsYB dggtcP").text
        name_list.append(name)
        #print(name)
        contact = soup3.find('p', class_="sc-1hez2tp-0 fanwIZ").text
        contact_list.append(contact)
        #print(contact)
        r = requests.get(test_url_overview, headers = headers)
        soup3 = BeautifulSoup(r.content, 'lxml')
        address = soup3.find('p', class_="sc-1hez2tp-0 clKRrC").text
        address_list.append(address)
        r = requests.get(link, headers = headers)
        soup2 = BeautifulSoup(r.content, 'lxml')
        #fssai
        soup4 = BeautifulSoup(r.content, 'lxml').text
        start = soup4.find('No. ') + 4
        end = soup4.find('Rel', start)
        fssai = soup4[start:end]
        fssai_list.append(fssai)
        
        #fssaiend
        menu_container = list()
        menu = soup2.find_all('h4', class_="sc-1s0saks-15 iSmBPS")
        for value in menu:
            menu_text = value.text
            menu_container.append(menu_text)
        menu_list.append(menu_container)
        
        
    except:
        pass
    
df = pd.DataFrame({'name_list': name_list,'contact_list': contact_list,'address_list': address_list,'fssai_list': fssai_list, 'menu_list': menu_list})


# In[15]:


df


# In[16]:


df.to_csv('zomato_restaurents_patia.csv')


# In[ ]:




