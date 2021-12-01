import re
import copy

from . import choice_helper
from . import jsonpath


class RunStateResult:
    def __init__(self, data, stateType, nextStateName, isTerminalState):
        if not nextStateName and not isTerminalState:
            raise Exception("Invalid result")

        self.isTerminalState = isTerminalState
        self.data = data
        self.stateType = stateType
        self.nextStateName = nextStateName

    def __eq__(self, other):
        return (
            self.isTerminalState == other.isTerminalState
            and self.data == other.data
            and self.nextStateName == other.nextStateName
            and self.stateType == other.stateType
        )

    def __repr__(self):
        return "stateType: {}, nextStateName: {}, isTermainalState: {}, data: {}".format(
            self.stateType,
            self.nextStateName,
            self.isTerminalState,
            self.data,
        )


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
        startAt = self.definition.get("StartAt")
        if not startAt:
            raise Exception("StartAt does not exist")

        result = self._run(input, startAt, None)
        print(result.data)
        return result

    def _run(self, data, current, end):
        result = self._runState(data, current)
        if result.isTerminalState or current == end:
            return result
        return self._runPartial(result.data, result.nextStateName, end)

    def _runPartial(self, data, current, end):
        result = self._runState(data, current)
        if result.isTerminalState or current == end:
            return result
        return self._runPartial(result.data, result.nextStateName, end)

    # experimental
    def _runCondition(self, data, _condition):
        condition = _condition
        result = self._runState(data, condition["start"])
        regex = condition.get("regex")
        if regex:
            regex = regex[1:-1]  # strip the slashes
        if result.isTerminalState or condition["start"] == condition.get("end") or (regex and not re.match(regex, result.nextStateName)):
            return result
        condition["start"] = result.nextStateName
        return self._runCondition(result.data, condition)

    def _runState(self, _data, stateName):
        data = copy.deepcopy(_data)
        state = self.definition["States"].get(stateName)
        if state is None:
            raise Exception("the state {} does not exists".format(stateName))

        stateType = state["Type"]
        nextState = state.get("Next")

        if stateType == "Task":
            resource = self.resources.get(state["Resource"])
            if resource is None:
                raise Exception("Unknown resource: {}".format(state["Resource"]))

            newValue = self._runStateTask(state, data, resource)
            if not state.get("ResultPath"):
                data = newValue
            else:
                jsonpath.set_json_value(data, state.get("ResultPath"), newValue)
        elif stateType == "Pass":
            newValue = self._runStatePass(state, data)
            jsonpath.set_json_value(data, state.get("ResultPath"), newValue)
        elif stateType == "Choice":
            nextState = self._runStateChoice(state, data)
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

    def _runStateTask(self, state, data, resource):
        dataInputPath = self.inputData(state, data)
        result = resource(dataInputPath)
        if not result:
            return None
        return copy.deepcopy(result)

    def _runStatePass(self, state, data):
        dataInputPath = self.inputData(state, data)
        return copy.deepcopy(state.get("Input", dataInputPath))

    def _runStateChoice(self, state, data):
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
