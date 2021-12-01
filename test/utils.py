import os
import json
import step_functions_local


def load_fixture(path, validate=True):
    path = os.path.join(os.path.dirname(__file__), path)

    with open(path, "r") as f:
        definition = json.load(f)
    if validate:
        step_functions_local.validate(definition)
    return definition


def increment(i):
    return i + 1


def add_numbers(numbers):
    return numbers["val1"] + numbers["val2"]
