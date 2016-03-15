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

# Use to check the last and second last word street name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Grove", 'Vista', 'Ridge', 'Hills', 'Carmeloway', 'Wishbone',
            'West', 'Linkway', 'Keanegate', 'Heights', 'Golfway', 'Wood', 'Cabotway', 'Hill', 'Way',
            'Islands', 'Gate', 'Circle', 'East', 'Pathway', 'Palisades', 'Roadway', 'Woodway', 'North',
            'Manor', 'Quay', 'Floor', 'Park', 'Cove', 'Queensway', 'Esplanade', 'Kingsway', 'Front', 'Path',
            'Ames', 'Terrace', 'Lawn', 'Warden', 'Plaza', 'Marinoway', 'Westway', 'Keep', 'Mall', 'Myrtleway',
            'Green', 'Glenway', 'Lanes', 'Mews', 'Elmway', 'Gardens', 'South', 'View', 'Outlook', 'Point',
            'Appleway', 'Wynd', 'Robertoway', 'Valleyway', 'Crescent', 'Close', 'Elms', 'Dundas', 'Tremont']

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
            "Dr": "Drive",
            "Dr.":"Drive",
            "E": "East",
            "E.": "East",
            "W": "West",
            "W.": "West",
            "Grv": "Grove",
            "Grv.": "Grove",
            "Hts": "Heights",
            "Hts.": "Heights",
            }

# Change the the first word in street names using the first_word dictionary.
first_word = {"1st": "First",
              "4": "Four",
              "Chole": "Cole"
              }

# Edit a few of the entries manually. The one off type errors. E.g. Terace, Tremont, San Vitoway, Dovercourt, Dundas etc.

flag = ["Terace", "Tremont", "Vitoway", "Millway", "Dovercourt", "Dundas", "Jarvis", "Italia", "Hts", \
        "Grv", "5700", "E", "W"],

### Use this array as if attr in CREATED node["attr"] = ....
CREATED = ["version", "changeset", "timestamp", "user", "uid"]

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^addr:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Audit and correct street names
def audit_street_name(street_name):
    street_name = street_name.strip()
    # Capitalize the first letter of every word in streetname
    for word in street_name.split():
        if word != "and" and (not word[0].isupper()or word.isupper()):
            new_word = word.capitalize()
            street_name = street_name.replace(word, new_word)

    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        # Check if street name does not have a valid ending
        if street_type not in expected:
            street_name = update_name(street_name, mapping)

    # Get second last word in street name if it exists. If it is abbreviated add to street_types
    getword = street_name.split()
    try:
        if getword[-2] in mapping.keys():
            street_name = update_name(street_name, mapping)
    except:
        pass

    # Standardized street names starting with "St", "St." or "Saint"
    # Get first word in street name. If it is "St." or "Saint" add to street_types
    if getword[0] == "St." or getword[0] == "Saint":
        street_name = update_name(street_name, mapping)

    # Standardized mispelt words or street names that begin with a digit
    if getword[0] in first_word.keys():
        street_name = update_name(street_name, mapping)

    return street_name


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# Correct street names
def update_name(name, mapping):
    # Strip whitespaces and apostrophesif name.find("'") != -1:
    name = name.replace("'", "")
    name = name.lstrip()
    word = name.split(" ")
    length = len(word)
    for key in mapping.keys():
        if key == word[-1]:
             name = " ".join(word[:(length-1)]) + " " + mapping[key]
        try:
            if key == word[-2]:
                name = " ".join(word[:(length-2)]) + " " + mapping[key] + " " + word[(length-1)]
        except:
            pass

    if word[0] == "St." or word[0] == "Saint":
        name = "St " + " ".join(word[1:])

    if word[0] in first_word.keys():
        name = first_word[word[0]] + " ".join(word[1:])

    return name

# Audit postal codes. Add a whitespace after the first three characters and change to uppercase
def audit_postcode(pcode):
    if pcode.find(" ") != -1:
        pcode = " ".join([pcode[0:3], pcode[3:5]])
    pcode = pcode.upper()
    return pcode

# Change any any address type reference in "name" attribute into a list
def change_to_list(name):
    if re.search(r'[,;/&]', name):
        # Remove all references to distance in m and km
        name = re.sub(r'\s[0-9]+\.?[0-9]?\s?k?m\s?', "", name)
        # Create list of addresses by splitting on ,;/ or &
        name = re.split(r'\s?[,;/&]\s?',name)
    else:
        name = [name]
    return name


# Add external data to the dictionary. Get districts and neighbourhoods from 1st three characters of postcode in canada.csv.
def add_neighb(pcode):
    neighb = {}
    place_name = None
    with open(POSTCODEFILE, "r") as filein:
        reader = csv.DictReader(filein)
        for row in reader:
            if row["Postalcode"] == pcode[0:3]:
                place_name = re.sub(r'\)', "", row["Place name"])
                place_name = re.split(r'[(/]\s?', place_name)
                neighb["district"] = place_name[0]
                neighb["name"] = place_name[1:]
            neighb["pos"] = [float(row["Longitude"]), float(row["Latitude"])]
            neighb["postalcode"] = row["Postalcode"]

    return neighb

