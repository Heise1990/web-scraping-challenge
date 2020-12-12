from bs4 import BeautifulSoup
from requests import get
from splinter import Browser
import pandas as pd
import re

def scrape():
    # Setup splinter------------------------------------
    executable_path = {'executable_path' : '/Users/jordanheise/.wdm/drivers/chromedriver/mac64/87.0.4280.88/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = False)
    
    ### Mars News
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    newsURL = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    scrape_results = {}
    # Load page into browser
    browser.visit(newsURL)
    # Find tag for first news headline
    if browser.is_element_present_by_css('div[class="list_text"]', wait_time=5):
        firstSlide = browser.find_by_css('div[class="list_text"]')[0]
        # Find Title and paragraph of headline
        news_title = firstSlide.find_by_css('div[class="content_title"]').text
        news_p = firstSlide.find_by_css('div[class="article_teaser_body"]').text
        scrape_results.update({'news_title':news_title})
        scrape_results.update({'news_p':news_p})
    else:
        print('Page timed out:' + newsURL)
        
    #####JPL Mars Space Images - Featured Image#####
    # Retrieve featured image link
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, "html.parser")

    # Retrieve background-image url from style tag 
    image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = "https://www.jpl.nasa.gov"

    # Concatenate website url with scrapped route
    image_url = main_url + image_url

    # Display full link to featured image
    image_url
    scrape_results.update({'image_url':image_url})
    
        ## Mars Facts
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    
    facts_df = pd.read_html(mars_facts_url)[0]
    facts_df = facts_df.rename(columns = {0:'unit', 1:'value'})
    
    equatorial_diam = facts_df[facts_df['unit'] == 'Equatorial Diameter:']['value'].values[0]
    polar_diam = facts_df[facts_df['unit'] == 'Polar Diameter:']['value'].values[0]
    mass = facts_df[facts_df['unit'] == 'Mass:']['value'].values[0]
    moons = facts_df[facts_df['unit'] == 'Moons:']['value'].values[0]
    orbit_distance = facts_df[facts_df['unit'] == 'Orbit Distance:']['value'].values[0]
    orbit_period = facts_df[facts_df['unit'] == 'Orbit Period:']['value'].values[0]
    surface_temp = facts_df[facts_df['unit'] == 'Surface Temperature:']['value'].values[0]
    first_record = facts_df[facts_df['unit'] == 'First Record:']['value'].values[0]
    recorded_by = facts_df[facts_df['unit'] == 'Recorded By:']['value'].values[0]
    
    scrape_results = ({
        'equatorial_diam':equatorial_diam,
        'polar_diam':polar_diam,
        'mass':mass,
        'moons':moons,
        'orbit_distance':orbit_distance,
        'orbit_period':orbit_period,
        'surface_temp':surface_temp,
        'first_record':first_record,
        'recorded_by':recorded_by,
        })
    
    # Use Pandas to convert the data to a HTML table string.
    html_table = facts_df
    html_table = html_table.to_html()
    scrape_results.update({'mars_facts_html_table':html_table})    
    
    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
    # Display hemisphere_image_urls
    hemisphere_image_urls
    scrape_results.update({'mars_hem_img_urls':hemisphere_image_urls})
        