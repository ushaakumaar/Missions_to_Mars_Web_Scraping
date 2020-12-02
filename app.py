###############################################
# Import Dependencies
###############################################
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

###############################################
# Flask Setup
###############################################

# create an app
app = Flask(__name__)

###############################################
# Database Setup
###############################################

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

###############################################
# Flask Routes
###############################################

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

###############################################
# Run the Flask Application
###############################################

if __name__ == "__main__":
    app.run(debug=True)
