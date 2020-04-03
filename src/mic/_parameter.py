from mic._utils import first_line_new, ask_simple_value

RESOURCE = "Parameter"

mapping_parameter = {
    'Name': 'label',
    'Value': 'hasFixedValue',
}

def add_parameter(i):
    first_line_new(RESOURCE, i+1)
    item = {"position": [i + 1]}
    for key in mapping_parameter:
        value = ask_simple_value(key, RESOURCE)
        item[mapping_parameter[key]] = value
    return item
