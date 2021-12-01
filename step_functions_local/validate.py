import os
import json
import jsonschema


def validate(definition):
    # pull the correct jsonschema
    schema_location = os.path.join(os.path.dirname(__file__), "data", "state-machine.json")
    if not os.path.exists(schema_location):
        raise Exception("Unknown schema")
    try:
        with open(schema_location, "r") as f:
            schema = json.load(f)
    except Exception as e:
        raise Exception("Could not load schema. Error was {}".format(e))

    try:
        schemas = os.path.join(os.path.dirname(__file__), "data")
        store = {}
        for fn in os.listdir(schemas):
            path = os.path.join(schemas, fn)
            with open(path, "r") as fh:
                data = json.load(fh)
                store[data.get("$id")] = data

        resolver = jsonschema.RefResolver("http://asl-validator.cloud", "http://asl-validator.cloud", store=store)
        jsonschema.validate(definition, schema, resolver=resolver)
    except jsonschema.ValidationError as e:
        raise Exception("Failed schema validation: " + str(e))

    return True
