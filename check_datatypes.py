""" Check if lat and lon attributes are valid
    - can it be converted to a number
    - does it lie within the bounding box
    - If it falls outside of  the bounding box
        o get the tag subelement and associated k, v attributes
        o write all data to a list of dictionaries and save to a csv file
        o Examine the file and determine if to keep these nodes or if to discard them

    tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]

"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import csv

INPUTFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\map_toronto1"
OUTFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\lat_long.csv"

# Check how far the lat and lon fall outside of the bounding box coordinates
def getcoord_diff(coord, min, max):
    diff = 0.0
    if abs(coord - min) < abs(coord-max):
        diff = abs(coord-min)
    else:
        diff = abs(coord-max)
    return diff

# Save any lat/lon errors ina dictionary
def make_dict(error, elem, lat_diff, lon_diff):
    latlon_dict = {}
    latlon_dict["error"] = error
    latlon_dict["type"] = elem.tag
    latlon_dict["lat"] = elem.attrib["lat"]
    latlon_dict["lon"] = elem.attrib["lon"]
    latlon_dict["lat_diff"] = lat_diff
    latlon_dict["lon_diff"] = lon_diff
    latlon_dict["tag"] = get_tag(elem)

    return latlon_dict

# Get all <tag> subelements and attributes in a <node>/<way> tag
def get_tag(elem):
    tags = []
    for subtag in elem.findall("*"):
            # Get only subelements or children of root tag
                if subtag.tag == "tag":
                    tags.append(subtag.attrib)
    return tags

# Write lat/lon data errors to file
def writefile(filename, data):
    keys = data[0].keys()
    with open(filename, "w") as fo:
        writer = csv.DictWriter(fo, delimiter=",", lineterminator="\n", fieldnames = keys)
        writer.writeheader()
        #for row in data:
        writer.writerows(data)
    return

def get_fieldtype(filename):
    data_coord = []
    count_range = 0
    count_num = 0
    lat_diff = 0.0
    lon_diff = 0.0
    latlon = {}
    data_error = []

    for event, elem in ET.iterparse(filename):
        coord = elem.attrib
        # Check if tag/element has a lat or lon attribute. If true check if it is a valid float value
        # or if it is out of bounding box range
        if "lat" in coord or "lon" in coord:
            if not (float(coord["lat"]) or float(coord["lon"])):
                error = "Coordinates are not a number"
                #print error + ":", coord["lat"], coord["lon"]
                data_coord.append(coord["lat"] + " " + coord["lon"])
                count_num += 1

                latlon = make_dict(error, elem, lat_diff, lon_diff)
                data_error.append(latlon)

            elif not (float(coord["lat"]) >= 43.6234 and float(coord["lat"]) <= 43.7451) or \
               not (float(coord["lon"]) >= -79.5681 and float(coord["lon"]) <= -79.2815):

                # Check how far a point lies outside of the bounding box
                lat_diff = getcoord_diff(float(coord["lat"]), 43.6234, 43.7451)
                lon_diff = getcoord_diff(float(coord["lon"]), -79.5681, -79.2815)
                error = "Coordinates out of range"
                data_coord.append(coord["lat"] + " " + coord["lon"])
                count_range += 1

                latlon = make_dict(error, elem, lat_diff, lon_diff)
                data_error.append(latlon)

    if not data_coord:
        print "Latitude and Longitude values are valid"

    print "{} lat/lon are out of range: ".format(count_range)
    print "{} lat/lon are not a number: ".format(count_num)

    writefile(OUTFILE, data_error)
    return data_coord

def test():
    data = get_fieldtype(INPUTFILE)
    return


if __name__ == "__main__":
    test()