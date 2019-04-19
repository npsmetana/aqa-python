import os
import xml.etree.ElementTree as ET
import copy
import json
import io

structure_items = ("/PERSON",
                   "/PERSON/FIRST_NAME",
                   "/PERSON/LAST_NAME",
                   "/PERSON/YEAR_OF_BIRTH",
                   "/PERSON/MONTH_OF_BIRTH",
                   "/PERSON/DAY_OF_BIRTH",
                   "/PERSON/COMPANY",
                   "/PERSON/PROJECT",
                   "/PERSON/ROLE",
                   "/PERSON/ROOM",
                   "/PERSON/HOBBY")

update_data = {"FIRST_NAME": "Yurii",
               "LAST_NAME": "Gagarin",
               "YEAR_OF_BIRTH": "1934",
               "MONTH_OF_BIRTH": "Mar",
               "DAY_OF_BIRTH": "09",
               "COMPANY": "Cosmonaut Training Center",
               "PROJECT": "Vostok-1",
               "ROLE": "Cosmonaut",
               "ROOM": "Zviozdnyi gorodok",
               "HOBBY": "Water skiing"}

search_pattern = "YOUR"


def is_file_exist(file_name):
    return os.path.isfile(file_name)


def clean_up(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)


def check_xml_structure(file_name):
    tree = ET.parse(file_name)

    num_items = len(tree.findall(structure_items[0]))
    for i in range(1, len(structure_items)):
        if num_items != len(tree.findall(structure_items[i])):
            return False

    return True


def import_xml_to_data(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()

    persons = list()
    for person in root:
        attributes = dict()
        for attribute in person:
            attributes.update({attribute.tag: attribute.text})
        persons.append(attributes)

    return {root.tag: {root[0].tag: persons}}


def replace_data(data):
    data_upd = copy.deepcopy(data)
    for person in data_upd["PERSONS"]["PERSON"]:
        for attribute in person.keys():
            if search_pattern in person[attribute]:
                person[attribute] = update_data[attribute]

    return data_upd


def is_everything_replaced(data):
    for person in data["PERSONS"]["PERSON"]:
        for attribute in person.keys():
            if search_pattern in person[attribute]:
                return False

    return True


def save_data_to_json_file(file_name, data):
    with io.open(file_name, 'w') as write_file:
        data_str = json.dumps(data, indent=4, separators=(',', ': '))
        write_file.write(data_str)


def is_data_saved_correctly(file_name, data):
    with open(file_name) as data_file:
        data_loaded = json.load(data_file)
    return sorted(data) == sorted(data_loaded)
