from jsonpath_ng import parse


def get_json_value(data, path):
    jsonpath_expr = parse(path)
    value = next(jsonpath_expr.find(data), None)
    if value:
        value = value.value
    return value


def set_json_value(data, path, value):
    jsonpath_expr = parse(path)
    jsonpath_expr.find(data)
    jsonpath_expr.update(data, value)
