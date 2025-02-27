### Urban Fact Mapper ###
# Wenhao's first Flask app
## Requirements
#1 quick fact finder page (State - County - City - Tract)
#2 city based mapper
# user search for a city 
# it checks for the stored ACS data downloaded from ACS API, filter to the county it belongs to
# the app fetches the maps and charts for that city (previously run)
# TBD: the app does the spatial join and clipping to the city boundary
# TBD: the app creates the maps


# # Step 1: Initialize the database
# python init_db.py

# # Step 2: Populate the database with sample data
# python insert_sample_data.py

# # Step 3: Start the Flask app
# python hello.py

import requests
import sqlite3
from flask import Flask, request, jsonify, g, render_template
from database import fetch_census_data, get_states, get_counties, get_tracts

app = Flask(__name__)

# set up app databse
DATABASE = "census_data.db"

def get_db():
    """Get a connection to the SQLite database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# default route
# app will run at: http://127.0.0.1:5000/
@app.route("/")
def home():
    # Fetch all states from the database
    states = get_states()
    # Pass the states to the template
    return render_template('index.html', states=states)
    # "<h1>Urban Fact Mapper</h1><br><p>Use the search bar to start with any city in the U.S.</p>"

@app.route('/counties', methods=['GET'])
def get_counties_route():
    """Fetch counties for a given state."""
    state = request.args.get('state')
    counties = get_counties(state)
    return jsonify(counties)

@app.route('/tracts', methods=['GET'])
def get_tracts_route():
    """Fetch tracts for a given state and county."""
    state = request.args.get('state')
    county = request.args.get('county')
    tracts = get_tracts(state, county)
    return jsonify(tracts)

@app.route('/population', methods=['GET'])
def get_population():
    """Fetch population data for a given state, county, and tract."""
    state = request.args.get('state')
    county = request.args.get('county')
    tract = request.args.get('tract')
    population = fetch_census_data(state, county, tract)
    if population:
        return jsonify({"population": population})
    else:
        return jsonify({"error": "Data not found"}), 404

# city reporter route
@app.route("/city-reporter")
def city_reporter():
    """Render the City Reporter page."""
    return render_template('city_reporter.html')

# search city
# @app.route('/search-city', methods=['GET'])
# def search_city():
#     """Fetch data for a given city."""
#     city = request.args.get('city')
#     # Replace this with actual logic to fetch city data from your database
#     if city.lower() == "san francisco":
#         return jsonify({"city": city, "population": 883305, "ami": 186600})
#     else:
#         return jsonify({"error": "City not found"}), 404


@app.route('/search-city', methods=['GET'])
def search_city():
    """Fetch population data for a given city using the Census API."""
    city = request.args.get('city')
    state = "06"  # California

    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

# Ref: 
# https://api.census.gov/data/2023/acs/acs5/examples.html
# https://api.census.gov/data/2023/acs/acs5?get=NAME,B01001_001E&for=place:*&in=state:06
    # Construct the API URL
    api_url = f"https://api.census.gov/data/2023/acs/acs5?get=NAME,B01001_001E&for=place:*&in=state:{state}"

    try:
        # Make the API request
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()

        # Find the city in the API response
        for entry in data[1:]:  # Skip the header row
            if city.lower() in entry[0].lower():  # Case-insensitive search
                return jsonify({
                    "city": entry[0],
                    "population": entry[1],
                    "state": entry[2],
                    "place": entry[3]
                })

        # If the city is not found
        return jsonify({"error": f"City '{city}' not found in California."}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data from Census API: {str(e)}"}), 500

# about route
@app.route("/about")
def about():
    return render_template('about.html')
    # "<h3>About Page</h3><br><p>This is a web application developed to streamline the Existing Condition Analysis process for city planning projects.</p><br><small>Developed by Wenhao Wu</small>"

# methodology route
@app.route("/methodology")
def methods():
    return render_template('methodology.html')
    # "<h3>Methodology</h3><br><p>Methods include automated data pipelines, analytical scripts, geopandas, and interactive charts.</p><br><small>Developed by Wenhao Wu</small>"

# Run the app
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True) #explicitly bind the app to the port 0.0.0.0

# in command line, run this:
# python app.py