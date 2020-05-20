import enum

import click
from modelcatalog import Model, DatasetSpecification, SoftwareVersion, Parameter, Person, SampleResource, \
    ModelConfiguration

SELECT = 'select'


def get_definition(mapping, variable_name):
    if "definition" in mapping:
        click.echo("Definition: {}".format(mapping['definition']))


def is_complex(mapping, variable):
    return mapping[variable]['complex']


def init_complex(resource, _property):
    builtin_types = ["int", "str", "bool", "float"]
    for b in builtin_types:
        if b in resource.openapi_types[_property]:
            return False
    return True


def get_prop_mapping(mapping, variable_selected):
    return mapping[variable_selected]["id"]


def get_type_mapping(mapping):
    if "type" in mapping:
        return mapping["type"]
    return None


def get_complex(mapping, resource):
    for key, _property in mapping.items():
        mapping[key]["complex"] = init_complex(resource, _property['id'])


def select_enable(mapping):
    if SELECT in mapping and mapping[SELECT]:
        return mapping[SELECT]
    return False


class Metadata_types(enum.Enum):
    Float = 1
    Url = 2


mapping_model = {
    'Name': {'id': 'label', 'definition': 'Name of the model', 'required': True},
    'Description': {"id": 'description', 'definition': 'Description of the model', 'required': False},
    'Keywords': {"id": 'keywords', 'definition': 'Keywords that can be used to describe the model', 'required': False},
    'Website': {"id": 'website', 'definition': 'Website where more information about the model can be found',
                'required': False, 'type': Metadata_types.Url},
    'Documentation': {"id": 'has_documentation',
                      'definition': 'URL where additional documentation of the model can be found', 'required': False},
    'Versions': {"id": 'has_version', 'definition': 'Available versions of a particular model', 'required': False},
    'Author': {"id": 'author', 'definition': 'Person(s) who created the model', 'required': False, SELECT: True},
    'Contributor': {"id": 'contributor', 'definition': 'Person(s) who contributed to the development of the model',
                    'required': False, SELECT: True},
    'Contact person': {"id": 'has_contact_person', 'definition': 'Contact person responsible for maintaining the model',
                       'required': False, SELECT: True},
    'License': {"id": 'license', 'definition': 'License associated to the model (e.g., CC-BY)', 'required': False},
    'Category': {"id": 'has_model_category', 'definition': 'Category associated with the model (e.g., Hydrology)',
                 'required': False},
    'Creation date': {"id": 'date_created', 'definition': 'Date when the model was created', 'required': False},
    'Assumptions': {"id": 'has_assumption', 'definition': 'Assumptions to be considered when using the model',
                    'required': False},
    # 'Publisher': {"id": 'publisher', 'definition': 'Organization responsible for publishing the model', 'required': False},
    'Download URL': {"id": 'has_download_url', 'definition': 'URL available for downloading the model',
                     'required': False, 'type': Metadata_types.Url},
    'Logo': {"id": 'logo', 'definition': 'URL to an image that can be used to identify this model', 'required': False},
    'Purpose': {"id": 'has_purpose',
                'definition': 'Objective or main functionality that can be achieved by running this model',
                'required': False},
    'Citation': {"id": 'citation', 'definition': 'Reference publication for citing a model', 'required': False},
    # publisher and logo commented until we define Organization and Image
}
mapping_software_version = {
    'Name': {"id": 'label'},
    'Description': {"id": 'description'},
    'Version number': {"id": 'has_version_id'},
    'Model Configurations': {"id": 'has_configuration', SELECT: False},
}

mapping_dataset_specification = {
    'Name': {'id': 'label', 'definition': 'Name of the input/output', 'required': True},
    'Description': {"id": 'description', 'definition': 'Description of the input/output', 'required': False},
    'Format': {"id": 'has_format', 'definition': 'Format of the file (e.g., CSV, tiff, nc, etc.)', 'required': False},
}
# mapping_parameter = {
#    'Name': {"id": 'label'},
#    'Value': {"id": 'has_fixed_value'},
# }

