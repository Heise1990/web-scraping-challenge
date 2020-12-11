from flask import Flask, render_template
import scrape_mars
import pymongo

app = Flask('__name__')

app.static_folder = 'static'