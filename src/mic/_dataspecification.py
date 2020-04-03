from mic._sample_resource import add_sample_resource
from mic._utils import first_line_new, ask_simple_value

RESOURCE_INPUT = "Input"
RESOURCE_OUTPUT = "Output"


mapping_dataset_specification = {
    'Name': 'label',
    'Format': 'hasFormat',
}

def add_input(i):
    first_line_new(RESOURCE_INPUT, i+1)
    item = {"position": [i + 1]}
    for key in mapping_dataset_specification:
        value = ask_simple_value(key, RESOURCE_INPUT)
        item[mapping_dataset_specification[key]] = value
    item["hasFixedResource"] = [add_sample_resource(item["label"])]
    return item


def add_output(i):
    first_line_new(RESOURCE_OUTPUT, i+1)
    item = {"position": [i + 1]}
    for key in mapping_dataset_specification:
        value = ask_simple_value(key, RESOURCE_OUTPUT)
        item[mapping_dataset_specification[key]] = value
    return item
