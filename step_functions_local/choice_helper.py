import re
import datetime
import fnmatch
from . import jsonpath


class ChoiceRule:
    And = []
    Or = []
    Not = []


def isRightChoice(choice, data):
    if choice.get("Not"):
        return not isRightChoice(choice.get("Not"), data)

    if choice.get("Or"):
        return any([isRightChoice(x, data) for x in choice.get("Or")])

    if choice.get("And"):
        return all([isRightChoice(x, data) for x in choice.get("And")])

    return compareChoice(choice, data)


def compareChoice(choice, data):
    value = jsonpath.get_json_value(data, choice.get("Variable"))

    if choice.get("BooleanEquals") is not None:
        return type(value) == bool and type(choice.get("BooleanEquals")) == bool and value == choice.get("BooleanEquals")

    if choice.get("BooleanEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("BooleanEqualsPath"))

        return type(value) == bool and type(compareTo) == bool and value == compareTo

    if choice.get("NumericEquals") is not None:
        return type(value) in {float, int} and type(choice.get("NumericEquals")) in {float, int} and float(value) == float(choice.get("NumericEquals"))

    if choice.get("NumericLessThan") is not None:
        return type(value) in {float, int} and type(choice.get("NumericLessThan")) in {float, int} and float(value) < float(choice.get("NumericLessThan"))

    if choice.get("NumericGreaterThan") is not None:
        return type(value) in {float, int} and type(choice.get("NumericGreaterThan")) in {float, int} and float(value) > float(choice.get("NumericGreaterThan"))

    if choice.get("NumericLessThanEquals") is not None:
        return (
            type(value) in {float, int}
            and type(choice.get("NumericLessThanEquals")) in {float, int}
            and float(value) <= float(choice.get("NumericLessThanEquals"))
        )

    if choice.get("NumericGreaterThanEquals") is not None:
        return (
            type(value) in {float, int}
            and type(choice.get("NumericGreaterThanEquals")) in {float, int}
            and float(value) >= float(choice.get("NumericGreaterThanEquals"))
        )

    if choice.get("NumericEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("NumericEqualsPath"))
        return type(value) in {float, int} and type(compareTo) in {float, int} and value == compareTo

    if choice.get("NumericLessThanPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("NumericLessThanPath"))
        return type(value) in {float, int} and type(compareTo) in {float, int} and value < compareTo

    if choice.get("NumericGreaterThanPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("NumericGreaterThanPath"))
        return type(value) in {float, int} and type(compareTo) in {float, int} and value > compareTo

    if choice.get("NumericLessThanEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("NumericLessThanEqualsPath"))
        return type(value) in {float, int} and type(compareTo) in {float, int} and value <= compareTo

    if choice.get("NumericGreaterThanEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("NumericGreaterThanEqualsPath"))
        return type(value) in {float, int} and type(compareTo) in {float, int} and value >= compareTo

    if choice.get("StringEquals") is not None:
        return type(value) == str and type(choice.get("StringEquals")) == str and value == choice.get("StringEquals")

    if choice.get("StringLessThan") is not None:
        return type(value) == str and type(choice.get("StringLessThan")) == str and value < choice.get("StringLessThan")

    if choice.get("StringGreaterThan") is not None:
        return type(value) == str and type(choice.get("StringGreaterThan")) == str and value > choice.get("StringGreaterThan")

    if choice.get("StringLessThanEquals") is not None:
        return type(value) == str and type(choice.get("StringLessThanEquals")) == str and value <= choice.get("StringLessThanEquals")

    if choice.get("StringGreaterThanEquals") is not None:
        return type(value) == str and type(choice.get("StringGreaterThanEquals")) == str and value >= choice.get("StringGreaterThanEquals")

    if choice.get("StringEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("StringEqualsPath"))
        return type(value) == str and type(compareTo) == str and value == compareTo

    if choice.get("StringLessThanPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("StringLessThanPath"))
        return type(value) == str and type(compareTo) == str and value < compareTo

    if choice.get("StringGreaterThanPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("StringGreaterThanPath"))
        return type(value) == str and type(compareTo) == str and value > compareTo

    if choice.get("StringLessThanEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("StringLessThanEqualsPath"))
        return type(value) == str and type(compareTo) == str and value <= compareTo

    if choice.get("StringGreaterThanEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("StringGreaterThanEqualsPath"))
        return type(value) == str and type(compareTo) == str and value >= compareTo

    if choice.get("StringMatches") is not None:
        raise NotImplementedError("stringMatches not yet implemented")
        # return type(value) == str and type(choice.get("StringMatches")) == str and stringMatches(value, choice.get("StringMatches"))

    if choice.get("TimestampEquals") is not None:
        return (
            is_timestamp(value)
            and is_timestamp(choice.get("TimestampEquals"))
            and get_datetime(value).timestamp() == get_datetime(choice.get("TimestampEquals")).timestamp()
        )

    if choice.get("TimestampLessThan") is not None:
        return (
            is_timestamp(value)
            and is_timestamp(choice.get("TimestampLessThan"))
            and get_datetime(value).timestamp() < get_datetime(choice.get("TimestampLessThan")).timestamp()
        )

    if choice.get("TimestampGreaterThan") is not None:
        return (
            is_timestamp(value)
            and is_timestamp(choice.get("TimestampGreaterThan"))
            and get_datetime(value).timestamp() > get_datetime(choice.get("TimestampGreaterThan")).timestamp()
        )

    if choice.get("TimestampLessThanEquals") is not None:
        return (
            is_timestamp(value)
            and is_timestamp(choice.get("TimestampLessThanEquals"))
            and get_datetime(value).timestamp() <= get_datetime(choice.get("TimestampLessThanEquals")).timestamp()
        )

    if choice.get("TimestampGreaterThanEquals") is not None:
        return (
            is_timestamp(value)
            and is_timestamp(choice.get("TimestampGreaterThanEquals"))
            and get_datetime(value).timestamp() >= get_datetime(choice.get("TimestampGreaterThanEquals")).timestamp()
        )

    if choice.get("TimestampEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("TimestampEqualsPath"))
        return is_timestamp(value) and is_timestamp(compareTo) and get_datetime(value).timestamp() == get_datetime(compareTo).timestamp()

    if choice.get("TimestampLessThanPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("TimestampLessThanPath"))
        return is_timestamp(value) and is_timestamp(compareTo) and get_datetime(value).timestamp() < get_datetime(compareTo).timestamp()

    if choice.get("TimestampGreaterThanPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("TimestampGreaterThanPath"))
        return is_timestamp(value) and is_timestamp(compareTo) and get_datetime(value).timestamp() > get_datetime(compareTo).timestamp()

    if choice.get("TimestampLessThanEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("TimestampLessThanEqualsPath"))
        return is_timestamp(value) and is_timestamp(compareTo) and get_datetime(value).timestamp() <= get_datetime(compareTo).timestamp()

    if choice.get("TimestampGreaterThanEqualsPath") is not None:
        compareTo = jsonpath.get_json_value(data, choice.get("TimestampGreaterThanEqualsPath"))
        return is_timestamp(value) and is_timestamp(compareTo) and get_datetime(value).timestamp() >= get_datetime(compareTo).timestamp()

    return (
        choice.get("IsPresent") == (value is not None)
        or choice.get("IsNone") == (value is None)
        or choice.get("IsBoolean") == (type(value) == bool)
        or choice.get("IsNumeric") == (type(value) in {float, int})
        or choice.get("IsString") == (type(value) == str)
        or choice.get("IsTimestamp") == is_timestamp(value)
    )


def stringMatches(value, rule):
    def escapeRegex(string):
        print(string)
        return re.sub("[-/^$*+?.()|[]{}]", "\\$&", string)

    def replaceAsterisk(string):
        print(string)
        return ".*".join([escapeRegex(x) for x in string.split("*")])

    test_mask = "\\\\".join([replaceAsterisk(x) for x in rule.split("\\\\")])
    print("test_mask", test_mask)
    return re.match(test_mask, value) is not None


def get_datetime(value):
    try:
        value = value.replace("Z", "+00:00")
        value = datetime.datetime.fromisoformat(value)
    except Exception as e:
        return None
    return value


def is_timestamp(value):
    value_converted = get_datetime(value)
    return value_converted is not None
