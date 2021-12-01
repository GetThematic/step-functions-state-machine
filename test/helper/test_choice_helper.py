from step_functions_local import choice_helper


def test_choice_helper():
    # when simple choice rule applied
    conditions = [
        {
            "conditionType": "BooleanEquals",
            "condition": True,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5, False],
                [False, False],
                [True, True],
            ],
        },
        {
            "conditionType": "BooleanEquals",
            "condition": False,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5, False],
                [False, True],
                [True, False],
            ],
        },
        {
            "conditionType": "BooleanEquals",
            "condition": None,
            "testCases": [
                [False, False],
                [True, False],
            ],
        },
        {
            "conditionType": "BooleanEquals",
            "condition": 5,
            "testCases": [
                [False, False],
                [True, False],
            ],
        },
        {
            "conditionType": "BooleanEquals",
            "condition": "abc",
            "testCases": [
                [False, False],
                [True, False],
            ],
        },
        {
            "conditionType": "BooleanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": True,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5, False],
                [False, False],
                [True, True],
            ],
        },
        {
            "conditionType": "BooleanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": None,
            "testCases": [
                [False, False],
                [True, False],
            ],
        },
        {
            "conditionType": "BooleanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": "abc",
            "testCases": [
                [False, False],
                [True, False],
            ],
        },
        {
            "conditionType": "BooleanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": 5,
            "testCases": [
                [False, False],
                [True, False],
            ],
        },
        {
            "conditionType": "BooleanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": False,
            "testCases": [
                [False, True],
                [True, False],
            ],
        },
        {
            "conditionType": "NumericEquals",
            "condition": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5.0, True],
                [5.1, False],
            ],
        },
        {
            "conditionType": "NumericLessThan",
            "condition": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [4.9, True],
                [5.0, False],
                [5.1, False],
            ],
        },
        {
            "conditionType": "NumericLessThanEquals",
            "condition": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [4.9, True],
                [5.0, True],
                [5.1, False],
            ],
        },
        {
            "conditionType": "NumericGreaterThan",
            "condition": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [4.9, False],
                [5.0, False],
                [5.1, True],
            ],
        },
        {
            "conditionType": "NumericGreaterThanEquals",
            "condition": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [4.9, False],
                [5.0, True],
                [5.1, True],
            ],
        },
        {
            "conditionType": "NumericEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5.1, False],
                [5.0, True],
                [4.9, False],
            ],
        },
        {
            "conditionType": "NumericLessThanPath",
            "condition": '$."compareTo"',
            "compareTo": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5.1, False],
                [5.0, False],
                [4.9, True],
            ],
        },
        {
            "conditionType": "NumericGreaterThanPath",
            "condition": '$."compareTo"',
            "compareTo": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5.1, True],
                [5.0, False],
                [4.9, False],
            ],
        },
        {
            "conditionType": "NumericLessThanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5.1, False],
                [5.0, True],
                [4.9, True],
            ],
        },
        {
            "conditionType": "NumericGreaterThanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": 5,
            "testCases": [
                [None, False],
                ["abc", False],
                ["5", False],
                [5.1, True],
                [5.0, True],
                [4.9, False],
            ],
        },
        {
            "conditionType": "StringEquals",
            "condition": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["ab", False],
                ["abc", True],
            ],
        },
        # {
        #     "conditionType": "StringMatches",
        #     "condition": "a*c",
        #     "testCases": [
        #         [None, False],
        #         [5, False],
        #         ["ab", False],
        #         ["bc", False],
        #         ["abc", True],
        #         ["ac", True],
        #         ["abdefc", True],
        #     ],
        # },
        # {
        #     "conditionType": "StringMatches",
        #     # Escaping backslash in string, so it's actually one backslash
        #     "condition": "a\\*c",
        #     "testCases": [
        #         ["ab", False],
        #         ["bc", False],
        #         ["a*c", True],
        #         ["a\\*c", False],
        #         ["ac", False],
        #     ],
        # },
        # {
        #     "conditionType": "StringMatches",
        #     # Escaping backslashes in string, so it's actually 2 backslashes
        #     "condition": "a\\\\*c",
        #     "testCases": [
        #         ["ab", False],
        #         ["bc", False],
        #         ["a*c", False],
        #         ["a\\*c", True],
        #         ["a\\c", True],
        #         ["a\\defc", True],
        #         ["ac", False],
        #     ],
        # },
        {
            "conditionType": "StringLessThan",
            "condition": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["ab", True],
                ["aba", True],
                ["abd", False],
                ["abc", False],
            ],
        },
        {
            "conditionType": "StringLessThanEquals",
            "condition": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["aba", True],
                ["abd", False],
                ["abc", True],
            ],
        },
        {
            "conditionType": "StringGreaterThan",
            "condition": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["aba", False],
                ["abd", True],
                ["az", True],
                ["abc", False],
            ],
        },
        {
            "conditionType": "StringGreaterThanEquals",
            "condition": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["aba", False],
                ["abd", True],
                ["az", True],
                ["abc", True],
            ],
        },
        {
            "conditionType": "StringEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["aba", False],
                ["abd", False],
                ["abc", True],
            ],
        },
        {
            "conditionType": "StringLessThanPath",
            "condition": '$."compareTo"',
            "compareTo": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["aba", True],
                ["abd", False],
                ["abc", False],
            ],
        },
        {
            "conditionType": "StringGreaterThanPath",
            "condition": '$."compareTo"',
            "compareTo": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["aba", False],
                ["abd", True],
                ["az", True],
                ["abc", False],
            ],
        },
        {
            "conditionType": "StringLessThanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["aba", True],
                ["abd", False],
                ["abc", True],
            ],
        },
        {
            "conditionType": "StringGreaterThanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": "abc",
            "testCases": [
                [None, False],
                [5, False],
                ["aba", False],
                ["abd", True],
                ["az", True],
                ["abc", True],
            ],
        },
        {
            "conditionType": "TimestampEquals",
            "condition": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02", False],
                ["2006-01-02T11:45:05.000Z", False],
                ["2006-01-02T15:04:05.000Z", True],
                ["2006-02-01T15:04:05.000Z", False],
            ],
        },
        {
            "conditionType": "TimestampLessThan",
            "condition": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02T11:45:05.000Z", True],
                ["2006-01-02T15:04:05.000Z", False],
                ["2006-02-01T15:04:05.000Z", False],
            ],
        },
        {
            "conditionType": "TimestampLessThanEquals",
            "condition": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02T11:45:05.000Z", True],
                ["2006-01-02T15:04:05.000Z", True],
                ["2006-02-01T15:04:05.000Z", False],
            ],
        },
        {
            "conditionType": "TimestampGreaterThan",
            "condition": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02", False],
                ["2006-01-02T11:45:05.000Z", False],
                ["2006-01-02T15:04:05.000Z", False],
                ["2006-02-01T15:04:05.000Z", True],
            ],
        },
        {
            "conditionType": "TimestampGreaterThanEquals",
            "condition": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02", False],
                ["2006-01-02T11:45:05.000Z", False],
                ["2006-01-02T15:04:05.000Z", True],
                ["2006-02-01T15:04:05.000Z", True],
            ],
        },
        {
            "conditionType": "TimestampEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02", False],
                ["2006-01-02T11:45:05.000Z", False],
                ["2006-01-02T15:04:05.000Z", True],
                ["2006-02-01T15:04:05.000Z", False],
            ],
        },
        {
            "conditionType": "TimestampLessThanPath",
            "condition": '$."compareTo"',
            "compareTo": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02T11:45:05.000Z", True],
                ["2006-01-02T15:04:05.000Z", False],
                ["2006-02-01T15:04:05.000Z", False],
            ],
        },
        {
            "conditionType": "TimestampGreaterThanPath",
            "condition": '$."compareTo"',
            "compareTo": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02", False],
                ["2006-01-02T11:45:05.000Z", False],
                ["2006-01-02T15:04:05.000Z", False],
                ["2006-02-01T15:04:05.000Z", True],
            ],
        },
        {
            "conditionType": "TimestampLessThanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02T11:45:05.000Z", True],
                ["2006-01-02T15:04:05.000Z", True],
                ["2006-02-01T15:04:05.000Z", False],
            ],
        },
        {
            "conditionType": "TimestampGreaterThanEqualsPath",
            "condition": '$."compareTo"',
            "compareTo": "2006-01-02T15:04:05.000Z",
            "testCases": [
                [None, False],
                [True, False],
                [5, False],
                ["ab", False],
                ["2006-01-02", False],
                ["2006-01-02T11:45:05.000Z", False],
                ["2006-01-02T15:04:05.000Z", True],
                ["2006-02-01T15:04:05.000Z", True],
            ],
        },
        {
            "conditionType": "IsPresent",
            "condition": True,
            "testCases": [
                [None, False],
                # [None, True], # should be an undefined test
                [0, True],
                ["abc", True],
            ],
        },
        {
            "conditionType": "IsPresent",
            "condition": False,
            "testCases": [
                [None, True],
                # [None, False],# should be an undefined test
                [0, False],
                ["abc", False],
            ],
        },
        {
            "conditionType": "IsNone",
            "condition": True,
            "testCases": [
                [5, False],
                [None, True],
            ],
        },
        {
            "conditionType": "IsNone",
            "condition": False,
            "testCases": [
                [5, True],
                [None, False],
            ],
        },
        {
            "conditionType": "IsBoolean",
            "condition": True,
            "testCases": [
                [None, False],
                [False, True],
            ],
        },
        {
            "conditionType": "IsBoolean",
            "condition": False,
            "testCases": [
                [None, True],
                [False, False],
            ],
        },
        {
            "conditionType": "IsNumeric",
            "condition": True,
            "testCases": [
                ["abc", False],
                [5, True],
                [5.1, True],
            ],
        },
        {
            "conditionType": "IsNumeric",
            "condition": False,
            "testCases": [
                ["abc", True],
                [5, False],
                [5.1, False],
            ],
        },
        {
            "conditionType": "IsString",
            "condition": True,
            "testCases": [
                [5.1, False],
                ["abc", True],
            ],
        },
        {
            "conditionType": "IsString",
            "condition": False,
            "testCases": [
                [5.1, True],
                ["abc", False],
            ],
        },
        {
            "conditionType": "IsTimestamp",
            "condition": True,
            "testCases": [
                ["abc", False],
                ["2006-01-02T15:04:05.000Z", True],
            ],
        },
        {
            "conditionType": "IsTimestamp",
            "condition": False,
            "testCases": [
                ["abc", True],
                ["2006-01-02T15:04:05.000Z", False],
            ],
        },
    ]

    for condition in conditions:
        for case in condition["testCases"]:
            inputValue = case[0]
            expectedResult = case[1]

            choice = {
                "Variable": "$.condition",
                "Next": "NextState",
            }
            choice[condition["conditionType"]] = condition["condition"]
            assert (
                choice_helper.isRightChoice(
                    choice,
                    {
                        "condition": inputValue,
                        "compareTo": condition.get("compareTo"),
                    },
                )
                == expectedResult
            )

    # when complex choice rule applied
    # with And
    choice = {
        "And": [
            {
                "Variable": "$.condition",
                "NumericLessThan": 5,
            },
            {
                "Variable": "$.condition",
                "NumericGreaterThan": 4,
            },
        ],
        "Next": "NextState",
    }

    assert choice_helper.isRightChoice(choice, {"condition": 4.5})

    assert not choice_helper.isRightChoice(choice, {"condition": 5.5})

    assert not choice_helper.isRightChoice(choice, {"condition": 0})

    # with Or
    choice = {
        "Or": [
            {
                "Variable": "$.condition",
                "NumericLessThan": 6,
            },
            {
                "Variable": "$.condition",
                "NumericLessThan": 5,
            },
        ],
        "Next": "NextState",
    }

    assert choice_helper.isRightChoice(choice, {"condition": 4.5})

    assert choice_helper.isRightChoice(choice, {"condition": 5.5})

    assert not choice_helper.isRightChoice(choice, {"condition": 7})

    # with Not
    choice = {
        "Not": {
            "Variable": "$.condition",
            "NumericLessThan": 5,
        },
        "Next": "NextState",
    }

    assert choice_helper.isRightChoice(choice, {"condition": 5.5})

    assert not choice_helper.isRightChoice(choice, {"condition": 4.5})
