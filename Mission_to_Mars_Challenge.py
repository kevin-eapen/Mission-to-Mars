#!/usr/bin/env python
# coding: utf-8

# In[33]:


# Import Splinter and BeautifulSoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[4]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[22]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div,list_text', wait_time=1)


# ### News

# In[23]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[24]:


slide_elem.find('div', class_='content_title')


# In[25]:


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[26]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[28]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[29]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[30]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[31]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[32]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[34]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[35]:


df.to_html()


# In[36]:


browser.quit()


# In[ ]:





# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[3]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[95]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.


# Create for loop to iterate through each full image elem... we want to click on every other html link found so will iterate
# over a range from 1-7, incrementing by 2 in order to click each of the 4 full image elem links.
for i in range(1, 8, 2):
    # Initialize empy dictionary valuable to add 'image link: title' key-value pair from scraping results.
    hemispheres = {}
    
    # Search for the full image elem link by partial href value and click on the element.
    full_image_elem = browser.links.find_by_partial_href('.html')
    full_image_elem[i].click()
    
    # Parse the html from the web page.
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Search for the 'a' tag containg the href full image link within the right div container,
    # and scrape scrape the href value (the relative url). Then concatenate the relative url with the main url. 
    img_url_rel = img_soup.find('div', class_='downloads').find('a').get('href')
    img_url = f'{url}{img_url_rel}'
    
    # Search for the image title in the 'h2' header tag with the 'title' class.
    title = img_soup.find('h2', class_='title').get_text()
    
    # Add full image url and title key-value pairs to hemispheres dictionary.
    # Then append the hemispheres dictionary to the hemisphere image urls list.
    hemispheres.update({'img_url': img_url, 'title': title})
    hemisphere_image_urls.append(hemispheres)
    
    # Use the browser to click 'back' to allow next loop iteration to click on the next full image elem link.
    browser.back()


# In[96]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[97]:


# 5. Quit the browser
browser.quit()


# In[ ]:




