import os
import json


def read_json(file_name):
    sep = os.sep

    nodes = list()
    links = list()

    with open('..' + sep + '..' + sep + 'networks' + sep + file_name) as json_file:
        data = json.load(json_file)
        nodes = data['Nodes']
        links = data['Links']

    return nodes, links
