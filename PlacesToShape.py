## CREATED BY:
## Gert Sterenborg; gertsterenborg@gmail.com
## 21-01-2015

##imports:
import os
import json
import urllib2
import osgeo.ogr, osgeo.osr

def getLatLng(place):
    ## Fetches coordinates from the google api
    url = "http://maps.googleapis.com/maps/api/geocode/json?address="+place
    response = urllib2.urlopen(url)
    jsonF = json.loads(response.read())
    if jsonF['status'] == "OK":
        lat = jsonF['results'][0]['geometry']['location']['lat']
        lng = jsonF['results'][0]['geometry']['location']['lng']
        return lat,lng

def storeShp(placeDic):
    ## current file location
    path = os.path.dirname(os.path.realpath(__file__))+"/"
    ## remove shapefile
    removeShp(path,'places')
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.ImportFromEPSG(4326) ##WGS84 degrees coordinates
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile') # will select the driver foir our shp-file creation.
    shapeData = driver.CreateDataSource(path) #so there we will store our data
    layer = shapeData.CreateLayer('places', spatialReference, osgeo.ogr.wkbPoint) #this will create a corresponding layer for our data with given spatial information.
    layer_defn = layer.GetLayerDefn() # gets parameters of the current shapefile
    new_field = osgeo.ogr.FieldDefn('PLACE', osgeo.ogr.OFTString)
    layer.CreateField(new_field)
    point = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
    i = 0
    for place in placeDic:
        point.AddPoint(placeDic[place]['lng'],placeDic[place]['lat']) #create a new point at given ccordinates
        featureIndex = i
        feature = osgeo.ogr.Feature(layer_defn)
        feature.SetGeometry(point)
        feature.SetFID(featureIndex)
        j = feature.GetFieldIndex("PLACE")
        feature.SetField(j, place)
        layer.CreateFeature(feature)
        i+= 1
    shapeData.Destroy() #lets close the shapefile

def removeShp(path,fileName):
    ## removes the exsisting shapefile
    extensions = ["shp","shx","prj","dbf"]
    for extension in extensions:
        command = "rm "+path+fileName+"."+extension
        os.system(command)

if __name__ == "__main__":
    placeDic = {} ## dictionary where all the coordinates and places will be stored in
    with open("places.txt") as f:
        for line in f:
            lineSplit = line.split(',')
            for place in lineSplit:
                lat,lng = getLatLng(place.strip())
                placeDic[place.strip()] = {
                    'lat':lat,
                    'lng':lng}
    storeShp(placeDic)
    try: ## show the result in qgis
        os.system("qgis places.shp")
    except:
        pass

                
