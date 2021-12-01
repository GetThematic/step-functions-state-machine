import pytest

import step_functions_local
from step_functions_local.state_machine import RunStateResult

from .utils import load_fixture, increment


def test_runCondition():
    definition = load_fixture("./fixtures/definitions/states-with-common-prefix.json", validate=False)
    state_machine = step_functions_local.StateMachine(definition, {"arn:aws:lambda:us-east-1:123456789012:function:Increment": increment})

    # with start and end
    # should run while the condition fulfills
    assert state_machine._runCondition({}, {"start": "main.initialize", "end": "main.check"}) == RunStateResult({"i": 1}, "Choice", "main.increment", False)

    # with start and regex
    # should run while the condition fulfills
    assert state_machine._runCondition({}, {"start": "main.initialize", "regex": "/main\.\w+/"}) == RunStateResult({"i": 3}, "Choice", "hoge", False)
