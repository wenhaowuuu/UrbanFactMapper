from database import insert_census_data

# Sample data: Two states, each with two counties and two tracts
sample_data = [
    # State: California (06)
    {"year": 2023, "state": "06", "county": "073", "tract": "020100", "population": 5000},  # San Diego County
    {"year": 2023, "state": "06", "county": "073", "tract": "020200", "population": 4500},  # San Diego County
    {"year": 2023, "state": "06", "county": "037", "tract": "010100", "population": 6000},  # Los Angeles County
    {"year": 2023, "state": "06", "county": "037", "tract": "010200", "population": 5500},  # Los Angeles County

    # State: New York (36)
    {"year": 2023, "state": "36", "county": "061", "tract": "030100", "population": 7000},  # New York County (Manhattan)
    {"year": 2023, "state": "36", "county": "061", "tract": "030200", "population": 6500},  # New York County (Manhattan)
    {"year": 2023, "state": "36", "county": "005", "tract": "040100", "population": 8000},  # Bronx County
    {"year": 2023, "state": "36", "county": "005", "tract": "040200", "population": 7500},  # Bronx County
]

# Insert sample data into the database
for data in sample_data:
    insert_census_data(data["year"], data["state"], data["county"], data["tract"], data["population"])

print("Sample data inserted successfully!")