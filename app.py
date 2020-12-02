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

