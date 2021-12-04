from flask import Flask, render_template, redirect
import pymongo 
from flask_pymongo import PyMongo
import mission_to_mars


# Create an instance of Flask
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client.Mars_db


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    details = list(db.details.find())
    return render_template("index.html", details=details)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mission_to_mars.scrape()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
