from flask import Flask, render_template
import scrape_mars
import pymongo

app = Flask('__name__')

newsURL = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
mars_facts_url = 'https://space-facts.com/mars/'

@app.route('/scrape')
def scrape_route():
    # scrape results to put in database
    scrape_results = scrape_mars.scrape()

    # connect to db
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # create db
    mars_db = myclient["mars_db"]
    # create collection in db
    mars_collection = mars_db["mars_collection"]
    # Clear Collection
    mars_collection.remove({})
    # Insert Data
    mars_collection.insert_one(scrape_results)

    return '<div>Mars Data Added</div><a href="/">Go Back</a>'

@app.route('/')
def root_route():
    # connect to db
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # create db
    mars_db = myclient["mars_db"]
    # create collection in db
    mars_collection = mars_db["mars_collection"]
