###############################################
# Import Dependencies
###############################################
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

###############################################
# Database Setup
###############################################

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

###############################################
# Flask Setup & Routes
###############################################

# create an app
app = Flask(__name__)

#define endpoints
@app.route("/")
def index():
    mars_facts = mongo.db.mars_facts.find_one()
    return render_template("index.html", mars_facts=mars_facts)


@app.route("/scrape")
def scraper():
    mars_facts = mongo.db.mars_facts
    scrape_mars_list = scrape_mars.scrape()
    mars_facts.update({}, scrape_mars_list, upsert=True)
    return redirect("/", code=302)

