# CREATED BY:
# Gert Sterenborg; gertsterenborg@gmail.com
# 21-01-2015

import json
import os
import urllib2

from osgeo import ogr
from osgeo import osr


def get_latlng(place):
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


def store_shape(path, placeDic):
    spatialReference = osr.SpatialReference()
    spatialReference.ImportFromEPSG(4326)  # WGS84 degrees coordinates
    # will select the driver for our shp-file creation.
    driver = ogr.GetDriverByName('ESRI Shapefile')
    # so there we will store our data
    shapeData = driver.CreateDataSource(path)
    # this will create a corresponding layer for our data with given
    # spatial information.
    layer = shapeData.CreateLayer('places', spatialReference, ogr.wkbPoint)
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
    # removes the exsisting shapefile
    extensions = ["shp", "shx", "prj", "dbf"]
    for extension in extensions:
        command = "rm " + path + file_name + "." + extension
        os.system(command)


def read_txt(txt_file):
    with open(txt_file) as f:
        return f.readlines()


def places_to_shape():
    # files and paths
    # current file location
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    txt_file = "places.txt"

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
    remove_shape(path, txt_file[:-4])

    # store results
    store_shape(path, placeDic)


if __name__ == "__main__":
    places_to_shape()