# Process all attributes starting with 'addr:'
def process_address(tag):
    addr_key = []
    addr_val = []
    address = tag.attrib["k"].split(":")
    addr_key.append(address[-1])

    # Process street names
    if address[-1] == "street":
        street_name = audit_street_name(tag.attrib["v"])
        if re.search(r'[;/&]', street_name):
            street_name = street_name.split(";")
        addr_val.append(street_name)

    # Process city field. E.g. "city of Toronto", remove "city of"
    elif address[-1] == "city" and re.search(r'^city of', tag.attrib["v"]):
            city = tag.attrib["v"].split()
            addr_val.append(" ".join(city[2:]))

    # Process postal code
    elif address[-1] == "postcode":
        pcode  = audit_postcode(tag.attrib["v"])
        addr_val.append(pcode)
    else:
        addr_val.append(tag.attrib["v"])

    return addr_key, addr_val

# Create a nested dictionary
def create_dict(tag, node):

    n_dict = {}
    get_keys = tag.attrib["k"].split(":")
    numkeys = len(get_keys)
    # Minimum number of keys for nested dictionary
    minkeys = 3
    # First two keys are joined by "_" to create the first key. All other keys are nested.
    first_key = get_keys[0] + "_" + get_keys[1]
    node[first_key] = {}
    n_dict = node[first_key]
    for attr in get_keys[2:]:
        if minkeys < numkeys:
            n_dict = n_dict.setdefault(attr, {})
        else:
            n_dict[attr] = tag.attrib["v"]

        minkeys += 1
    return n_dict

# Change XML nodes to JSON documents
def shape_element(element):
    node = {}
    add_ndref = []
    addr_key = []
    addr_val = []
    nested_dict = {}
    if element.tag == "node" or element.tag == "way" :

        # Check  if postal code is outside of Toronto. do for nodes only.
        # toronto = address_loc(element)
        # if (toronto and element.tag == "node") or element.tag == "way":
        node["type"] = element.tag
        node["created"] = {}
        for attr in element.attrib:
            if attr == "id":
                node["id"] = element.attrib["id"]

            if "lat" in element.attrib and "lon" in element.attrib:
                node["pos"] = [float(element.attrib["lon"]), float(element.attrib["lat"])]

            if attr in CREATED:
                node["created"][attr] = element.attrib[attr]

        # Find and process <tag> sub-elements
        if element.findall("tag"):
            for tag in element.iter("tag"):
                if not problemchars.search(tag.attrib["k"]):
                    # Find if k attribute starts with 'addr:'
                    if lower_colon.search(tag.attrib["k"]):
                        # Process all values for the address key
                        (addr_key, addr_val) = process_address(tag)
                        # Create address nested directory in node dictionary
                        if len(addr_key) > 0 and len(addr_val) > 0:
                            node["address"] = dict(zip(addr_key, addr_val))
                            try:
                                node["neighborhood"] = add_neighb(node["address"]["postcode"])
                            except:
                                pass

                    # Find attributes with only one ':', but do not start with 'addr:'. Change ':' to '_'
                    elif not re.match(r'(addr)', tag.attrib["k"]) and (re.split(r':', tag.attrib["k"])) == 2:
                        newkey = re.sub(":", "_", tag.attrib["k"])
                        node[newkey] = tag.attrib["v"]

                    # Find k attributes with multiple ':' and create a nested directory
                    # Split the k attribute to get the first two fields as the root key
                    # The first two fields are joined by the "_" character
                    elif len(tag.attrib["k"].split(":")) > 2:
                        nested_dict = create_dict(tag, node)

                    # Process all other first level k attributes
                    elif lower.match(tag.attrib["k"]):
                        # Special processing for name attribute in <node> or <way> tags
                        # If highway or guidepost tags present treat name as an address list
                        try:
                            if tag.attrib["k"] == "name" and (node["type"] == "node" or node["type"] == "way") and \
                                    (node["highway"] or node["guidepost"]):
                                name_list = change_to_list(tag.attrib["v"])
                                for index, name in enumerate(name_list):
                                    name_list[index] = update_name(name, mapping)
                                node["name"] = name_list
                        except KeyError:
                            pass
                        try:
                            if tag.attrib["k"] == "postal_code" and not (node["neighborhood"]):
                                node["postal_code"] = audit_postcode(tag.attrib["v"])
                                node["neighborhood"] = add_neighb(node["postal_code"])
                        except KeyError:
                            pass
                        else:
                            node[tag.attrib["k"]] = tag.attrib["v"]

        # Find and process <nd> sub-elements
        if element.findall("nd"):
            for nd in element.iter("nd"):
                add_ndref.append(nd.attrib["ref"])

            node["node_refs"] = add_ndref

        return node

    else:
        return None


# Save XML file as JSON document
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")

    return data

def test():
    data = process_map(INPUTFILE, True)
    pprint.pprint(data[0:10])
    pprint.pprint(data[1000:1010])

if __name__ == '__main__':
    test()