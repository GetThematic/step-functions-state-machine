import copy

from . import choice_helper
from . import jsonpath


class RunStateResult:
    def __init(self, data, stateType, nextState, isTerminalState):
        self.isTerminalState = isTerminalState
        self.isTerminalState = data
        self.stateType = stateType
        self.nextStateName = nextState


class StateMachine:
    startAt = "initialState"

    def __init__(self, definition, resources):
        """
        definition: the asl definition
        resources: a map of string to class for resources
        """
        self.definition = definition
        self.resources = resources

    def run(self, input):
        return self._run(input, self.startAt, None)

    def _run(self, data, current, end):
        result = self._runState(data, current)
        if result.isTerminalState or current == end:
            return result
        return self.runPartial(result.data, result.nextStateName, end)

    # experimental
    def runCondition(self, data, _condition):
        condition = _condition
        result = self.runState(data, condition["start"])
        if result.isTerminalState or condition["start"] == condition["end"] or not result.nextStateName.match(condition.regex):
            return result
        condition.start = result.nextStateName
        return self.runCondition(result.data, condition)

    def runState(self, _data, stateName):
        data = copy.deepcopy(_data)
        state = self.definition.States.get(stateName)
        if state is None:
            raise Exception("the state {} does not exists".format(stateName))

        stateType = state["Type"]
        nextState = state.get("Next")

        if stateType == "Task":
            resource = self.fakeResources.get(state["Resource"])
            if resource is None:
                raise Exception("Unknown resource: {}".format(state["Resource"]))

            newValue = self.runStateTask(state, data, resource)
            if not state.get["ResultPath"]:
                data = newValue
            else:
                jsonpath.set_json_value(data, state.get["ResultPath"], newValue)
        elif stateType == "Pass":
            newValue = self.runStatePass(state, data)
            jsonpath.set_json_value(data, state.get["ResultPath"], newValue)
        elif stateType == "Choice":
            nextState = self.runStateChoice(state, data)
        elif stateType == "Succeed":
            pass
        elif stateType == "Fail":
            pass
        elif stateType == "Wait":
            pass
        elif stateType == "Parallel":
            pass
        else:
            raise Exception("Invalid Type: {}".format(stateType))

        isTerminalState = state.get("End") or stateType == "Succeed" or stateType == "Fail"

        return RunStateResult(data, stateType, nextState, isTerminalState)

    def runStateTask(self, state, data, resource):
        dataInputPath = self.inputData(state, data)
        result = resource(dataInputPath)
        if not result:
            return None
        return copy.deepcopy(result)

    def runStatePass(self, state, data):
        dataInputPath = self.inputData(state, data)
        return copy.deepcopy(state.get("Input", dataInputPath))

    def runStateChoice(self, state, data):
        matched = [x for x in state["Choices"] if choice_helper.isRightChoice(x, data)]
        if matched:
            return matched[0]["Next"]
        return state["Default"]

    def inputData(self, state, data):
        if state["Type"] == "Pass":
            if "Result" in state:
                return state["Result"]
        elif state["Type"] == "Task":
            if "Input" in state:
                return state["Input"]

        if "Parameters" in state:
            rawParameters = state["Parameters"]
            return self.resolveParameters(rawParameters, data)

        if "InputPath" not in state:
            return copy.deepcopy(data)
        elif not state["InputPath"]:
            return {}
        else:
            return jsonpath.get_json_value(data, state["InputPath"])

    def resolveParameters(self, rawParameters, data):
        if type(rawParameters) == list:
            return [self.resolveParameters(x, data) for x in rawParameters]
        resolvedParameters = {}

        for key, rawValue in rawParameters.items():
            if key.endswith(".$"):
                key = key[:-2]
                resolvedParameters[key] = jsonpath.get_json_value(data, rawValue)
            elif type(rawValue) in {list, dict}:
                resolvedParameters[key] = self.resolveParameters(rawValue, data)
            else:
                resolvedParameters[key] = rawValue
        return resolvedParameters
