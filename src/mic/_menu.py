from mic._mappings import get_definition, get_prop_mapping, get_type_mapping, select_enable, is_complex
from mic.model_catalog_utils import get_label_from_response, create_request
from mic.drawer import print_request, print_choices, show_values_complex, show_values, show_error
from mic.file import save
from mic._utils import first_line_new, validate_metadata
import click
from modelcatalog import ApiException
from mic.model_catalog_utils import MODEL_CATALOG_URL

COMPLEX_CHOICES = ["select", "add", "edit", "remove"]
ACTION_CHOICES = ["show", "save", "send", "exit"]


def menu_select_existing_resources(resource_object, request_property, variable_selected):
    """
    Menu: Show the existing resources and asks to user the selection
    @param variable_selected: The name of variable selected (mic spec). For example: Versions
    @type variable_selected: string
    @return: A resource
    @rtype: dict
    """
    click.echo("Available resources")
    sub_resource_object = getattr(resource_object, request_property)
    sub_resource_mapping, sub_resource = sub_resource_object["mapping"], sub_resource_object["resource"]
    response = sub_resource.get()
    resources = get_label_from_response(response)
    print_choices(resources)
    if click.confirm("Did you find the {}?".format(variable_selected), default=True):
        choice = click.prompt("Select the {}".format(variable_selected),
                              default=1,
                              show_choices=False,
                              type=click.Choice(list(range(1, len(resources) + 1))),
                              value_proc=parse
                              )
        return response[choice - 1].to_dict()
    return None


def menu_select_property(request, mapping, is_subresource=False):
    """
    Menu: Show the properties by the request
    @param request: Request (modelcatalog spec)
    @type request: dict
    @param mapping: Mapping of the resource
    @type mapping: dict
    @return: the choice
    @rtype: [int, str]
    """
    choices_new = ACTION_CHOICES.copy()
    if is_subresource:
        choices_new.remove("send")
    print_request(request, mapping)
    properties_choices = list(request.keys())
    select_property = click.prompt(
        "Select the property to edit [{}-{}] or {}".format(1, len(properties_choices), choices_new),
        default=1,
        show_choices=False,
        type=click.Choice(list(range(1, len(properties_choices) + 1)) + choices_new),
        value_proc=parse
    )

    if not isinstance(select_property, int) and select_property not in choices_new:
        return -1
    return select_property


def menu_call_actions_complex(request, variable_selected, resource_name, mapping, resource_object, request_property):
    """
    Asks about the action to take for complex resource (select, add, edit, remove)
    @param resource_object:
    @type resource_object:
    @param request: request
    @type request: dict
    @param variable_selected: The name of variable selected (mic spec). For example: Versions
    @type variable_selected: string
    @param resource_name: the resource_name to print it
    @type resource_name: string
    @param mapping: Mapping of the resource
    @type mapping: dict
    @param request_property: the property selected (model spec). For example: has_version
    @type request_property: string
    @return: The action to take: COMPLEX_CHOICES
    @rtype: string
    """
    choices_new = COMPLEX_CHOICES.copy()
    if request[request_property] is None:
        choices_new.remove("edit")
        choices_new.remove("remove")
    if not select_enable(mapping[variable_selected]):
        choices_new.remove("select")

    if len(choices_new) == 1:
        choice = choices_new[0]
    else:
        choice = click.prompt("Select action:",
                              default=choices_new[0],
                              show_choices=True,
                              type=click.Choice(choices_new),
                              value_proc=parse
                              )

    if choice not in choices_new:
        return choice

    if choice == COMPLEX_CHOICES[0]:
        call_menu_select_existing_resources(request, variable_selected, resource_object, mapping, request_property)
    elif choice == COMPLEX_CHOICES[1]:
        mapping_create_value_complex(request, resource_object, request_property)
    elif choice == COMPLEX_CHOICES[2]:
        menu_edit_resource_complex(request[request_property], variable_selected, mapping, resource_object, request)
    elif choice == COMPLEX_CHOICES[3]:
        menu_delete_resource_complex(request[request_property])
    return choice


