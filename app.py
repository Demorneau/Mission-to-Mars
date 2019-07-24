# Importing the jupyter notebbok (python) depandencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from flask import render_template
from scrape_mars import scrape
from pymongo import MongoClient
import json
import pprint

# Use Mongodb with flask templating to create a new HTML page
app = Flask(__name__, template_folder='.')
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
#mongoImp = db.insert_many(odbcArray)

# Store the return value in Mongo as Python Dictionary
client = MongoClient()
db = client["myDatabase"]
collection = db["marsComplete_data"]
marsComplete_data = {}

# Create a root route to querry Mongo database and pass the mars data into HTML
@app.route("/")
def index():
    #marsComplete_data = list(db.collection.find())[0]
    marsComplete_data = mongo.db.marsComplete_data.find_one()
    return render_template('index.html', marsComplete_data=marsComplete_data )

# Create a route call scrape to import the scrape_mars file to the scrape function
@app.route("/scrape")
def web_scrape():
    marsComplete_data = mongo.db.marsComplete_data
    mars_data = scrape()
    #collection.insert_one(marsComplete)
    marsComplete_data.update({}, mars_data, upsert= True)
    return  "Some else!!"
    #return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)