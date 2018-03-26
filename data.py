import csv
from datetime import date, datetime
import json
from shapely.geometry import Point, shape
from pymongo import MongoClient

config = json.loads(open("config.json").read())

# Gets the database to input data to from MongoDB
client = MongoClient('mongodb://'+config['mongo_user']+':'+config['mongo_pass']+'@'+config['mongo_host'])
db = client.get_database()

# Set up neighborhoods from GeoJSON file
with open('static/neighborhoods.geojson', 'r') as f:
    neighborhoods = [{"s": shape(feature['geometry']), "f": feature} for feature in json.load(f)['features']]

# Open the csv file that currently contains the data
with open('sfpd-dispatch/sfpd_dispatch_data_subset.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # go through the data and cast to correct variable type as necessary
        row["call_number"] = int(row["call_number"])

        row["incident_number"] = int(row["incident_number"])

        row["call_date"] = datetime.strptime(row["call_date"], '%m/%d/%y')

        row["watch_date"] = datetime.strptime(row["watch_date"], '%m/%d/%y')

        if row["received_timestamp"] == '':
            row["receiver_timestamp"] = None
        else:
            row["received_timestamp"] = datetime.strptime(row["received_timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")
            row["received_timestamp_hr"] = row["received_timestamp"].hour
            row["received_timestamp_min"] = row["received_timestamp"].minute

        if row["entry_timestamp"] == '':
            row["entry_timestamp"] = None
        else:
            row["entry_timestamp"] = datetime.strptime(row["entry_timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")

        if row["dispatch_timestamp"] == '':
            row["dispatch_timestamp"] = None
        else:
            row["dispatch_timestamp"] = datetime.strptime(row["dispatch_timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")

        if row["response_timestamp"] == '':
            row["response_timestamp"] = None
        else:
            row["response_timestamp"] = datetime.strptime(row["response_timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")

        if row["on_scene_timestamp"] == '':
            row["on_scene_timestamp"] = None
        else:
            row["on_scene_timestamp"] = datetime.strptime(row["on_scene_timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")

        if row["transport_timestamp"] == '':
            row["transport_timestamp"] = None
        else:
            row["transport_timestamp"] = datetime.strptime(row["transport_timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")

        if row["hospital_timestamp"] == '':
            row["hospital_timestamp"] = None
        else:
            row["hospital_timestamp"] = datetime.strptime(row["hospital_timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")

        if row["available_timestamp"] == '':
            row["available_timestamp"] = None
        else:
            row["available_timestamp"] = datetime.strptime(row["available_timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")

        row["zipcode_of_incident"] = int(row["zipcode_of_incident"])

        row["final_priority"] = int(row["final_priority"])

        row["als_unit"] = bool(row["als_unit"])

        row["number_of_alarms"] = int(row["number_of_alarms"])

        row["unit_sequence_in_call_dispatch"] = int(row["unit_sequence_in_call_dispatch"])

        row["latitude"] = float(row["latitude"])

        row["longitude"] = float(row["longitude"])

        #Find the neighborhood from this call
        pt = Point(row["longitude"], row["latitude"])
        for neighborhood in neighborhoods:
            if neighborhood["s"].contains(pt):
                row['neighborhood_district'] = neighborhood["f"]["properties"]["nhood"]
                break
        else:
            row['neighborhood_district'] = None

        # db.calls.insert_one(row)
