from jsonpath_ng import parse


def get_json_value(data, path):
    jsonpath_expr = parse(path)
    found = jsonpath_expr.find(data)
    if len(found) > 0:
        return found[0].value
    return None


def set_json_value(data, path, value):
    # ensure all parents are available for updating
    path_parts = path.split(".")
    for i in range(2, len(path_parts) + 1):
        test_path = ".".join(path_parts[:i])
        jsonpath_expr = parse(test_path)
        if not jsonpath_expr.find(data):
            existing = get_json_value(data, ".".join(path_parts[: i - 1]))
            if type(existing) != dict:
                return None
            existing[path_parts[i - 1]] = {}
            update_path = ".".join(path_parts[: i - 1])
            jsonpath_expr = parse(update_path)
            jsonpath_expr.update(data, existing)
    # do the actual update
    jsonpath_expr = parse(path)
    result = jsonpath_expr.find(data)
    jsonpath_expr.update(data, value)
    return value
