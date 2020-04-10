import json
import typing

import modelcatalog
from modelcatalog import Model
from mic._utils import get_api
from modelcatalog import ApiException
api, username = get_api()
api_instance = modelcatalog.ModelApi(api_client=api)


def test_1():
    try:
        # List all Person entities
        api_response = api_instance.models_id_get("CYCLES", username=username)
    except ApiException as e:
        raise e
    response = api_response
    a = api_instance.models_post(username, model=response)
    with open("cycles.json", "w") as f:
        json.dump(a.to_dict(), f)

def read_json():
    with open("test.json", "r") as f:
        data = json.load(f)
    m = Model(**data)
    a = api_instance.models_post(username, model=m)
    return a

print(read_json())