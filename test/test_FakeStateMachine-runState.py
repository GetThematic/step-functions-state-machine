import pytest

import step_functions_local
from step_functions_local.state_machine import RunStateResult
from step_functions_local.validate import validate

from .utils import load_fixture, add_numbers


# state_machine#runState()
def test_runstate():
    # when the specified stateName does not exists
    # should throw an Error
    definition = load_fixture("./fixtures/definitions/startat-does-not-exist.json", validate=False)
    state_machine = step_functions_local.StateMachine(definition, {})

    with pytest.raises(Exception):
        state_machine._runState(
            {
                "a1": 123,
            },
            "Target",
        )

    # when the state has `"End": True`
    # should be marked as a terminal state
    definition = load_fixture("./fixtures/definitions/state-with-end-is-True.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine._runState(
        {
            "a1": 123,
        },
        "Target",
    ).isTerminalState

    # when the state contains "Next" field
    # should return the state with results and "Next" destination
    definition = load_fixture("./fixtures/definitions/state-with-next-property.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert (
        state_machine._runState(
            {
                "a1": 123,
            },
            "Target",
        ).nextStateName
        == "NextState"
    )

    # when the state does not contain "Next" field and does not have `"End": True`
    # should throw an error
    definition = load_fixture("./fixtures/definitions/state-without-next-and-end.json", validate=False)
    state_machine = step_functions_local.StateMachine(definition, {})

    with pytest.raises(Exception):
        state_machine._runState(
            {
                "a1": 123,
            },
            "Target",
        )

    # when the state has `"Type": "Succeed"`
    # should not change the state and return it
    definition = load_fixture("./fixtures/definitions/succeed.json")
    state_machine = step_functions_local.StateMachine(definition, {})

    assert state_machine._runState({sum: 7}, "Target") == RunStateResult({sum: 7}, "Succeed", None, True)

    # when the state has `"Type": "Fail"`
    # should not change the state and return it
    definition = load_fixture("./fixtures/definitions/fail.json")
    state_machine = step_functions_local.StateMachine(definition, {})

    assert state_machine._runState({sum: 7}, "Target") == RunStateResult({sum: 7}, "Fail", None, True)

    # when the state has `"Type": "Choice"`
    # when Choices contains only one element
    def create_machine():
        choice = {
            "Variable": "$.condition",
            "BooleanEquals": True,
            "Next": "NextState",
        }

        definition = {
            "States": {
                "Choices": {
                    "Type": "Choice",
                    "Choices": [choice],
                    "Default": "DefaultState",
                },
            },
        }

        return step_functions_local.StateMachine(definition, {})

    # should select next state if condition is met
    state_machine = create_machine()
    assert state_machine._runState({"condition": True}, "Choices") == RunStateResult(
        {
            "condition": True,
        },
        "Choice",
        "NextState",
        False,
    )

    state_machine = create_machine()
    assert state_machine._runState({"condition": False}, "Choices") == RunStateResult(
        {
            "condition": False,
        },
        "Choice",
        "DefaultState",
        False,
    )

    # when Choices contains more than one element
    # should select the asserted state as a next state
    definition = load_fixture("./fixtures/definitions/choice-more-than-one-choice.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine._runState({"condition1": False, "condition2": True}, "Choices") == RunStateResult(
        {
            "condition1": False,
            "condition2": True,
        },
        "Choice",
        "NextState2",
        False,
    )

    # when the state has `"Type": "Pass"`
    # when there is an Input field
    # should fill outputPath using Input field
    definition = load_fixture("./fixtures/definitions/pass-input-to-resultpath.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine._runState({"a1": 123}, "Target") == RunStateResult(
        {
            "a1": 123,
            "a2": 123,
        },
        "Pass",
        "NextState",
        False,
    )

    # when the state has an InputPath field
    # when the InputPath is undefined
    # should fill outputPath using the whole data (i.e. $)
    definition = load_fixture("./fixtures/definitions/pass-inputpath-is-undefined.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine._runState({"a1": 123}, "Target") == RunStateResult(
        {
            "a1": 123,
            "a2": {"a1": 123},
        },
        "Pass",
        "NextState",
        False,
    )

    # when the state contains Result
    # should fill the content of Result to ResultPath
    definition = load_fixture("./fixtures/definitions/pass-result-to-resultpath.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine._runState({"a1": 123}, "Target") == RunStateResult(
        {
            "a1": 123,
            "a2": "a",
        },
        "Pass",
        "NextState",
        False,
    )

    # when the InputPath is None
    # should fill outputPath using {}
    definition = load_fixture("./fixtures/definitions/task-inputpath-is-none.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine._runState({"a1": 123}, "Target") == RunStateResult(
        {
            "a1": 123,
            "a2": {},
        },
        "Pass",
        "NextState",
        False,
    )

    # when the InputPath is non-None
    # should fill outputPath using InputPath field
    definition = load_fixture("./fixtures/definitions/task-inputpath-to-outputpath.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine._runState({"a1": 123}, "Target") == RunStateResult(
        {
            "a1": 123,
            "a2": 123,
        },
        "Pass",
        "NextState",
        False,
    )

    # when the InputPath points a path like $.a.b3.c2
    # should parse the InputPath correctly
    definition = load_fixture("./fixtures/definitions/task-complex-inputpath-and-outputpath.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine._runState({"a": {"b1": "a-b1", "b2": {"c1": "a-b2-c1"}, "b3": {"c1": "a-b3-c1"}}}, "Target") == RunStateResult(
        {
            "a": {
                "b1": "a-b1",
                "b2": {"c1": "a-b2-c1"},
                "b3": {"c1": "a-b3-c1", "c2": "a-b2-c1"},
            },
        },
        "Pass",
        "NextState",
        False,
    )

    # when the state has `"Type": "Task"`
    resources = {
        "arn:aws:lambda:us-east-1:123456789012:function:Add": add_numbers,
        "arn:aws:lambda:us-east-1:123456789012:function:AddAsync": add_numbers,
        "arn:aws:lambda:us-east-1:123456789012:function:Double": lambda x: 2 * x,
        "arn:aws:lambda:us-east-1:123456789012:function:Identity": lambda x: x,
    }
    # when there is an InputPath field
    # should pass the specified subset to the Resource
    definition = load_fixture("./fixtures/definitions/task-inputpath.json")
    state_machine = step_functions_local.StateMachine(definition, resources)
    assert state_machine._runState({"numbers": {"val1": 3, "val2": 4}}, "Target") == RunStateResult(
        {
            "numbers": {"val1": 3, "val2": 4},
            "sum": 7,
        },
        "Task",
        "NextState",
        False,
    )

    # when the fakeResource is an async function
    # should pass the specified subset to the Resource
    definition = load_fixture("./fixtures/definitions/task-addasync.json")
    state_machine = step_functions_local.StateMachine(definition, resources)
    assert state_machine._runState({"numbers": {"val1": 3, "val2": 4}}, "Add") == RunStateResult(
        {
            "numbers": {"val1": 3, "val2": 4},
            "sum": 7,
        },
        "Task",
        None,
        True,
    )

    # when the InputPath points a path like $.a.b3.c2
    # should pass the specified subset to the Resource
    definition = load_fixture("./fixtures/definitions/task-complex-inputpath.json")
    state_machine = step_functions_local.StateMachine(definition, resources)
    assert state_machine._runState({"a": {"b3": {"c2": {"val1": 3, "val2": 4}}}}, "Target") == RunStateResult(
        {
            "a": {
                "b3": {
                    "c2": {"val1": 3, "val2": 4},
                },
            },
            "sum": 7,
        },
        "Task",
        "NextState",
        False,
    )

    # when the Task state is called without InputPath
    # should pass $ to the Resource
    definition = load_fixture("./fixtures/definitions/task-without-input.json")
    state_machine = step_functions_local.StateMachine(definition, resources)
    assert state_machine._runState({"val1": 3, "val2": 4}, "Target") == RunStateResult(
        {
            "val1": 3,
            "val2": 4,
            "sum": 7,
        },
        "Task",
        "NextState",
        False,
    )

    # when the Task state is called with Input
    # should pass the Input to the Resource
    definition = load_fixture("./fixtures/definitions/task-input-to-resource.json")
    state_machine = step_functions_local.StateMachine(definition, resources)
    assert state_machine._runState({"input": 3}, "Target") == RunStateResult(
        {
            "input": 3,
            "result": 6,
        },
        "Task",
        "NextState",
        False,
    )

    # when the Task state does not contain ResultPath
    # should use the default value ResultPath=`$`
    definition = load_fixture("./fixtures/definitions/task-resultpath-is-undefined.json")
    state_machine = step_functions_local.StateMachine(definition, resources)
    assert state_machine._runState({}, "Target") == RunStateResult(
        {
            "a": 1,
            "b": 2,
        },
        "Task",
        "NextState",
        False,
    )

    # when the Task state contains an unknown fake resource
    # should raise an error
    definition = load_fixture("./fixtures/definitions/task-unknown-resource.json")
    state_machine = step_functions_local.StateMachine(definition, resources)
    with pytest.raises(Exception):
        state_machine._runState({}, "Target")

    # when the Task state contains a Parameters property
    # should pass the specified parameters
    definition = load_fixture("./fixtures/definitions/parameter-property.json")
    input = None

    def save_input(event):
        nonlocal input
        input = event
        return event["input"]["val1"] + event["input"]["val2"]

    state_machine = step_functions_local.StateMachine(definition, {"arn:aws:lambda:us-east-1:123456789012:function:saveInput": save_input})

    actual = state_machine._runState({"a": 2, "b": {"c": {"val2": 4}}}, "Target")
    assert input == {
        "input": {"val1": 3, "val2": 4},
        "arrayInput": [
            {"val1": 3, "val2": 4},
            {"val1": 4, "val2": 3},
        ],
    }

    assert actual.data == {
        "a": 2,
        "b": {
            "c": {"val2": 4},
        },
        "result": 7,
    }
