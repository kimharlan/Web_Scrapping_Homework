from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")


@app.route('/')
def index():
    latest_mars = mongo.db.mars_scrape.find_one()
    return render_template('index.html', latest_mars=latest_mars)


@app.route('/scrape')
def scrape():
    mars_data_scrape = mongo.db.mars_scrape
    data = mission_to_mars.scrape()
    mars_data_scrape.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