def menu_delete_resource_complex(request):
    """
    Menu: asks the resource to delete
    @param request: request
    @type request: dict
    """
    labels = get_label_from_response(request)
    print_choices(labels)
    choice = click.prompt("Select the resource to delete",
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(labels) + 1))),
                          value_proc=parse
                          )
    if not isinstance(choice, int):
        show_error("Please only input integers not characters.")
        menu_delete_resource_complex(request)
    elif choice > 0 and choice <= len(labels):
        request.pop(choice - 1)
    else:
        show_error("The current value for choice is either greater than length of input size or less than equal to zero.")
        menu_delete_resource_complex(request)


def menu_ask_simple_value(variable_selected, resource_name, mapping, default_value=""):
    """
    Menu: ask the value for simple property
    @param default_value: If the resource has a value, pass it as default value
    @type default_value: [int, string, bool, float]
    @param variable_selected: The name of variable selected (mic spec). For example: Versions
    @type variable_selected: string
    @param resource_name: the resource_name to print it
    @type resource_name: string
    @param mapping: Mapping of the resource
    @type mapping: dict
    @return:
    @rtype:
    """
    get_definition(mapping, variable_selected)
    metadata_type = get_type_mapping(mapping)
    value = click.prompt('{} - {} '.format(resource_name, variable_selected), default=default_value)
    if value:
        if metadata_type is not None:
            if validate_metadata(metadata_type, value):
                return value
            else:
                show_error("{} should be type of {}".format(variable_selected, metadata_type.name))
                return menu_ask_simple_value(variable_selected, resource_name, mapping, default_value=default_value)
        return value
    else:
        return None


def menu_push(request, resource_object, parent):
    try:
        response_sub_resource = resource_object.post(request)
        request['id'] = response_sub_resource.id
        if parent and parent.name == "Software Version":
            variable_selected = "models"
            response_get_parent = parent.get()
            resources = get_label_from_response(response_get_parent)
            print_choices(resources)
            if click.confirm("Did you find the {}?".format(variable_selected), default=True):
                choice = click.prompt("Select the {}".format(variable_selected),
                                      default=1,
                                      show_choices=False,
                                      type=click.Choice(list(range(1, len(resources) + 1))),
                                      value_proc=parse
                                      )
                model_version = response_get_parent[choice - 1]
                if model_version.has_configuration:
                    model_version.has_configuration.append({"id":response_sub_resource.id})
                else:
                    model_version.has_configuration = [{"id":response_sub_resource.id}]

                parent.put(model_version)
        click.secho(f"Success", fg="green")
    except ApiException:
        click.secho(f"An error occurred when sending the request", fg="red")


def menu_edit_resource_complex(request, variable_selected, mapping, resource_object, full_request=None):
    """
    Call to the menu to create the resource complex
    @param resource_object:
    @type resource_object:
    @param request: request
    @type request: dict
    @param variable_selected: The name of variable selected (mic spec). For example: Versions
    @type variable_selected: string
    @param mapping: Mapping of the resource
    @type mapping: dict
    """
    labels = get_label_from_response(request)
    print_choices(labels)
    choice = click.prompt("Select the resource to edit",
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(labels) + 1))),
                          value_proc=parse
                          )
    request_var = get_prop_mapping(mapping, variable_selected)
    call_edit_resource(request, mapping, variable_selected, request_var, resource_object, full_request)


