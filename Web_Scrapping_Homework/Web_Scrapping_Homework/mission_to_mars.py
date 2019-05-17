#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

# In[2]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'


# In[3]:

def init_browser():
    #Pointing to the directory where chromedriver exists
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)


# In[4]:

def scrape():
# Retrieve page with the requests module
    browser = init_browser()
    response = requests.get(url)


    # In[5]:
    #put all values into dictionary
    mars_data_dict = {}

    # Create BeautifulSoup object; parse with 'html.parser'
    ## Step 1 - Scraping
    soup = BeautifulSoup(response.content, 'html.parser')


    # In[6]:


    # Examine the results, then determine element that contains sought info
    print(soup.prettify())


    # In[7]:


    ### NASA Mars News


    # In[8]:


    title = soup.find ('div', class_="content_title").text
    #paragraph = soup.find('div', class_='article_teaser_body').text

    #print(title)
    mars_data_dict['title'] = title


    # In[9]:


    #JPL Mars Space Images - Featured Image
    #Visit the url for JPL Featured Space Image
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)
    time.sleep(5)
    


    # In[10]:


    # Retrieve page with the requests module
    response = requests.get(url)


    # In[11]:


    #Use splinter to navigate the site and find the image url for the current Featured Mars Image

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Display full link to featured image
    featured_image_url

    mars_data_dict['img_url'] = featured_image_url
    # In[12]:


    ### Mars Weather
    # Visit the Mars Weather twitter account
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(5)

    # In[13]:


    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            #print(weather_tweet)
            mars_data_dict['weather'] = weather_tweet
            break
        else: 
            pass


    # In[14]:


    ### Mars Facts


    # In[17]:


    # Visit the Mars Facts webpage
    #Use Pandas to convert the data to a HTML table string.

    marsfacts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(marsfacts_url)
    mars_df = mars_facts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    mars_html = mars_df.to_html(header=False)
    data = mars_df.to_dict(orient='records')  # Here's our added param..

    # Display mars_df
    #mars_df
    mars_data_dict['mars_fact_table'] = mars_html

    # In[18]:


    mars_html


    # In[19]:


    ### Mars Hemispheres


    # In[20]:


    #Visit the USGS Astrogeology site

    astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrogeology_url)
    time.sleep(5)

    # In[21]:


    #Find the image url to the full resolution image
    #Append the dictionary with the image url string and the hemisphere title to a list

    html_hemispheres = browser.html


    soup = BeautifulSoup(html_hemispheres, 'html.parser')


    items = soup.find_all('div', class_='item')


    hemisphere_image_urls = []


    hemispheres_main_url = 'https://astrogeology.usgs.gov'


    for i in items: 
        
        title = i.find('h3').text
        
        
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        
        browser.visit(hemispheres_main_url + partial_img_url)
        
        
        partial_img_html = browser.html
        
        
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        


    
    mars_data_dict['hemisphere_pic_url'] = hemisphere_image_urls

    return mars_data_dict


    # In[ ]:




