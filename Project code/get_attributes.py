""" Get list of attributes found in each tag
    tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import csv

INPUTFILE = "map_toronto1"
tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]

# Get attributes of all tags
# This will give some indication of the the best way to structure the JSON documents
# def sample_file(filename):
#     data ={}
#     count = 0
#     for event, elem in ET.iterparse(filename):
#         if elem.tag == "tag" and elem.attrib["k"].startswith("addr"):
#             if count < 200:
#                 print elem.tag, elem.attrib
#                 count += 1
#     return data

def get_attrs(filename):
    data ={}
    for tag in tags:
        data[tag] = set()
    for event, elem in ET.iterparse(filename):
        data[elem.tag] |= set(elem.attrib)
    return data


def test():
   # filename = csv.DictReader(open(INPUTFILE, "r"))
   # data = check_tags(INPUTFILE)
    data = get_attrs(INPUTFILE)
    pprint.pprint(data)


if __name__ == "__main__":
    test()