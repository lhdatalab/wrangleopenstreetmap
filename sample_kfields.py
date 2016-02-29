""" Get k attributes with 2 or more ":". Save in  a list.
    Place in a set and then save in a json or a csv file.

    tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]

"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import csv
import geocoder

INPUTFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\map_toronto1"
OUTFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\k_values.csv"
#tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]

lower = re.compile(r'^([a-z]|_)*$')
# lower_colon = re.compile(r'^addr:([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Write k attributes to a csv file
def writefile(filename, data):
    #keys = data[0].keys()
    data = sorted(list(data))
    with open(filename, "w") as fo:
        writer = csv.writer(fo, delimiter=",", quotechar="'", lineterminator="\n")
        writer.writerow(["<tag> k attributes"])
        for row in data:
            print [row]
            writer.writerow([row])
    return

# Lots of k,v pairs. Get a list of all k values in the OSM file to determine how to process them
def get_knames(elem, k_attrib):
    #k_attrib = set()
    #for event, elem in ET.iterparse(filename):
     #   if elem.tag == "tag":
    k_attrib |= set([elem.attrib.get("k")])

    #writefile(OUTFILE, k_attrib)
    #print "TEST2"
    return k_attrib

def key_type(element, keys, probchar_fields):

   # if element.tag == "tag":
        # YOUR CODE HERE
     #   knames = set()
    attr = element.attrib['k']
    if lower.search(attr):
        keys["lower"] = keys["lower"] + 1
    elif lower_colon.search(attr):
        keys["lower_colon"] += 1
    elif problemchars.search(attr):
        keys["problemchars"] += 1
        probchar_fields.append(attr)
    else:
        keys["other"] += 1
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    probchars_fields = []
    knames = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "tag":
            keys = key_type(element, keys, probchars_fields)
            knames = get_knames(element, knames)

   # writefile(OUTFILE, knames)
    print probchars_fields
    return keys



def test():
    #get_codes(INPUTFILE)
    data = process_map(INPUTFILE)
    pprint.pprint(data)

if __name__ == "__main__":
    test()