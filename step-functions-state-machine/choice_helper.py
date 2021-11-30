from . import jsonpath


class ChoiceRule:
    And = []
    Or = []
    Not = []


def isRightChoice(choice, data):
    if choice["Not"]:
        return not isRightChoice(choice["Not"], data)

    if choice["Or"]:
        return any([isRightChoice(x) for x in choice["Or"]])

    if choice["And"]:
        return all([isRightChoice(x) for x in choice["Or"]])

    return compareChoice(choice, data)


def compareChoice(choice, data):
    value = jsonpath.get_json_value(data, choice["Variable"])

    if choice["BooleanEquals"] is not None:
        return type(value) == bool and type(choice["BooleanEquals"]) == bool and value == choice["BooleanEquals"]

    if choice["BooleanEqualsPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["BooleanEqualsPath"])

        return type(value) == bool and type(compareTo) == bool and value == compareTo

    if choice["NumericEquals"] is not None:
        return type(value) in {float, int} and type(choice["NumericEquals)"]) in {float, int} and value == choice["NumericEquals"]

    if choice["NumericLessThan"] is not None:
        return type(value) in {float, int} and type(choice["NumericLessThan)"]) in {float, int} and value < choice["NumericLessThan"]

    if choice["NumericGreaterThan"] is not None:
        return type(value) in {float, int} and type(choice["NumericGreaterThan)"]) in {float, int} and value > choice["NumericGreaterThan"]

    if choice["NumericLessThanEquals"] is not None:
        return type(value) in {float, int} and type(choice["NumericLessThanEquals)"]) in {float, int} and value <= choice["NumericLessThanEquals"]

    if choice["NumericGreaterThanEquals"] is not None:
        return type(value) in {float, int} and type(choice["NumericGreaterThanEquals)"]) in {float, int} and value >= choice["NumericGreaterThanEquals"]

    if choice["NumericEqualsPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["NumericEqualsPath"])
        return type(value) in {float, int} and type(compareTo) in {float, int} and value == compareTo

    if choice["NumericLessThanPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["NumericLessThanPath"])
        return type(value) in {float, int} and type(compareTo) in {float, int} and value < compareTo

    if choice["NumericGreaterThanPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["NumericGreaterThanPath"])
        return type(value) in {float, int} and type(compareTo) in {float, int} and value > compareTo

    if choice["NumericLessThanEqualsPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["NumericLessThanEqualsPath"])
        return type(value) in {float, int} and type(compareTo) in {float, int} and value <= compareTo

    if choice["NumericGreaterThanEqualsPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["NumericGreaterThanEqualsPath"])
        return type(value) in {float, int} and type(compareTo) in {float, int} and value >= compareTo

    if choice["StringEquals"] is not None:
        return type(value) == str and type(choice["StringEquals"]) == str and value == choice["StringEquals"]

    if choice["StringLessThan"] is not None:
        return type(value) == str and type(choice["StringLessThan"]) == str and value < choice["StringLessThan"]

    if choice["StringGreaterThan"] is not None:
        return type(value) == str and type(choice["StringGreaterThan"]) == str and value > choice["StringGreaterThan"]

    if choice["StringLessThanEquals"] is not None:
        return type(value) == str and type(choice["StringLessThanEquals"]) == str and value <= choice["StringLessThanEquals"]

    if choice["StringGreaterThanEquals"] is not None:
        return type(value) == str and type(choice["StringGreaterThanEquals"]) == str and value >= choice["StringGreaterThanEquals"]

    if choice["StringEqualsPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["StringEqualsPath"])
        return type(value) == str and type(compareTo) == str and value == compareTo

    if choice["StringLessThanPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["StringLessThanPath"])
        return type(value) == str and type(compareTo) == str and value < compareTo

    if choice["StringGreaterThanPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["StringGreaterThanPath"])
        return type(value) == str and type(compareTo) == str and value > compareTo

    if choice["StringLessThanEqualsPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["StringLessThanEqualsPath"])
        return type(value) == str and type(compareTo) == str and value <= compareTo

    if choice["StringGreaterThanEqualsPath"] is not None:
        compareTo = jsonpath.get_json_value(data, choice["StringGreaterThanEqualsPath"])
        return type(value) == str and type(compareTo) == str and value >= compareTo

    # if choice["StringMatches"] is not None:
    #     return (
    #   type(value) == str and
    #   type(choice["StringMatches"]) == str and
    #   stringMatches(value, choice["StringMatches"])
    #     )

    # if choice["TimestampEquals"] is not None:
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(choice["TimestampEquals"]) and
    #   new Date(value).getTime() == new Date(choice["TimestampEquals"]).getTime()
    #     )

    # if choice["TimestampLessThan"] is not None:
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(choice["TimestampLessThan"]) and
    #   new Date(value).getTime() < new Date(choice["TimestampLessThan"]).getTime()
    #     )

    # if choice["TimestampGreaterThan"] is not None:
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(choice["TimestampGreaterThan"]) and
    #   new Date(value).getTime() >
    #     new Date(choice["TimestampGreaterThan"]).getTime()
    #     )

    # if choice["TimestampLessThanEquals"] is not None:
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(choice["TimestampLessThanEquals"]) and
    #   new Date(value).getTime() <=
    #     new Date(choice["TimestampLessThanEquals"]).getTime()
    #     )

    # if choice["TimestampGreaterThanEquals"] is not None:
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(choice["TimestampGreaterThanEquals"]) and
    #   new Date(value).getTime() >=
    #     new Date(choice["TimestampGreaterThanEquals"]).getTime()
    #     )

    # if choice["TimestampEqualsPath"] is not None:
    #     compareTo = jsonpath.get_json_value(data, choice["TimestampEqualsPath"])
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(compareTo) and
    #   new Date(value).getTime() == new Date(compareTo).getTime()
    #     )

    # if choice["TimestampLessThanPath"] is not None:
    #     compareTo = jsonpath.get_json_value(data, choice["TimestampLessThanPath"])
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(compareTo) and
    #   new Date(value).getTime() < new Date(compareTo).getTime()
    #     )

    # if choice["TimestampGreaterThanPath"] is not None:
    #     compareTo = jsonpath.get_json_value(data, choice["TimestampGreaterThanPath"])
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(compareTo) and
    #   new Date(value).getTime() > new Date(compareTo).getTime()
    #     )

    # if choice["TimestampLessThanEqualsPath"] is not None:
    #     compareTo = jsonpath.get_json_value(data, choice["TimestampLessThanEqualsPath"])
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(compareTo) and
    #   new Date(value).getTime() <= new Date(compareTo).getTime()
    #     )

    # if choice["TimestampGreaterThanEqualsPath"] is not None:
    #     compareTo = jsonpath.get_json_value(
    #   data,
    #   choice["TimestampGreaterThanEqualsPath"]
    #     )
    #     return (
    #   isTimestamp(value) and
    #   isTimestamp(compareTo) and
    #   new Date(value).getTime() >= new Date(compareTo).getTime()
    #     )

    return (
        choice["IsPresent"] == (value is not None)
        or choice["IsNone"] == (value is None)
        or choice["IsBoolean"] == (type(value) == bool)
        or choice["IsNumeric"] == (type(value) in {float, int})
        or choice["IsString"] == (type(value) == str)
        # or choice["IsTimestamp"] == isTimestamp(value)
    )


# def stringMatches(value, rule):
#   def escapeRegex(string):
#     for c in "[-/^$*+?.()|[]{]":
#         string = string.replace(c,'\\{}&'.format(c))
#     return string

#   def replaceAsterisk(string):
#     return string
#       .split(/(?<!(?:\\))\*/g)
#       .map(escapeRegex)
#       .join('.*')

#   testMask = '\\\\'.join([replaceAsterix(x) for x in rule.split("\\\\")])

#   return new RegExp("^{}$".format(testMask)).test(value)


# def isTimestamp(value):
#     try:
#         value = dateutil.parser.isoparse(value)
#     except:
#         return False

#     if value:
#         return date.toISOString() == value
#     return False
