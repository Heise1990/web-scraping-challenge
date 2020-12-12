{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 75,
   "metadata": {},
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup\n",
    "from requests import get\n",
    "from splinter import Browser\n",
    "import pandas as pd\n",
    "from webdriver_manager.chrome import ChromeDriverManager"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 76,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[WDM] - Current google-chrome version is 87.0.4280\n",
      "[WDM] - Get LATEST driver version for 87.0.4280\n",
      "[WDM] - Driver [/Users/jordanheise/.wdm/drivers/chromedriver/mac64/87.0.4280.88/chromedriver] found in cache\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " \n"
     ]
    }
   ],
   "source": [
    "# Setup splinter\n",
    "executable_path = {'executable_path' : ChromeDriverManager().install()}\n",
    "browser = Browser('chrome', **executable_path, headless = False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 77,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "5 Hidden Gems Are Riding Aboard NASA's Perseverance Rover\n",
      "The symbols, mottos, and small objects added to the agency's newest Mars rover serve a variety of purposes, from functional to decorative.\n"
     ]
    }
   ],
   "source": [
    "### Mars News\n",
    "# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.\n",
    "newsURL = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'\n",
    "\n",
    "# Load page into browser\n",
    "browser.visit(newsURL)\n",
    "# Find tag for first news headline\n",
    "if browser.is_element_present_by_css('div[class=\"list_text\"]', wait_time=5):\n",
    "    firstSlide = browser.find_by_css('div[class=\"list_text\"]')[0]\n",
    "    # Find Title and paragraph of headline\n",
    "    news_title = firstSlide.find_by_css('div[class=\"content_title\"]').text\n",
    "    news_p = firstSlide.find_by_css('div[class=\"article_teaser_body\"]').text\n",
    "else:\n",
    "    print('Page timed out:' + newsURL)\n",
    "print(news_title)\n",
    "print(news_p)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 78,
   "metadata": {},
   "outputs": [],
   "source": [
    "#####JPL Mars Space Images - Featured Image#####"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 79,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Retrieve featured image link\n",
    "featured_image_url = \"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars\"\n",
    "browser.visit(featured_image_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 80,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA23341-1920x1200.jpg'"
      ]
     },
     "execution_count": 80,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# HTML Object \n",
    "html_image = browser.html\n",
    "\n",
    "# Parse HTML with Beautiful Soup\n",
    "soup = BeautifulSoup(html_image, \"html.parser\")\n",
    "\n",
    "# Retrieve background-image url from style tag \n",
    "image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]\n",
    "\n",
    "# Website Url \n",
    "main_url = \"https://www.jpl.nasa.gov\"\n",
    "\n",
    "# Concatenate website url with scrapped route\n",
    "image_url = main_url + image_url\n",
    "\n",
    "# Display full link to featured image\n",
    "image_url"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 83,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<table border=\"1\" class=\"dataframe\">\n",
      "  <thead>\n",
      "    <tr style=\"text-align: right;\">\n",
      "      <th></th>\n",
      "      <th>unit</th>\n",
      "      <th>value</th>\n",
      "    </tr>\n",
      "  </thead>\n",
      "  <tbody>\n",
      "    <tr>\n",
      "      <th>0</th>\n",
      "      <td>Equatorial Diameter:</td>\n",
      "      <td>6,792 km</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>1</th>\n",
      "      <td>Polar Diameter:</td>\n",
      "      <td>6,752 km</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>2</th>\n",
      "      <td>Mass:</td>\n",
      "      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>3</th>\n",
      "      <td>Moons:</td>\n",
      "      <td>2 (Phobos &amp; Deimos)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>4</th>\n",
      "      <td>Orbit Distance:</td>\n",
      "      <td>227,943,824 km (1.38 AU)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>5</th>\n",
      "      <td>Orbit Period:</td>\n",
      "      <td>687 days (1.9 years)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>6</th>\n",
      "      <td>Surface Temperature:</td>\n",
      "      <td>-87 to -5 °C</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>7</th>\n",
      "      <td>First Record:</td>\n",
      "      <td>2nd millennium BC</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>8</th>\n",
      "      <td>Recorded By:</td>\n",
      "      <td>Egyptian astronomers</td>\n",
      "    </tr>\n",
      "  </tbody>\n",
      "</table>\n"
     ]
    }
   ],
   "source": [
    "## Mars Facts\n",
    "# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.\n",
    "mars_facts_url = 'https://space-facts.com/mars/'\n",
    "browser.visit(mars_facts_url)\n",
    "\n",
    "facts_df = pd.read_html(mars_facts_url)[0]\n",
    "facts_df = facts_df.rename(columns = {0:'unit', 1:'value'})\n",
    "\n",
    "equatorial_diam = facts_df[facts_df['unit'] == 'Equatorial Diameter:']['value'].values[0]\n",
    "polar_diam = facts_df[facts_df['unit'] == 'Polar Diameter:']['value'].values[0]\n",
    "mass = facts_df[facts_df['unit'] == 'Mass:']['value'].values[0]\n",
    "moons = facts_df[facts_df['unit'] == 'Moons:']['value'].values[0]\n",
    "orbit_distance = facts_df[facts_df['unit'] == 'Orbit Distance:']['value'].values[0]\n",
    "orbit_period = facts_df[facts_df['unit'] == 'Orbit Period:']['value'].values[0]\n",
    "surface_temp = facts_df[facts_df['unit'] == 'Surface Temperature:']['value'].values[0]\n",
    "first_record = facts_df[facts_df['unit'] == 'First Record:']['value'].values[0]\n",
    "recorded_by = facts_df[facts_df['unit'] == 'Recorded By:']['value'].values[0]\n",
    "\n",
    "scrape_results = ({\n",
    "    'equatorial_diam':equatorial_diam,\n",
    "    'polar_diam':polar_diam,\n",
    "    'mass':mass,\n",
    "    'moons':moons,\n",
    "    'orbit_distance':orbit_distance,\n",
    "    'orbit_period':orbit_period,\n",
    "    'surface_temp':surface_temp,\n",
    "    'first_record':first_record,\n",
    "    'recorded_by':recorded_by,\n",
    "    })\n",
    "\n",
    "# Use Pandas to convert the data to a HTML table string.\n",
    "html_table = facts_df\n",
    "html_table = html_table.to_html()\n",
    "print(html_table)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 90,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit hemispheres website through splinter module \n",
    "hemispheres_url = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "browser.visit(hemispheres_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 91,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'title': 'Cerberus Hemisphere Enhanced',\n",
       "  'img_url': 'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'},\n",
       " {'title': 'Schiaparelli Hemisphere Enhanced',\n",
       "  'img_url': 'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'},\n",
       " {'title': 'Syrtis Major Hemisphere Enhanced',\n",
       "  'img_url': 'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'},\n",
       " {'title': 'Valles Marineris Hemisphere Enhanced',\n",
       "  'img_url': 'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'}]"
      ]
     },
     "execution_count": 91,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# HTML Object\n",
    "html_hemispheres = browser.html\n",
    "\n",
    "# Parse HTML with Beautiful Soup\n",
    "soup = BeautifulSoup(html_hemispheres, 'html.parser')\n",
    "\n",
    "# Retreive all items that contain mars hemispheres information\n",
    "items = soup.find_all('div', class_='item')\n",
    "\n",
    "# Create empty list for hemisphere urls \n",
    "hemisphere_image_urls = []\n",
    "\n",
    "# Store the main_ul \n",
    "hemispheres_main_url = 'https://astrogeology.usgs.gov'\n",
    "\n",
    "# Loop through the items previously stored\n",
    "for i in items: \n",
    "    # Store title\n",
    "    title = i.find('h3').text\n",
    "    \n",
    "    # Store link that leads to full image website\n",
    "    partial_img_url = i.find('a', class_='itemLink product-item')['href']\n",
    "    \n",
    "    # Visit the link that contains the full image website \n",
    "    browser.visit(hemispheres_main_url + partial_img_url)\n",
    "    \n",
    "    # HTML Object of individual hemisphere information website \n",
    "    partial_img_html = browser.html\n",
    "    \n",
    "    # Parse HTML with Beautiful Soup for every individual hemisphere information website \n",
    "    soup = BeautifulSoup( partial_img_html, 'html.parser')\n",
    "    \n",
    "    # Retrieve full image source \n",
    "    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']\n",
    "    \n",
    "    # Append the retreived information into a list of dictionaries \n",
    "    hemisphere_image_urls.append({\"title\" : title, \"img_url\" : img_url})\n",
    "    \n",
    "\n",
    "# Display hemisphere_image_urls\n",
    "hemisphere_image_urls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
