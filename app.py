from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import timedelta, datetime
from statistics import mean
from collections import Counter, OrderedDict
import os
import json
import sys

# Set up flask
app = Flask(__name__)

debug = False

if os.path.isfile("config.json"):
    conf = json.loads(open("config.json").read())
    for key in conf:
        app.config[key] = conf[key]
    debug = True
else:
    req = ["mongo_user", "mongo_pass", "mongo_host"]
    for key in req:
        val = os.environ.get(key, None)
        if val is None:
            sys.exit("Missing config: " + key)
        app.config[key] = val

# Get the database
client = MongoClient('mongodb+srv://'+app.config['mongo_user']+':'+app.config['mongo_pass']+'@'+app.config['mongo_host'])
db = client.get_database()


# Set up the homepage
@app.route('/')
def homepage():
    return render_template("index.html")


# Set up the page for the statistics & visuals
@app.route('/statistics')
def statistics():
    # Variables for Statistics
    num_calls = db.calls.find().count()
    call_types = []
    num_stations = []
    supervisor_districts = []

    # Variables for Graphs
    calls_per_hour = [0] * 24
    days_covered = []
    district_calls = {}
    unit_calls = {}

    # Iterate through all the calls from the database
    for document in db.calls.find():
        # Find the call type, if not already listed add to list of all call types
        call_type = document["call_type"]
        if call_type not in call_types:
            call_types.append(call_type)

        # Find the station, if not already listed add to list of all stations
        station = document["station_area"]
        if station not in num_stations:
            num_stations.append(station)

        # Find the supervising district, if not already listed add to list of all supervisor districts
        supervisor = document["supervisor_district"]
        if supervisor not in supervisor_districts:
            supervisor_districts.append(supervisor)

        # Find the hour from the call, increment to num total from that hour accordingly
        call_time = document["received_timestamp"]
        hour = call_time.hour
        calls_per_hour[hour] += 1

        # Find the day from this call, add to list if not already there
        day = call_time.day
        if day not in days_covered:
            days_covered.append(day)

        # Find the unit type from this call, add to total num calls per unit type
        unit_type = document["unit_type"]
        if unit_type in unit_calls:
            unit_calls[unit_type] += 1
        else:
            unit_calls[unit_type] = 1

    # Average the number of calls per day within each hour
    num_days = len(days_covered)
    index = 0
    for hour in calls_per_hour:
        calls_per_hour[index] /= num_days
        index += 1

    # Find all the calls that are specifically for Fire
    possible_calls = db.calls.find({"call_type_group": "Fire"})
    # Loop through these calls. Add up the number of calls that are fire related for each fire prevention district
    for call in possible_calls:
        district = call["fire_prevention_district"]
        if district in district_calls:
            district_calls[district] += 1
        else:
            district_calls[district] = 1

    # Create the page
    return render_template("statistics.html", calls=calls_per_hour, district=district_calls, units=unit_calls,
                           num_calls=num_calls, num_types=len(call_types), stations=len(num_stations),
                           unit_num=len(unit_calls), district_num=(len(district_calls)-1),
                           supervisors=len(supervisor_districts))


# Set up the page with information shown on maps
@app.route('/maps')
def maps():
    # Variable for Dispatch Times tab
    time_for_areas = {}

    # Variable for Heat Map tab
    lat_longs = []

    # Variables for Increasing Dispatches map
    calls_per_day = {}
    days = []

    # Iterate through all the calls from the database
    for document in db.calls.find():
        # Find the time it took to dispatch in seconds
        time_diff = document["dispatch_timestamp"] - document["received_timestamp"]
        time_to_dispatch = time_diff.total_seconds()

        # Find the zipcode of this call, for each zipcode add the time it took to dispatch
        zipcode = document["zipcode_of_incident"]
        if zipcode in time_for_areas:
            time_for_areas[zipcode].append(time_to_dispatch)
        else:
            time_for_areas[zipcode] = [time_to_dispatch]

        # Add the latitude and longitude from this call to the dictionary for the locations of each call
        lat_longs.append({"lat": document["latitude"], "lng": document["longitude"]})

        # Find the day from this call, and add it to the list of days
        day = document["call_date"]
        if day not in days:
            days.append(day)

        # For each call, find the zipcode, and increase the amount of calls for the specific day at that zipcode
        if zipcode in calls_per_day:
            if day in calls_per_day[zipcode]:
                calls_per_day[zipcode][day] += 1
            else:
                calls_per_day[zipcode][day] = 1
        else:
            # Since the database is ordered by the date, make this an ordered dictionary so sorted by when they come in
            calls_per_day[zipcode] = OrderedDict()
            calls_per_day[zipcode][day] = 1
            # Variables for Safe Neighborhoods tab

    # For the Dispatch Times tab
    # Find the average time to dispatch for each zipcode
    average_times = {}
    for area in time_for_areas:
        average_time = mean(time_for_areas[area])
        average_times[area] = average_time
    # Find the 3 zipcodes which receive the highest average time to dispatch
    counter_zip_list = Counter(average_times)
    highest_times = counter_zip_list.most_common(3)
    high_zips = []
    for zipcode in highest_times:
        high_zips.append(zipcode[0])

    # For Safe Neighborhoods Tab
    # Find all the calls which seem to call a unit type that could be correlated to a crime
    neighborhood_calls = db.calls.find({"$or": [{"unit_type": "MEDIC"}, {"unit_type": "CHIEF"},
                                                {"unit_type": "PRIVATE"}, {"unit_type": "SUPPORT"},
                                                {"unit_type": "INVESTIGATION"}]})
    # For each call, find its neighborhood, and increase the number of calls for that neighborhood
    nhood_num_calls = {}
    for call in neighborhood_calls:
        neighborhood = call["neighborhood_district"]
        if neighborhood in nhood_num_calls:
            nhood_num_calls[neighborhood] += 1
        else:
            nhood_num_calls[neighborhood] = 1
    # Find the 3 neighborhoods which receive the least amount of calls
    counter_nhood_list = Counter(nhood_num_calls)
    safest_nhood = counter_nhood_list.most_common()[:-4:-1]
    safe_neighborhoods = []
    for neighborhood in safest_nhood:
        safe_neighborhoods.append(neighborhood[0])

    # For Increasing Dispatches Tab
    # Go through each zipcode, and add in any days that had no calls
    for zipcode in calls_per_day:
        for day in days:
            if day in calls_per_day[zipcode]:
                # Re-order as go so that they stay in order based on date
                calls_per_day[zipcode].move_to_end(day)
            else:
                calls_per_day[zipcode][day] = 0
    # For each zipcode, find the add up all the differences in amount of calls from day to day
    zip_increases = {}
    for zipcode in calls_per_day:
        # Set previous day to none to account for skipping getting difference for first day
        previous_day = None
        for day in calls_per_day[zipcode]:
            if previous_day is not None:
                zip_increases[zipcode] += calls_per_day[zipcode][day] - calls_per_day[zipcode][previous_day]
            else:
                # Sets initial difference to zero
                zip_increases[zipcode] = 0
            # Keep track of previous day
            previous_day = day
    # Average the differences across the number of days that there are to find the average increase in amount of calls
    for zipcode in zip_increases:
        zip_increases[zipcode] = zip_increases[zipcode] / (len(days) - 1)
    # Find the 3 zipcodes which have the highest average increase in number of calls
    counter_inc_list = Counter(zip_increases)
    highest_increase = counter_inc_list.most_common(3)
    high_inc = []
    for zipcode in highest_increase:
        high_inc.append((zipcode[0]))

    # Create the page
    return render_template("maps.html", times=high_zips, lat_longs=lat_longs,
                           increases=high_inc, safest=safe_neighborhoods)


