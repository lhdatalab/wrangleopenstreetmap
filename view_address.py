""" Get all addresses associated with the k attribute addr:street
    Store in a dictionary of sets based on the ending of the streetname.
    Inspect the dictionary for incorrect/invalid addresses.
    Design a plan to fix these addresses.

    tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import csv

INPUTFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\map_toronto1"

# Use to check the ending of the streetname
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Intial list of streetname endings
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Grove"]


# Find abbreviated or invalid streetname endings
def audit_street_type(street_types, street_name):
    #Get streetname ending
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        # Check if it is not in the list of valid endings
        if street_type not in expected:
            street_types[street_type].add(street_name)

    return

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Get the streetname value ( v attribute) for every addr:street (k attribute)
def audit(osmfile):
    osm_file = open(osmfile, "r")
    # Create dictionary of sets
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                # Check if k attribute = addr:street
                if is_street_name(tag):
                    # Update abbreviated or invalid streetname endings
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def update_name(name, mapping):
    get_end = name.split(" ")
    for key in mapping.keys():
        if key == get_end[-1]:
            name = re.sub(key, mapping[key], name)

    return name

def test():
    st_types = audit(INPUTFILE)
    pprint.pprint(dict(st_types))
    return

if __name__ == '__main__':
    test()