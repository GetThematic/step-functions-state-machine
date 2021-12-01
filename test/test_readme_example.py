import step_functions_local


def test_RunStateResult():
    # FakeStateMachine.run
    definition = {
        "Comment": "https://states-language.net/spec.html#data",
        "StartAt": "AddNumbers",
        "States": {
            "AddNumbers": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-1:123456789012:function:Add",
                "InputPath": "$.numbers",
                "ResultPath": "$.sum",
                "End": True,
            },
        },
    }
    step_functions_local.validate(definition)
    resources = {"arn:aws:lambda:us-east-1:123456789012:function:Add": lambda x: x["val1"] + x["val2"]}
    state_machine = step_functions_local.StateMachine(definition, resources)

    # should execute the state machine with fakeResource
    runStateResult = state_machine.run({"title": "Numbers to add", "numbers": {"val1": 3, "val2": 4}})

    assert runStateResult.data == {"title": "Numbers to add", "numbers": {"val1": 3, "val2": 4}, "sum": 7}
