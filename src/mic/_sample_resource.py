from mic._utils import ask_simple_value

mapping_sample_resource = {
    'URL': 'value'
}

RESOURCE = "Input"


def add_sample_resource(description):
    item = {"description": description, "label": description}
    for key in mapping_sample_resource:
        value = ask_simple_value(key, RESOURCE)
        item[mapping_sample_resource[key]] = value
    return item