# Set up the default page for finding the most likely dispatch
@app.route('/interactive')
def interactive():
    # Create the page
    return render_template("which_dispatch.html")


# Find the most likely dispatch, and send result to JS to replace text on page
@app.route('/interactive_data')
def interactive_data():
    # Get the latitude and longitude from the address the user requested
    user_latitude = float(request.args.get("lat"))
    user_longitude = float(request.args.get("lng"))
    # Get the time the user requested
    given_time = request.args.get("time")
    user_time = datetime.strptime(given_time, "%H:%M%p")
    # Adjust the hour variable accordingly if a pm hour
    if given_time[-2:] == "pm":
        user_time += timedelta(hours=12)

    # Find the range of latitude and longitudes to look at
    min_latitude_want = user_latitude - .005
    max_latitude_want = user_latitude + .005
    min_longitude_want = user_longitude - .005
    max_longitude_want = user_longitude + .005
    # Find the range of time to look at
    min_time_want = user_time - timedelta(minutes=15)
    max_time_want = user_time + timedelta(minutes=15)
    min_hour_want = min_time_want.hour
    min_min_want = min_time_want.minute
    max_hour_want = max_time_want.hour
    max_min_want = max_time_want.minute

    # Find all the calls that match both the ranges of location and time
    if max_min_want > min_min_want:
        # We know it's the same hour, and that we can easily get only the range in minutes
        possible_calls = db.calls.find({"latitude": {"$gt": min_latitude_want, "$lt": max_latitude_want},
                                        "longitude": {"$gt": min_longitude_want, "$lt": max_longitude_want},
                                        "received_timestamp_hr": min_hour_want,
                                        "received_timestamp_min": {"$gte": min_min_want, "$lte": max_min_want}
                                        })
    else:
        # Special Case: we have two separate hours we have to look at
        # Same situation for location, but for time find ones that match higher hour and are less than the greater
        # minute or ones that match the smaller hour and are greater than the lower minute
        # Example Special Case: Range is {3:55-4:25}; We would find times that are within hour 4 and minutes 0-25
        # or within hour 3 and minutes 55-59
        possible_calls = db.calls.find({"latitude": {"$gt": min_latitude_want, "$lt": max_latitude_want},
                                        "longitude": {"$gt": min_longitude_want, "$lt": max_longitude_want},
                                        "$or": [{"received_timestamp_hr": max_hour_want,
                                                 "received_timestamp_min": {"$lte": max_min_want}},
                                                {"received_timestamp_hr": min_hour_want,
                                                 "received_timestamp_min": {"$gte": min_min_want}}]})

    # For each call, find the unit type and increase the number of calls for that unit type
    dispatch_results = {}
    for call in possible_calls:
        dispatch_type = call["unit_type"]
        if dispatch_type in dispatch_results:
            dispatch_results[dispatch_type] += 1
        else:
            dispatch_results[dispatch_type] = 1
    # Get the unit_type that has the most calls for our given parameters, this will be the most likely dispatch
    counter_list = Counter(dispatch_results)
    highest_result = counter_list.most_common(1)
    high_chance = [""]
    for result in highest_result:
        high_chance[0] = (result[0])

    # Send the result to the javascript
    return high_chance[0]


# Starts the server
if __name__ == '__main__':
    app.run(port=os.environ.get("PORT", 5000), debug=debug)
