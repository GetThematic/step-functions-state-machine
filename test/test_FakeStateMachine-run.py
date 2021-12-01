import pytest

import step_functions_local
from step_functions_local.state_machine import RunStateResult

from .utils import load_fixture, add_numbers, increment


def test_run():
    # when StartAt field does not exist
    # should throw an Error
    definition = load_fixture("./fixtures/definitions/startat-field-does-not-exist.json", validate=False)
    state_machine = step_functions_local.StateMachine(definition, {})
    with pytest.raises(Exception):
        state_machine.run({})

    # should pass the input to fakeResource and fill the result to ResultPath
    definition = load_fixture("./fixtures/definitions/add.json")
    resources = {
        "arn:aws:lambda:us-east-1:123456789012:function:Add": add_numbers,
    }
    state_machine = step_functions_local.StateMachine(definition, resources)

    assert state_machine.run({"title": "Numbers to add", "numbers": {"val1": 3, "val2": 4}}) == RunStateResult(
        {
            "title": "Numbers to add",
            "numbers": {"val1": 3, "val2": 4},
            "sum": 7,
        },
        "Task",
        None,
        True,
    )

    # when there is invalid Type String
    # should throw an Error
    definition = load_fixture("./fixtures/definitions/unknown-type.json", validate=False)
    state_machine = step_functions_local.StateMachine(definition, {})

    with pytest.raises(Exception):
        state_machine.run({})

    # when the state machine has two states
    # should return the result successfully
    definition = load_fixture("./fixtures/definitions/two-states.json")
    resources = {
        "arn:aws:lambda:us-east-1:123456789012:function:Add": add_numbers,
    }
    state_machine = step_functions_local.StateMachine(definition, resources)

    assert state_machine.run({"title": "Numbers to add", "numbers": {"val1": 3, "val2": 4}}) == RunStateResult(
        {
            "title": "Numbers to add",
            "numbers": {"val1": 3, "val2": 4},
            "sum1": 7,
            "sum2": 7,
        },
        "Task",
        None,
        True,
    )

    # when state machine contains a loop with break
    # should return the result successfully
    definition = load_fixture("./fixtures/definitions/loop.json")
    resources = {
        "arn:aws:lambda:us-east-1:123456789012:function:Increment": increment,
    }
    state_machine = step_functions_local.StateMachine(definition, resources)
    assert state_machine.run({"i": 0}) == RunStateResult(
        {
            "i": 3,
        },
        "Succeed",
        None,
        True,
    )

    # when the state updates a copied field
    # should not affect the original field
    definition = load_fixture("./fixtures/definitions/copy-object.json")
    state_machine = step_functions_local.StateMachine(definition, {})
    assert state_machine.run({"a1": {"b": 1}}) == RunStateResult(
        {
            "a1": {"b": 1},
            "a2": {"b": 1},
        },
        "Succeed",
        None,
        True,
    )
