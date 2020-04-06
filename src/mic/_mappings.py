from mic._utils import get_complex
from modelcatalog import Model, DatasetSpecification, SoftwareVersion, Parameter, Person, SampleResource

SELECT = 'select'

mapping_model = {
    'Name': {'id': 'label', 'definition': 'Name of the model', 'required': True},
    'Description': {"id": 'description', 'definition': 'Description of the model', 'required': False},
    'Keywords': {"id": 'keywords', 'definition': 'Keywords that can be used to describe the model', 'required': False},
    'Website': {"id": 'website', 'definition': 'Website where more information about the model can be found', 'required': False},
    'Documentation': {"id": 'has_documentation', 'definition': 'URL where additional documentation of the model can be found', 'required': False},
    'Versions': {"id": 'has_version', 'definition': 'Available versions of a particular model', 'required': False},
    'Author': {"id": 'author', 'definition': 'Person(s) who created the model', 'required': False, SELECT: True},
    'Contributor': {"id": 'contributor', 'definition': 'Person(s) who contributed to the development of the model', 'required': False},
    'Contact person': {"id": 'has_contact_person', 'definition': 'Contact person responsible for maintaining the model', 'required': False},
    'License': {"id": 'license', 'definition': 'License associated to the model (e.g., CC-BY)', 'required': False},
    'Category': {"id": 'has_model_category', 'definition': 'Category associated with the model (e.g., Hydrology)', 'required': False},
    'Creation date': {"id": 'date_created', 'definition': 'Date when the model was created', 'required': False},
    'Assumptions': {"id": 'has_assumption', 'definition': 'Assumptions to be considered when using the model', 'required': False},
    # 'Publisher': {"id": 'publisher', 'definition': 'Organization responsible for publishing the model', 'required': False},
    'Download URL': {"id": 'has_download_url', 'definition': 'URL available for downloading the model', 'required': False},
    #'Logo': {"id": 'logo', 'definition': 'URL to an image that can be used to identify this model', 'required': False},
    'Purpose': {"id": 'has_purpose', 'definition': 'Objective or main functionality that can be achieved by running this model', 'required': False},
    'Citation': {"id": 'citation', 'definition': 'Reference publication for citing a model', 'required': False},
    #publisher and logo commented until we define organization and Image
}
mapping_model_version = {
    'Name': {"id": 'label'},
    'Description': {"id": 'description'},
    'Version': {"id": 'has_version_id'},
}
mapping_dataset_specification = {
    'Name': {"id": 'label'},
    'Format': {"id": 'has_format'},
}
#mapping_parameter = {
#    'Name': {"id": 'label'},
#    'Value': {"id": 'has_fixed_value'},
#}

mapping_parameter = {
    'Name': {'id': 'label', 'definition': 'Name of the parameter', 'required': True},
    'Data type': {'id': 'has_data_type', 'definition': 'Tpe of the parameter. Accepted values are string, integer, '
                                                       'float or boolean', 'required': True},
    'Value': {'id': 'has_fixed_value', 'definition': 'Value of this parameter in this setup. Setting up a value will '
                                                     'make the parameter non-editable on execution',
              'required': False},
    'Default Value': {'id': 'has_default_value', 'definition': 'Default value of the parameter', 'required': False},
    'Minimum accepted value': {'id': 'has_minimum_accepted_value', 'definition': 'Minimum value the parameter can have',
                               'required': False},
    'Maximum accepted value': {'id': 'has_maximum_accepted_value', 'definition': 'Maximum value the parameter can '
                                                                                 'have ', 'required': False},
}

mapping_model_configuration = {
    'Name': {"id": 'label'},
}
mapping_person = {
    'name': {"id": 'label'},
    'email': {"id": 'email'},
    'website': {"id": 'website'}
}
mapping_sample_resource = {
    'URL': {"id": 'value'}
}
get_complex(mapping_model, Model)
get_complex(mapping_model_version, SoftwareVersion)
get_complex(mapping_dataset_specification, DatasetSpecification)
get_complex(mapping_parameter, Parameter)
get_complex(mapping_person, Person)
get_complex(mapping_sample_resource, SampleResource)
