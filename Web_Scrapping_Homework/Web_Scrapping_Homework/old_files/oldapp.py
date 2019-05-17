from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
#db = client.team_db

# Drops collection if available to remove duplicates
#db.team.drop()

# Creates a collection in the database and inserts two documents
#db.team.insert_many(
    #[
        #{
            #'player': 'Jessica',
            #'position': 'Point Guard'
        #},
        #{
            #'player': 'Mark',
            #'position': 'Center'
        #}
    #]
#)


# Set route
@app.route('/')

def home():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)



#def index():
    # Store the entire team collection in a list
    #teams = list(db.team.find())
    #print(teams)

    # Return the template with the teams list passed in
    #return render_template('index.html', teams=teams)


if __name__ == "__main__":
    app.run(debug=True)
