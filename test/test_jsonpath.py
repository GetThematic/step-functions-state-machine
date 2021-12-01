import step_functions_local.jsonpath as jsonpath

# jsonpath
def test_jsonpath():
    # #value()
    # should return the path
    data = {
        "foo": 123,
        "bar": ["a", "b", "c"],
        "car": {
            "cdr": True,
        },
    }
    assert jsonpath.get_json_value(data, "$.foo") == 123
    assert jsonpath.get_json_value(data, "$.bar") == ["a", "b", "c"]
    assert jsonpath.get_json_value(data, "$.car.cdr") == True

    # should assign the value to the specified path)
    data = {
        "car": {
            "cdr": True,
        },
    }
    result = jsonpath.set_json_value(data, "$.car.foo", 123)
    assert result == 123
    assert data == {
        "car": {
            "cdr": True,
            "foo": 123,
        }
    }
