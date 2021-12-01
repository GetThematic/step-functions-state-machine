import pytest

from step_functions_local.state_machine import RunStateResult


# RunStateResult
def test_RunStateResult():
    # should be able to compare
    r1 = RunStateResult({}, "Task", "NextState", False)
    r2 = RunStateResult({}, "Task", "NextState", False)
    assert r1 == r2

    with pytest.raises(Exception):
        RunStateResult({}, "Task", None, False)
