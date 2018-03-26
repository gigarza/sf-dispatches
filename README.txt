    I decided to split all the information for the web application into 4 web pages. However, before beginning I
imported all of the data into a mongoDB database hosted by mLab. I did this by creating a python file (data.py) which
accessed the database, then would put in one document per row from the csv file given. For each of these rows from the
file, one specific call, I casted the data to its appropriate variable type, and added the features of received hour,
received minute, and neighborhood. Following this, I created a homepage which
simply introduces the user to the web application and allows them to access all the pages from the click of a button.
    The first page, Statistics & Graphs, gives the user a very broad overview of a variety of the information that can
be found from the data. At the top of this page, you can see 6 different statistical numbers represented the amounts of
different variables. To solve these I simply looped through all the documents in the databased to find all the
different options for that specific variable, and then returned the length of that list. Following this, there are 3
data visuals, which adhere to the first deliverable.
    The first graph shows the average amount of calls for each hour in a given day. To get the data points I needed for
this, I began by creating a list of length 24, aka one index per hour. Then when looping through all the documents, I
would look at the hour for the given call and increment the index equal to that hour value in the list accordingly. At
the same time, I also kept a list of all of the different days the calls covered, so that after looping through I could
take each hour and divide by the number of days covered to find the average number of calls at that hour mark. To
create the graph, I used javascript and a chartist template.
    The second graph is a bar graph which shows number of calls considered of type fire that occurred in each fire
prevention district. I was able to do this by narrowing down to a list of the documents that had the fire call type, and
then creating a dictionary were the keys were the fire prevention district and the values was the number of total calls
from our reduced list that occurred in that district. Similarly to the first graph, I also used javascript and a
chartist template to create the visual graph to show up on the page.
    The final data visual is a pie chart which shows the different percentage of calls per dispatch type (unit_type). To
do this I created a dictionary that had keys that were unit_types and values which were the number of calls for that
unit type, which I solved for by incrementing accordingly when looping through all the documents from the database. To
create the visual on the page, I again used javascript and a chartist template.
    Following this we look at the next page, Informational Maps. Here, we have 4 different tabs which hold different
maps to show different information from the data. The first tab, Dispatch Times, meets the third deliverable by showing
the zipcodes which generally take the longest time to dispatch. The algorithm I used to solve this was by looping
through all the to a dictionary where the keys were zipcodes and the value was a list of the time differences for
various calls. Lastly, I found the mean of these times for each zipcode, then returned the 3 zipcodes which had the
highest averages. To display this information on a map, I connected my javascript to the GeoJson file with the zipcode
information for San Francisco. This allowed me to overlay a shade on the map which outlined all the zipcodes. I then
compared my results from the python file to highlight those top zipcodes in red.
    The second tab, Heat Map, has a heat map to show the frequency of calls throughout the city, which meets the first
of the bonus. To do this, I first went through all the documents/calls and appended each latitude and longitude
combination to a list. I then put this data into a javascript file which created a heat map with the google maps API.
    The third tab, Safe Neighborhoods, shows the safest neighborhoods in the city based of of the unit types and
frequency of calls, which meets the second bonus. I solved this by first narrowing down the list of documents to calls
which only had unit types which seemed like they could be crime related. I then looped through this list, and for each
call I would increment the number of calls that had occurred for that neighborhood. Lastly, I returned a list of the
neighborhoods with the highest amount of calls for the unit parameters given. To display this, I connected the
javascript to a GeoJson file which had the information about the neighborhoods for the city. I used this to create a
gray overlap on the map which outlined the various neighborhoods. I then compared my results, and highlighted the 3
neighborhoods which were the safest.
    The fourth and final tab, Increasing Dispatches, shows the zipcodes with the greatest increase in dispatch calls. To
solve this I first created a dictionary where the keys were zipcodes and the values were another dictionary which
mapped each day to the number of calls that were made that day in that zipcode. To make sure I accounted for days
without calls I then added in 0 calls for any unaccounted days. To keep these dates sorted, I used an OrderedDict, but
had to consistently push dates to the end when adding in the no-call days to keep the order. After this, I then
continuously compared the difference in the number of calls from day to day for each zipcode and added this value to
a new dictionary mapping zipcodes to tall differences. I then averaged this difference to find the average increase in
calls for each zipcode, and returned the 3 zipcodes with the highest increase. To display this, I connected the
javascript to the same zipcode GeoJson file from the first tab to create the gray overlay on the map outlining the
zipcodes. Similarly to the first tab, I then compared results and highlighted the 3 zipcode results in red.
    Lastly, we have the Most Likely Dispatch page which will display the most likely dispatch given an address and time.
I first created a default page which displays a graph that will place a marker at the address the user inputs, used from
the google maps API. I then connected a timepicker template to add in the timepicker for the user to choose a time. Once
they click submit, I begin an algorithm to find the most likely dispatch. This finds all the calls within a 15 minute
range of the given time and a .005 degree of the latitude and longitude. I then go through these calls and find the
total number of calls that have been given for each unit type. I finally return the highest of these, which will be the
most likely dispatch for that address and time. I then use this result to replace the text on the page to show
information about that result.