def call_ask_value(request, variable_selected, resource_name, resource_object, mapping):
    """
    Asks about the value (complex or not)
    @param resource_object:
    @type resource_object:
    @param request: request
    @type request: dict
    @param variable_selected: The name of variable selected (mic spec). For example: Versions
    @type variable_selected: string
    @param resource_name: the resource_name to print it
    @type resource_name: string
    @param mapping: Mapping of the resource
    @type mapping: dict
    """
    request_property = get_prop_mapping(mapping, variable_selected)
    click.clear()

    # Check if the subresource of the object causes an AttributeError (Raised when there is no such attribute in the object)
    is_info_about_sub_resource = True

    try:
        sub_resource_object = getattr(resource_object, request_property)
    except AttributeError as ae:
        is_info_about_sub_resource = False

    # Perform menu action for complex resource if subresource is available 
    if is_complex(mapping, variable_selected) and is_info_about_sub_resource:
        show_values_complex(request, request_property, variable_selected)
        menu_call_actions_complex(request, variable_selected, resource_name, mapping, resource_object, request_property)
    else:
        show_values(request, request_property, variable_selected)
        call_ask_simple_value(request, variable_selected, resource_name, mapping, request_property)


def call_ask_simple_value(request, variable_selected, resource_name, mapping, request_property):
    """
    Call to the menu to set the value for simple resource
    @param request: request
    @type request: dict
    @param variable_selected: The name of variable selected (mic spec). For example: Versions
    @type variable_selected: string
    @param resource_name: the resource_name to print it
    @type resource_name: string
    @param mapping: Mapping of the resource
    @type mapping: dict
    @param request_property: the property selected (model spec). For example: has_version
    @type request_property: string
    """
    default_value = request[request_property] if request_property in request and request[request_property] else None
    default_value = default_value[0] if isinstance(default_value, list) else default_value

    value = menu_ask_simple_value(variable_selected, resource_name, mapping[variable_selected],
                                  default_value=default_value)
    if value:
        request[request_property] = [value]


def call_menu_select_existing_resources(request, variable_selected, resource_object, mapping, request_property):
    """
    Call to the menu to select the resource complex
    @param request: request
    @type request: dict
    @param variable_selected: The name of variable selected (mic spec). For example: Versions
    @type variable_selected: string
    @param resource_object: the resource_name to print it
    @type resource_object: string
    @param mapping: Mapping of the resource
    @type mapping: dict
    @param request_property: the property selected (model spec). For example: has_version
    @type request_property: string
    """
    value = None
    if select_enable(mapping[variable_selected]):
        select_sub_resource = menu_select_existing_resources(resource_object, request_property, variable_selected)
        value = select_sub_resource if select_sub_resource else mapping_resource_complex(resource_object,
                                                                                         request_property, request)
    elif not request[request_property]:
        value = mapping_resource_complex(resource_object, request_property, request)
    if request[request_property] is None:
        request[request_property] = [value]
    else:
        request[request_property].append(value)


def call_menu_select_property(mapping, resource_object, full_request=None, parent=None, is_subresource=False):
    """
    Method to call the menu to add resource
    @param mapping: Mapping of the resource
    @type mapping: dict
    @param resource_object: the resource_object
    @type resource_object: object
    @param full_request: request (optionally loaded from file)
    @type request: dict
    """
    request = create_request(mapping.values())
    if full_request is None:
        full_request = request
    # load from file only if it's top resource. Otherwise it would affect sub-resources.
    if parent is None and full_request is not None:
        request = full_request
    while True:
        click.clear()
        first_line_new(resource_object.name)
        property_chosen = menu_select_property(request, mapping, is_subresource)
        if handle_actions(request, property_chosen, mapping, resource_object, full_request=full_request, parent=parent):
            break
        if isinstance(property_chosen, int) and 0 < property_chosen < len(mapping.keys()) + 1:
            property_model_catalog_selected = list(mapping.keys())[property_chosen - 1]
            call_ask_value(request, property_model_catalog_selected, resource_name=resource_object.name,
                           resource_object=resource_object, mapping=mapping)
    return request


