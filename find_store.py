'''
Find Store
  find_store will locate the nearest store (as the vrow flies) from
  store-locations.csv, print the matching store address, as well as
  the distance to that store.

Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>            Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address="<address>"  Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)        Display units in miles or kilometers [default: mi]
  --output=(text|json)   Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
'''

import typing
import geocoder
import csv
import math
import json
import sys
from docopt import docopt

options = None
STORE_FILE = "store-locations.csv"
EARTH_RADIUS_KM = 6371.008
KM_TO_MI = 0.621371

output_format="""\
The closest location is the {Store Name} store, located {Distance:.2f} {Unit} away.
The store's address is:
    {Address}
    {City}, {State} {Zip Code}
"""


def run():
    location, json_resp, in_km = parse_args()
    local_coordinates = get_local_coordinates(location)
    if local_coordinates is None :
        sys.exit("The location provided could not be found. Please check your address or ZIP code.")
    closest_store, distance = find_closest_store(local_coordinates)
    print_store(closest_store, distance, json_resp, in_km)


def parse_args():
    options = docopt(__doc__)
    location = options['--address']
    if location is None :
        location = options['--zip']
    json_resp = options['--output'] == 'json'
    in_km = options['--units'] == 'km'
    return location, json_resp, in_km


def get_local_coordinates(location) -> typing.Tuple[float, float]:
    '''
    Find the latitude and longitude of a given location

    :param location: string input can be an address or a zipcode
    :return: Tuple signifying a lat, lng coordinate.  None if input location was not found
    '''
    geocode = geocoder.osm(location)
    if not geocode.ok:
        return None
    lat = geocode.json['lat']
    lng = geocode.json['lng']
    return lat, lng


def find_closest_store(local_coordinates) -> typing.Tuple[dict, float]:
    '''
    Goes through the store-location csv file and finds the closest store to the input coordinate

    :param local_coordinates: tuple coordinate that we're trying to find the closest store to
    :return: dictionary with all the details of the store and the distance to that store
    '''
    closest_store = {}
    closest_distance = float('inf')
    # encoding needed due to a error noted in the header
    with open(STORE_FILE, encoding="utf-8-sig") as storeFile:
        storeReader = csv.DictReader(storeFile)
        for store in storeReader:
            # Get the latitude and longitude form the file in tuple format
            store_coordinates = (float(store['Latitude']), float(store['Longitude']))
            dist_to_store = calculate_great_circle_km(local_coordinates, store_coordinates)
            if dist_to_store < closest_distance :
                closest_store = store
                closest_distance = dist_to_store

    return dict(closest_store), closest_distance


def calculate_great_circle_km(c1, c2) -> float:
    '''
    Find the great circle distance between c1 and c2 in km
    This is calculated using the spherical law of cosines
    https://en.wikipedia.org/wiki/Great-circle_distance

    We'll need to convert the coordinates to degrees and then the final degree into distance
    :param c1:
    :param c2:
    :return:
    '''
    rc1 = get_radial_coordinates(c1)
    rc2 = get_radial_coordinates(c2)
    delta_lng_rad = abs(rc2[1] - rc1[1])
    sin_product = math.sin(rc1[0]) * math.sin(rc2[0])
    cos_product = math.cos(rc1[0]) * math.cos(rc2[0]) * math.cos(delta_lng_rad)
    delta_rad = math.acos(sin_product+cos_product)
    return delta_rad * EARTH_RADIUS_KM


def get_radial_coordinates(coord):
    return (coord[0] * math.pi/180), (coord[1] * math.pi/180)


def print_store(closest_store, distance, json_resp, in_km):
    unit = 'km'
    if not in_km :
        distance *= KM_TO_MI
        unit = 'mi'
    closest_store['Distance'] = distance
    closest_store['Unit'] = unit
    if json_resp:
        output = json.dumps(closest_store)
    else :
        output = output_format.format(**closest_store)
    print(output)


if __name__ == '__main__' :
    run()
