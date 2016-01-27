# CREATED BY:
# Gert Sterenborg; gertsterenborg@gmail.com
# 21-01-2015

import os

import requests
from fiona import collection
from shapely.geometry import Point
from shapely.geometry import mapping


def get_latlng(place):
    """Get lattitude longitude dictionary for `place` from Google web api.

    Args:
        place (str): place to get coordinates for

    Returns:
        dictionary with keys `lat` and `lng` with corresponding values when
        status code is `200`, returns `None` if status code does not equal
        `200`
    """
    # Fetches coordinates from the google api
    url = "http://maps.googleapis.com/maps/api/geocode/json?address={}".format(
        place)
    response = requests.get(url)
    jsonF = response.json()
    if jsonF['status'] == "OK":
        lat = jsonF['results'][0]['geometry']['location']['lat']
        lng = jsonF['results'][0]['geometry']['location']['lng']
        return {'lat': lat, 'lng': lng}
    else:
        return None


def store_shape(shape_name, schema, data):
    """Stores `placeDic` as ESRI Shapefile at `path`

    Args:
        path (str): path to store shapefile at
        schema (dict): dictionary describing the schema of the data
        data (list): list of dicts which look like schema which will be
            stored to shapefile
    """
    with collection(shape_name, "w", "ESRI Shapefile", schema) as output:
        for row in data:
            output.write(row)


def read_txt(txt_file):
    """Read a text file and return lines as list.

    Args:
        txt_file (str): path to file to read

    Returns:
        list with lines of file as items.
    """
    with open(txt_file) as f:
        return f.readlines()


def places_to_shape():
    """Read text file with place names, get coordinates from google and
    write as shapefile.
    """
    # files and paths
    # current file location
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    txt_file = "places.txt"
    txt_file_root = txt_file[:-4]
    output_shape = os.path.join(path, txt_file_root + '.shp')

    # list where results will be stored
    results = []

    # our result will look like this
    schema = {'geometry': 'Point',
              'properties': {'place': 'str'}}

    # read from source
    places = read_txt(txt_file)

    # main loop
    for place in places:
        place = place.strip()
        latlng = get_latlng(place)
        print place, latlng
        point_geom = Point(float(latlng['lng']), float(latlng['lat']))
        results.append({'geometry': mapping(point_geom),
                        'properties': {'place': place}})

    # store results
    store_shape(output_shape, schema, results)


if __name__ == "__main__":
    places_to_shape()
