# Prerequisites
Make sure you have a connection to the internet to be able to run the geocoding API from OSM
Ensure the libraries from requirements.txt are installed

# Explanation
The script works by first figuring out the coordinates of the user's location by leveraging an geocoding API.  This 
converts addresses or zip codes into cartesian coordinates.  Using this coordinate, we calculate the great-circle 
distance in km between this location and each of the store's location, keeping track of the closest one so far.  Once
we finish iterating through the list, we'll format the output in accordance with the arguments and print out the 
result.
 
To simplify coding, I leveraged several libraries.  Docopts (https://github.com/docopt/docopt) simplifies input 
parsing. Geocoder (https://geocoder.readthedocs.io/index.html) abstracts several geocoding APIs and makes it easy to 
get the latitude and longitude of zip codes or addresses.  I use the Open Street Maps (OSM) API since it doesn't need
an API key to use.  Python's csv library provides a nice way to parse CSV files into OrderedDict however this puts a 
hard dependency on the header line. If any of the headers were to change, then a lot of this code would break; 
however the unit tests would catch if this happened.  To calculate the distance between two coordinates, I found the
formula to calculate great-circle distance (the shortest distance between two points on the surface of the sphere). 
This assumes the Earth is perfect sphere (I use a radius of 6371.008 km).  The json output is just a dictionary 
parsing of the csv line with some additional values for distance and units.