def call_edit_resource(request, mapping, resource_name, request_property, resource_object, full_request=None):
    """
    Call to the menu to edit the resource complex
    @param resource_object:
    @type resource_object:
    @param request: request
    @type request: dict
    @param resource_name: the resource_name to print it
    @type resource_name: string
    @param mapping: Mapping of the resource
    @type mapping: dict
    @param request_property: the property selected (model spec). For example: has_version
    @type request_property: string
    """
    while True:
        sub_resource_object = getattr(resource_object, request_property)
        sub_resource_mapping, sub_resource = sub_resource_object["mapping"], sub_resource_object["resource"]
        property_chosen = menu_select_property(request[0], sub_resource_mapping)
        if handle_actions(request, property_chosen, sub_resource_mapping, sub_resource, full_request=full_request,
                          parent=None):
            break
        # Some special actions do not require exit.
        if isinstance(property_chosen, int) and 0 < property_chosen < (len(sub_resource_mapping.keys()) + 1):
            property_mcat_selected = list(sub_resource_mapping.keys())[property_chosen - 1]
            call_ask_value(request[0], property_mcat_selected, resource_name=resource_name,
                           resource_object=sub_resource,
                           mapping=sub_resource_mapping)


def mapping_resource_complex(resource_object, request_property, full_request=None):
    """
    Mapping: maps the variable_select with the Model Catalog Resource
    @param request_selected:
    @type request_selected:
    @param subresource:
    @type subresource:
    @param full_request:
    @type full_request:
    """
    sub_resource_object = getattr(resource_object, request_property)
    sub_resource_mapping, sub_resource = sub_resource_object["mapping"], sub_resource_object["resource"]
    return call_menu_select_property(sub_resource_mapping, sub_resource, full_request, is_subresource=True)


def mapping_create_value_complex(request, resource_object, request_property):
    """
    Call to the menu to create the resource complex
    @param request: request
    @type request: dict
    @param resource_object: Mapping of the resource
    @type resource_object: dict
    @param request_property: the property selected (model spec). For example: has_version
    @type request_property: string
    """
    value = mapping_resource_complex(resource_object, request_property)
    # If the 'id' key is empty, we add a default so the program does not fail
    if value['label'] is None:
        value['label'] = 'Resource name [required]'
    if request[request_property] is None:
        request[request_property] = [value]
    else:
        request[request_property].append(value)


def handle_actions(request, action, mapping, resource_object, full_request, parent):
    """
    Verify the choice (menu_select_property) and call the special actions (show, save, push or exit). If not return False
    @param parent:
    @type parent:
    @param resource_object:
    @type resource_object:
    @param full_request:
    @type full_request:
    @param request: request (modelcatalog spec)
    @type request: dict
    @param action: The choice
    @type action: [str, int]
    @return: True: the special action is done. False: The user is selecting a property, handle the next action.
    @rtype: bool
    @param mapping: mapping to be able to show properties
    """
    if type(action) != str or action not in ACTION_CHOICES:
        # action not recognized; do not exit
        return False
    if action == ACTION_CHOICES[0]:
        # SHOW
        prop = parse(click.prompt('Select property to show'))
        try:
            property_mcat_selected = list(mapping.keys())[prop - 1]
            show_values(request, mapping[property_mcat_selected]['id'], 'Resource')
            input('Press ENTER to continue')
        except:
            click.echo('Property not in range')
        finally:
            return False
    if action == ACTION_CHOICES[1]:
        # SAVE
        save(full_request)
        return click.confirm("Exit?", default=False)
    elif action == ACTION_CHOICES[2]:
        # PUSH
        menu_push(full_request, resource_object, parent=parent)
        save(full_request)
        if request["id"] and click.confirm("See the model/config/setup on your browser?", default=False):
            click.launch("{}{}".format(MODEL_CATALOG_URL, request["id"]))
        if request["id"]:
            click.echo("Online URI for model/configuration/setup: " + MODEL_CATALOG_URL + request["id"])
    elif action == ACTION_CHOICES[3]:
        pass
    return True


def parse(value):
    try:
        return int(value)
    except:
        return value
