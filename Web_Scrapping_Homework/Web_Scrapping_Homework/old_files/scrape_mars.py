# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

# URL of page to be scraped
#url = 'https://mars.nasa.gov/news/'


# Initialize browser
def init_browser(): 
        executable_path = {"executable_path":"chromedriver"}
        return Browser('chrome', headless=True, **exec_path) 


# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()
    
    # create mars_data dict that we can insert into mongo    
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        time.sleep(5)


 # Example visit unsplash.com
        #unsplash = "https://unsplash.com/search/photos/surfing"
        #browser.visit(unsplash)
        #browser.is_element_present_by_id("gridMulti", 1)
        #html = browser.html


 # Visit Mars Nasa News
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        time.sleep(5)
        html = browser.html
        

# Retrieve page with the requests module
#response = requests.get(url)


# Create BeautifulSoup object; parse with 'html.parser'
## Step 1 - Scraping
#soup = BeautifulSoup(response.content, 'html.parser')


# Example create a soup object from the html
    #img_soup = BeautifulSoup(html, "html.parser")
    #elem = img_soup.find(id="gridMulti")
    #img_src = elem.find("img")["src"]

# Create a soup object from the html
        soup = BeautifulSoup(html, 'html.parser')



# Retrieve the latest element that contains news title and news_paragraph
        title = soup.find('div', class_='content_title').find('a').text
        
        mars_info['title'] = title
                       
        return mars_info

        browser.quit()


# Examine the results, then determine element that contains sought info
#print(soup.prettify())


#title = soup.find ('div', class_="content_title").text
#paragraph = soup.find('div', class_='article_teaser_body').text

#print(title)


#JPL Mars Space Images - Featured Image
#Visit the url for JPL Featured Space Image
#image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#browser.visit(image_url_featured)

def scrape_mars_image():

    try: 

        browser = init_browser()

        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)
        time.sleep(5)

# Retrieve page with the requests module
#response = requests.get(url)

#Use splinter to navigate the site and find the image url for the current Featured Mars Image

# HTML Object 
        html_image = browser.html

# Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

# Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

# Website Url 
        main_url = 'https://www.jpl.nasa.gov'
        time.sleep(5)

# Concatenate website url with scrapped route
        featured_image_url = main_url + featured_image_url

# Display full link to featured image
        featured_image_url
        mars_info['featured_image_url'] = featured_image_url 


        return mars_info
    finally:

        browser.quit()


### Mars Weather
# Visit the Mars Weather twitter account
#weather_url = 'https://twitter.com/marswxreport?lang=en'
#browser.visit(weather_url)

def scrape_mars_weather():

    try: 

        
        browser = init_browser()
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url) 
        time.sleep(5)
        html_weather = browser.html
        soup = BeautifulSoup(html_weather, 'html.parser')
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')


        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass


        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info
    finally:

        browser.quit()

# HTML Object 
#html_weather = browser.html

# Parse HTML with Beautiful Soup
#soup = BeautifulSoup(html_weather, 'html.parser')

# Find all elements that contain tweets
#latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

# Retrieve all elements that contain news title in the specified range
# Look for entries that display weather related words to exclude non weather related tweets 
#for tweet in latest_tweets: 
    #weather_tweet = tweet.find('p').text
    #if 'Sol' and 'pressure' in weather_tweet:
        #print(weather_tweet)
        #break
    #else: 
        #pass

### Mars Facts

# Visit the Mars Facts webpage
#Use Pandas to convert the data to a HTML table string.

        marsfacts_url = 'http://space-facts.com/mars/'
        mars_facts = pd.read_html(facts_url)
        mars_df = mars_facts[0]
        mars_df.columns = ['Description','Value']
        mars_df.set_index('Description', inplace=True)
        mars_df.to_html()
#data = mars_df.to_dict(orient='records')  # Here's our added param..

        mars_info['mars_facts'] = data

        return mars_info


# Display mars_df
#mars_df


### Mars Hemispheres

#Visit the USGS Astrogeology site

#astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#browser.visit(astrogeology_url)


        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        time.sleep(5)

#Find the image url to the full resolution image
#Append the dictionary with the image url string and the hemisphere title to a list

        html_hemispheres = browser.html


        soup = BeautifulSoup(html_hemispheres, 'html.parser')


        items = soup.find_all('div', class_='item')

        hiu = []

#hemisphere_image_urls = 


        hemispheres_main_url = 'https://astrogeology.usgs.gov'


    for i in items: 
    
        title = i.find('h3').text
    
    
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    
        browser.visit(hemispheres_main_url + partial_img_url)
    
    
        partial_img_html = browser.html
    
    
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
     
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        hiu.append({"title" : title, "img_url" : img_url})
    
    #hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    mars_info['hiu'] = hiu      

        return mars_info
    finally:

        browser.quit()