mapping_parameter = {
    'Name': {'id': 'label', 'definition': 'Name of the parameter', 'required': True},
    'Data type': {'id': 'has_data_type', 'definition': 'Tpe of the parameter. Accepted values are string, integer, '
                                                       'float or boolean', 'required': True},
    'Value': {'id': 'has_fixed_value', 'definition': 'Value of this parameter in this setup. Setting up a value will '
                                                     'make the parameter non-editable on execution',
              'required': False, 'type': Metadata_types.Float},
    'Default Value': {'id': 'has_default_value', 'definition': 'Default value of the parameter', 'required': False,
                      'type': Metadata_types.Float},
    'Minimum accepted value': {'id': 'has_minimum_accepted_value', 'definition': 'Minimum value the parameter can have',
                               'required': False, 'type': Metadata_types.Float},
    'Maximum accepted value': {'id': 'has_maximum_accepted_value', 'definition': 'Maximum value the parameter can '
                                                                                 'have ', 'required': False,
                               'type': Metadata_types.Float},
}
mapping_image = {
    'Name': {'id': 'label', 'definition': 'Name of the image', 'required': True, 'complex': False},
    'Description': {"id": 'description', 'definition': 'Description of the image', 'required': False, 'complex': False},
    'URL': {"id": 'value', 'definition': 'URL of the image', 'required': False, 'complex': False,
            'type': Metadata_types.Url},
    'Source': {"id": 'had_primary_source',
               'definition': 'URL of the website where the logo comes from (e.g., https://wikidata.org/)',
               'required': False, 'complex': False},
}
mapping_model_configuration = {
    'Name': {'id': 'label',
             'definition': 'Name of the model configuration',
             'required': True},
    'Description': {"id": 'description',
                    'definition': 'Description of the model configuration',
                    'required': False
                    },
    'Keywords': {"id": 'keywords', 'definition': 'Keywords that can be used to describe the model configuration',
                 'required': False},
    'Documentation': {"id": 'has_documentation',
                      'definition': 'URL where additional documentation of the model configuration can be found',
                      'required': False},
    'Author': {"id": 'author', 'definition': 'Person(s) who created the model configuration', 'required': False,
               SELECT: True},
    'Contributor': {"id": 'contributor',
                    'definition': 'Person(s) who contributed to the development of the model configuration',
                    'required': False, SELECT: True},
    # 'License': {"id": 'license', 'definition': 'License associated to the model (e.g., CC-BY)', 'required': False},
    'Category': {"id": 'has_model_category',
                 'definition': 'Category associated with the model configuration (e.g., Hydrology)',
                 'required': False},
    'Creation date': {"id": 'date_created', 'definition': 'Date when the model configuration was created',
                      'required': False},
    'Assumptions': {"id": 'has_assumption',
                    'definition': 'Assumptions to be considered when using the model configuration',
                    'required': False},
    'Inputs': {"id": 'has_input',
               'definition': 'Input files used in the model configuration',
               'required': False,
               SELECT: False},
    'Outputs': {"id": 'has_output',
                'definition': 'Output files produced by the model configuration',
                'required': False,
                SELECT: True},
    'Parameters': {"id": 'has_parameter',
                   'definition': 'Parameters (i.e., numerical values, strings or booleans) to required by the model '
                                 'configuration',
                   'required': False,
                   SELECT: False},
    'Executable URL': {"id": 'has_component_location',
                       'definition': 'URL where the executable for this configuration can be found',
                       'required': False},
}
mapping_person = {
    'Name': {'id': 'label', 'definition': 'Name of the person', 'required': True},
    'email': {"id": 'email', 'definition': 'Email of the person', 'required': False},
    'website': {"id": 'website', 'definition': 'Website of the person', 'required': False, 'type': Metadata_types.Url},
}
mapping_sample_resource = {
    'URL': {"id": 'value'}
}

get_complex(mapping_model, Model)
get_complex(mapping_model_configuration, ModelConfiguration)
get_complex(mapping_software_version, SoftwareVersion)
get_complex(mapping_dataset_specification, DatasetSpecification)
get_complex(mapping_parameter, Parameter)
get_complex(mapping_person, Person)
get_complex(mapping_sample_resource, SampleResource)
# In Image URL and source are mapped as complex, but they are not
# get_complex(mapping_image, Image)
