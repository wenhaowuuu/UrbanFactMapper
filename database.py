import sqlite3

DATABASE = "census_data.db"

# Mapping of state codes to state names
STATE_NAMES = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
}

# Mapping of county codes to county names for the sample states
COUNTY_NAMES = {
    "06": {  # California
        "001": "Alameda County",
        "003": "Alpine County",
        "005": "Amador County",
        "007": "Butte County",
        "009": "Calaveras County",
        "011": "Colusa County",
        "013": "Contra Costa County",
        "015": "Del Norte County",
        "017": "El Dorado County",
        "019": "Fresno County",
        "021": "Glenn County",
        "023": "Humboldt County",
        "025": "Imperial County",
        "027": "Inyo County",
        "029": "Kern County",
        "031": "Kings County",
        "033": "Lake County",
        "035": "Lassen County",
        "037": "Los Angeles County",
        "039": "Madera County",
        "041": "Marin County",
        "043": "Mariposa County",
        "045": "Mendocino County",
        "047": "Merced County",
        "049": "Modoc County",
        "051": "Mono County",
        "053": "Monterey County",
        "055": "Napa County",
        "057": "Nevada County",
        "059": "Orange County",
        "061": "Placer County",
        "063": "Plumas County",
        "065": "Riverside County",
        "067": "Sacramento County",
        "069": "San Benito County",
        "071": "San Bernardino County",
        "073": "San Diego County",
        "075": "San Francisco County",
        "077": "San Joaquin County",
        "079": "San Luis Obispo County",
        "081": "San Mateo County",
        "083": "Santa Barbara County",
        "085": "Santa Clara County",
        "087": "Santa Cruz County",
        "089": "Shasta County",
        "091": "Sierra County",
        "093": "Siskiyou County",
        "095": "Solano County",
        "097": "Sonoma County",
        "099": "Stanislaus County",
        "101": "Sutter County",
        "103": "Tehama County",
        "105": "Trinity County",
        "107": "Tulare County",
        "109": "Tuolumne County",
        "111": "Ventura County",
        "113": "Yolo County",
        "115": "Yuba County",
    },
    "36": {  # New York
        "001": "Albany County",
        "003": "Allegany County",
        "005": "Bronx County",
        "007": "Broome County",
        "009": "Cattaraugus County",
        "011": "Cayuga County",
        "013": "Chautauqua County",
        "015": "Chemung County",
        "017": "Chenango County",
        "019": "Clinton County",
        "021": "Columbia County",
        "023": "Cortland County",
        "025": "Delaware County",
        "027": "Dutchess County",
        "029": "Erie County",
        "031": "Essex County",
        "033": "Franklin County",
        "035": "Fulton County",
        "037": "Genesee County",
        "039": "Greene County",
        "041": "Hamilton County",
        "043": "Herkimer County",
        "045": "Jefferson County",
        "047": "Kings County",
        "049": "Lewis County",
        "051": "Livingston County",
        "053": "Madison County",
        "055": "Monroe County",
        "057": "Montgomery County",
        "059": "Nassau County",
        "061": "New York County",
        "063": "Niagara County",
        "065": "Oneida County",
        "067": "Onondaga County",
        "069": "Ontario County",
        "071": "Orange County",
        "073": "Orleans County",
        "075": "Oswego County",
        "077": "Otsego County",
        "079": "Putnam County",
        "081": "Queens County",
        "083": "Rensselaer County",
        "085": "Richmond County",
        "087": "Rockland County",
        "089": "St. Lawrence County",
        "091": "Saratoga County",
        "093": "Schenectady County",
        "095": "Schoharie County",
        "097": "Schuyler County",
        "099": "Seneca County",
        "101": "Steuben County",
        "103": "Suffolk County",
        "105": "Sullivan County",
        "107": "Tioga County",
        "109": "Tompkins County",
        "111": "Ulster County",
        "113": "Warren County",
        "115": "Washington County",
        "117": "Wayne County",
        "119": "Westchester County",
        "121": "Wyoming County",
        "123": "Yates County",
    },
}

def get_db():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    return conn

def insert_census_data(year, state, county, tract, population):
    """Insert census data into the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO census_data (year, state, county, tract, population)
            VALUES (?, ?, ?, ?, ?)
        """, (year, state, county, tract, population))
        conn.commit()

def fetch_census_data(state, county, tract):
    """Fetch census data from the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT population FROM census_data
            WHERE state = ? AND county = ? AND tract = ?
        """, (state, county, tract))
        result = cursor.fetchone()
        return result[0] if result else None

## TODO: get all state, county, and tracts mapping from US Census

def get_states():
    """Fetch all unique states from the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT state FROM census_data")
        states = cursor.fetchall()
        # Map state codes to state names
        return [(state[0], STATE_NAMES.get(state[0], "Unknown State")) for state in states]
        # return [row[0] for row in cursor.fetchall()]

def get_counties(state):
    """Fetch all unique counties for a given state."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT county FROM census_data WHERE state = ?", (state,))
        counties = cursor.fetchall()

        # Map county codes to county names
        return [(county[0], COUNTY_NAMES.get(state, {}).get(county[0], "Unknown County")) for county in counties]
        # return [row[0] for row in cursor.fetchall()]

def get_tracts(state, county):
    """Fetch all unique tracts for a given state and county."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tract FROM census_data WHERE state = ? AND county = ?", (state, county))
        return [row[0] for row in cursor.fetchall()]