""" Based on the results from view_address.py
    - Add to the address endings in expected list with additional valid addresses for Toronto.
        o Save a new list with all valid address endings to a csv file
    - Convert all lowercase addresses to capitalize first letter
    - After capitalizing the first letter it was noticed that some addresses start with a number. Those that are part
        of the street address change to the word, e.g. 1st = First. Those that are not par of the street address
        store in the addr:building corresponding  v attribute
    - All other endings that are not in the new valid names list store add to the mapping directory

    tags = ["bounds", "member", "meta", "nd", "node", "note", "osm", "relation", "tag", "way"]
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import csv

INPUTFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\map_toronto1"
OUTFILE = "C:\Mathlab\CV\Courses\DAND\P3 - Data Wrangling with MongoDB\P3 Project\OSM Data\\toronto_canada.osm\\valid_address.csv"
# Use to check the ending of the streetname
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Grove"]

flag = ["Terace", "Tremont", "Vitoway", "Millway", "Dovercourt", "Dundas", "Jarvis", "Italia", "Hts", "Grv", \
        "5700", "Dixon", "E", "E.", "W", "W."]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Road.": "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Ct": "Court",
            "Ct.": "Court",
            }

# Write valid address endings to file
def writefile(outfile, data):
    data = sorted(list(data))
    with open(outfile, "w") as fo:
        writer = csv.writer(fo, delimiter=",", quotechar="'", lineterminator="\n")
        writer.writerow(["Valid address endings"])
        for row in data:
            writer.writerow([row])
    return

def get_editnodes():


def audit_street_type(street_types, street_name, valid_name):
    street_name = street_name.strip()
    # Capitalize the first letter of every word in streetname
    for word in street_name.split():
        if word != "and" and (not word[0].isupper()or word.isupper()):
            new_word = word.capitalize()
            street_name = street_name.replace(word, new_word)
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        # Add to invalid endings if the streetname is not in expected or mapping, but in flag lists
        if street_type not in expected and street_type in flag or street_type in mapping.keys():
            street_types[street_type].add(street_name)
        # Add to the list of valid streetname endings. This will be used as an automated way to update expected list
        elif street_type not in expected and street_type not in flag:
            valid_name = valid_name.add(street_type)
    return

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    valid_name = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'], valid_name)
    osm_file.close()
    return (street_types, valid_name)


def update_name(name, mapping):
    get_end = name.split(" ")
    for key in mapping.keys():
        if key == get_end[-1]:
            name = re.sub(key, mapping[key], name)

    return name

def test():
    (st_types, vd_names) = audit(INPUTFILE)
    writefile(OUTFILE, vd_names)
    print "Invalid address endings"
    pprint.pprint(dict(st_types))
    print "Valid address ending"
    print vd_names

if __name__ == '__main__':
    test()