# find_store.py
import typing
import geocoder

options = None
STORE_FILE = "store-locations.csv"


def run():
    options = parse_args()
    local_coordinates = get_local_coordinates(None)
    closest_store = find_closest_store(local_coordinates)
    print_store(closest_store)


def parse_args():
    return {}


def get_local_coordinates(location) -> typing.Tuple[float, float]:
    geocode = geocoder.mapquest(location)
    lat = geocode.json['lat']
    lng = geocode.json['lng']
    return lat, lng


def find_closest_store(local_coordinates) -> dict:
    return {}


def print_store(closest_store) :
    print(closest_store)


if __name__ == '__main__' :
    run()
