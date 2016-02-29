""" Process the OSM map file
    Audit and correct all values, except those corrected manually
    Create a list of dictionaries
    Store list in a JSON file

    tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import csv
import codecs
import json

INPUTFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\map_toronto2"
POSTCODEFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\canada.csv"
NOPOSTCODE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\nopcode.json"

CREATED = ["version", "changeset", "timestamp", "user", "uid"]

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^addr:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def write_nopcode(node, pretty = False):
    #file_out = NOPOSTCODE
   # file_out = "{0}_test.json".format(file_in)
    data = []
    with open("nopcode.json", "w") as fo:
       # for _, element in ET.iterparse(file_in):
        #   el = shape_element(element)
        if node:
            data.append(node)
            if pretty:
                fo.write(json.dumps(node, indent=2)+"\n")
            else:
                fo.write(json.dumps(node) + "\n")
    return


# Add external data to the dictionary. Get districts and neighbourhoods from 1st three characters of postcode in canada.csv.
def add_neighb(row):
    neighb = {}
    place_name = None
    if re.search(r'^M\d[A-Z]', row["Postalcode"]):
        print row ["Postalcode"]
        place_name = re.sub(r'\)', "", row["Place name"])
        place_name = re.split(r'[(/]\s?', place_name)
        neighb["name"] = place_name[1:]
        neighb["district"] = place_name[0]
        neighb["province"] = row["Province"]
        neighb["country"] = row["Country"]
        neighb["postalcode"] = row["Postalcode"]
        neighb["pos"] = [float(row["Longitude"]), float(row["Latitude"])]

    else:
        neighb = None

    return neighb

def process_file(file_in, pretty = False):
    file_out = "neighb.json"
    data = []

    with open(POSTCODEFILE, "r") as filein:
        reader = csv.DictReader(filein)
        with codecs.open(file_out, "w") as fo:
            for row in reader:
                el = add_neighb(row)
                if el:
                    data.append(el)
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")

    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_file(POSTCODEFILE, True)
    pprint.pprint(data)


    # assert len(data) == 76
    # pprint.pprint(data[14])
    # assert data[0] == first_entry
    # assert data[17]["name"] == "Ogdenia"
    # assert data[48]["label"] == "Hydrachnidiae"
    # assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == '__main__':
    test()