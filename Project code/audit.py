""" Audit file initially by checking for number of nodes, ways and relations and other tags
    Also check for the tag structure
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import csv
#import sys, string, os
#import sys, subprocess

INPUTFILE = "map_toronto1"

# result = os.system(sys.argv[1], sys.argv[2])
# result = subprocess.check_output(sys.argv[1], sys.argv[2])

# Audit tags in toronto.osm file
# def check_tags(filename):
#     data = {}
#     numtags = 0
#     for event, elem in ET.iterparse(filename):
#             if elem.tag in data.keys():
#                 data[elem.tag] = data[elem.tag] + 1
#             else:
#                 data[elem.tag] = 1
#             numtags = numtags + 1
#     data["total"] = numtags
#     return data

# Get relationship between child tags and parent tags
def get_childtags(filename):
    tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]
    root_tag = {}
    for tag in tags:
        root_tag[tag] = set()
    # For each root tag find all sub tags
    for event, elem in ET.iterparse(filename):
        # Check if root tag has no subelements
        if elem.tag == "bounds":
            print "bounds = {}".format(elem.attrib)
        if elem.findall("*") == []:
            root_tag[elem.tag] |= set(["None"])
        else:
            for subtag in elem.findall("*"):
            # Get only subelements or children of root tag
                if subtag.tag in tags:
                    root_tag[elem.tag] |= set([subtag.tag])
    return root_tag

# Print results of tag Audit
def test():
   # filename = csv.DictReader(open(INPUTFILE, "r"))
   # data = check_tags(INPUTFILE)
    child_data = get_childtags(INPUTFILE)
    pprint.pprint(child_data)


if __name__ == "__main__":
    test()