""" Audit file initially by checking for number of nodes, ways and relations and other tags
    Also check for the tag structure
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import csv

INPUTFILE = "map_toronto1"


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
    child_data = get_childtags(INPUTFILE)
    pprint.pprint(child_data)


if __name__ == "__main__":
    test()