import pytest

import step_functions_local
from step_functions_local.state_machine import RunStateResult

from .utils import load_fixture


def test_runPartial():
    definition = load_fixture("./fixtures/definitions/many-states.json", validate=False)
    state_machine = step_functions_local.StateMachine(definition, {})
    # should execute states between the start state and the end state
    assert state_machine._runPartial({"title": "run-partial"}, "Pass1", "Pass2") == RunStateResult(
        {
            "title": "run-partial",
            "p1": "b",
            "p2": "c",
        },
        "Pass",
        "Pass3",
        False,
    )
