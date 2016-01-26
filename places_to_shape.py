# CREATED BY:
# Gert Sterenborg; gertsterenborg@gmail.com
# 21-01-2015

import json
import os
import urllib2

from osgeo import ogr
from osgeo import osr


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
    response = urllib2.urlopen(url)
    jsonF = json.loads(response.read())
    if jsonF['status'] == "OK":
        lat = jsonF['results'][0]['geometry']['location']['lat']
        lng = jsonF['results'][0]['geometry']['location']['lng']
        return {'lat': lat, 'lng': lng}
    else:
        return None


def store_shape(path, shape_name, placeDic):
    """Stores `placeDic` as ESRI Shapefile at `path`

    Args:
        path (str): path to store shapefile at
        placeDic (dict): dictionary which looks like
            {'<placename': {'lat': <lat>}, 'lng': <lng> }
    """
    spatialReference = osr.SpatialReference()
    spatialReference.ImportFromEPSG(4326)  # WGS84 degrees coordinates
    # will select the driver for our shp-file creation.
    driver = ogr.GetDriverByName('ESRI Shapefile')
    # so there we will store our data
    shapeData = driver.CreateDataSource(path)
    # this will create a corresponding layer for our data with given
    # spatial information.
    layer = shapeData.CreateLayer(shape_name, spatialReference, ogr.wkbPoint)
    # gets parameters of the current shapefile
    layer_defn = layer.GetLayerDefn()
    new_field = ogr.FieldDefn('PLACE', ogr.OFTString)
    layer.CreateField(new_field)
    point = ogr.Geometry(ogr.wkbPoint)
    i = 0
    for place in placeDic:
        # create a new point at given ccordinates
        point.AddPoint(placeDic[place]['lng'], placeDic[place]['lat'])
        featureIndex = i
        feature = ogr.Feature(layer_defn)
        feature.SetGeometry(point)
        feature.SetFID(featureIndex)
        j = feature.GetFieldIndex("PLACE")
        feature.SetField(j, place)
        layer.CreateFeature(feature)
        i += 1
    shapeData.Destroy()  # lets close the shapefile


def remove_shape(path, file_name):
    """Removes shapefile `filename` at `path`.

    Args:
        path (str): path the shapefile is stored at
        file_name (str): name of shapefile
    """
    # removes the exsisting shapefile
    extensions = ["shp", "shx", "prj", "dbf"]
    for extension in extensions:
        command = "rm " + path + file_name + "." + extension
        os.system(command)


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

    # dictionary where all the coordinates and places will be stored in
    placeDic = {}

    # read from source
    places = read_txt(txt_file)

    # main loop
    for place in places:
        place = place.strip()
        latlng = get_latlng(place)
        print place, latlng
        placeDic[place] = latlng

    # remove shape, if exists
    remove_shape(path, txt_file_root)

    # store results
    store_shape(path, txt_file_root, placeDic)


if __name__ == "__main__":
    places_to_shape()
