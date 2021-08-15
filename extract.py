"""Extract data on near-Earth objects and close approaches.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at
the command line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path='data/neos.csv'):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file with data on near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # list to store each neo row
    neos_data = []
    # read file
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        for idx, row in enumerate(reader):
            neos_data.append(row)

    neo_list = list()
    for item in neos_data:
        curr_designation = str(item.get('pdes'))
        curr_name = item.get('name') if item.get('name') != '' else None
        curr_hazardous = True if item.get('pha') == 'Y' else False

        try:
            curr_diameter = float(item.get('diameter'))
        except ValueError:
            curr_diameter = float('nan')
        neo_list.append(NearEarthObject(designation=curr_designation,
                                        name=curr_name,
                                        diameter=curr_diameter,
                                        hazardous=curr_hazardous))

    neo_list.sort(key=lambda neo_obj: neo_obj.designation)

    return neo_list


def load_approaches(cad_json_path='data/cad.json'):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file with close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, 'r') as infile:
        ca_dict = json.load(infile)

    # list of all close approaches
    ca_data_list = ca_dict['data']
    ca_list = list()

    for item in ca_data_list:
        # get designation
        curr_designation = str(item[0])
        # get time
        curr_time = item[3]
        # get distance
        curr_distance = item[4]
        # get velocity
        curr_velocity = item[7]

        ca_list.append(CloseApproach(curr_time,
                                     designation=curr_designation,
                                     distance=curr_distance,
                                     velocity=curr_velocity))
    ca_list.sort(key=lambda ca_obj: ca_obj._designation)
    return ca_list
