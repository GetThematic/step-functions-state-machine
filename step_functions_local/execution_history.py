from enum import Enum
import datetime


class EventType(Enum):
    ActivityFailed = "ActivityFailed"
    ActivityScheduled = "ActivityScheduled"
    ActivityScheduleFailed = "ActivityScheduleFailed"
    ActivityStarted = "ActivityStarted"
    ActivitySucceeded = "ActivitySucceeded"
    ActivityTimedOut = "ActivityTimedOut"
    ChoiceStateEntered = "ChoiceStateEntered"
    ChoiceStateExited = "ChoiceStateExited"
    ExecutionAborted = "ExecutionAborted"
    ExecutionFailed = "ExecutionFailed"
    ExecutionStarted = "ExecutionStarted"
    ExecutionSucceeded = "ExecutionSucceeded"
    ExecutionTimedOut = "ExecutionTimedOut"
    FailStateEntered = "FailStateEntered"
    LambdaFunctionFailed = "LambdaFunctionFailed"
    LambdaFunctionScheduled = "LambdaFunctionScheduled"
    LambdaFunctionScheduleFailed = "LambdaFunctionScheduleFailed"
    LambdaFunctionStarted = "LambdaFunctionStarted"
    LambdaFunctionStartFailed = "LambdaFunctionStartFailed"
    LambdaFunctionSucceeded = "LambdaFunctionSucceeded"
    LambdaFunctionTimedOut = "LambdaFunctionTimedOut"
    MapIterationAborted = "MapIterationAborted"
    MapIterationFailed = "MapIterationFailed"
    MapIterationStarted = "MapIterationStarted"
    MapIterationSucceeded = "MapIterationSucceeded"
    MapStateAborted = "MapStateAborted"
    MapStateEntered = "MapStateEntered"
    MapStateExited = "MapStateExited"
    MapStateFailed = "MapStateFailed"
    MapStateStarted = "MapStateStarted"
    MapStateSucceeded = "MapStateSucceeded"
    ParallelStateAborted = "ParallelStateAborted"
    ParallelStateEntered = "ParallelStateEntered"
    ParallelStateExited = "ParallelStateExited"
    ParallelStateFailed = "ParallelStateFailed"
    ParallelStateStarted = "ParallelStateStarted"
    ParallelStateSucceeded = "ParallelStateSucceeded"
    PassStateEntered = "PassStateEntered"
    PassStateExited = "PassStateExited"
    SucceedStateEntered = "SucceedStateEntered"
    SucceedStateExited = "SucceedStateExited"
    TaskFailed = "TaskFailed"
    TaskScheduled = "TaskScheduled"
    TaskStarted = "TaskStarted"
    TaskStartFailed = "TaskStartFailed"
    TaskStateAborted = "TaskStateAborted"
    TaskStateEntered = "TaskStateEntered"
    TaskStateExited = "TaskStateExited"
    TaskSubmitFailed = "TaskSubmitFailed"
    TaskSubmitted = "TaskSubmitted"
    TaskSucceeded = "TaskSucceeded"
    TaskTimedOut = "TaskTimedOut"
    WaitStateAborted = "WaitStateAborted"
    WaitStateEntered = "WaitStateEntered"
    WaitStateExited = "WaitStateExited"


EVENT_TYPE_TO_DETAILS_MAP = {
    EventType.ActivityFailed: "activityFailedEventDetails",
    EventType.ActivityScheduled: "activityScheduledEventDetails",
    EventType.ActivityScheduleFailed: "activityScheduleFailedEventDetails",
    EventType.ActivityStarted: "activityStartedEventDetails",
    EventType.ActivitySucceeded: "activitySucceededEventDetails",
    EventType.ActivityTimedOut: "activityTimedOutEventDetails",
    EventType.ChoiceStateEntered: "stateEnteredEventDetails",
    EventType.ChoiceStateExited: "stateExitedEventDetails",
    EventType.ExecutionAborted: "executionAbortedEventDetails",
    EventType.ExecutionFailed: "executionFailedEventDetails",
    EventType.ExecutionStarted: "executionStartedEventDetails",
    EventType.ExecutionSucceeded: "executionSucceededEventDetails",
    EventType.ExecutionTimedOut: "executionTimedOutEventDetails",
    EventType.FailStateEntered: "stateEnteredEventDetails",
    EventType.LambdaFunctionFailed: "executionTimedOutEventDetails",
    EventType.LambdaFunctionScheduled: "lambdaFunctionScheduledEventDetails",
    EventType.LambdaFunctionScheduleFailed: "lambdaFunctionScheduleFailedEventDetails",
    EventType.LambdaFunctionStarted: None,
    EventType.LambdaFunctionStartFailed: "lambdaFunctionStartFailedEventDetails",
    EventType.LambdaFunctionSucceeded: "lambdaFunctionSucceededEventDetails",
    EventType.LambdaFunctionTimedOut: "lambdaFunctionTimedOutEventDetails",
    EventType.MapIterationAborted: "mapIterationAbortedEventDetails",
    EventType.MapIterationFailed: "mapIterationFailedEventDetails",
    EventType.MapIterationStarted: "mapIterationStartedEventDetails",
    EventType.MapIterationSucceeded: "mapIterationSucceededEventDetails",
    EventType.MapStateAborted: None,
    EventType.MapStateEntered: "stateEnteredEventDetails",
    EventType.MapStateExited: "stateExitedEventDetails",
    EventType.MapStateFailed: None,
    EventType.MapStateStarted: None,
    EventType.MapStateSucceeded: None,
    EventType.ParallelStateAborted: None,
    EventType.ParallelStateEntered: "stateEnteredEventDetails",
    EventType.ParallelStateExited: "stateExitedEventDetails",
    EventType.ParallelStateFailed: None,
    EventType.ParallelStateStarted: None,
    EventType.ParallelStateSucceeded: None,
    EventType.PassStateEntered: "stateEnteredEventDetails",
    EventType.PassStateExited: "stateExitedEventDetails",
    EventType.SucceedStateEntered: "stateEnteredEventDetails",
    EventType.SucceedStateExited: "stateExitedEventDetails",
    EventType.TaskFailed: "taskFailedEventDetails",
    EventType.TaskScheduled: "taskScheduledEventDetails",
    EventType.TaskStarted: "taskStartedEventDetails",
    EventType.TaskStartFailed: "taskStartFailedEventDetails",
    EventType.TaskStateAborted: None,
    EventType.TaskStateEntered: "stateEnteredEventDetails",
    EventType.TaskStateExited: "stateExitedEventDetails",
    EventType.TaskSubmitFailed: "taskSubmitFailedEventDetails",
    EventType.TaskSubmitted: "taskSubmittedEventDetails",
    EventType.TaskSucceeded: "taskSucceededEventDetails",
    EventType.TaskTimedOut: "taskTimedOutEventDetails",
    EventType.WaitStateAborted: None,
    EventType.WaitStateEntered: "stateEnteredEventDetails",
    EventType.WaitStateExited: "stateExitedEventDetails",
}


class ExecutionHistory(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.execution_history = []

    def record(self, event_type, event_details, previous_event_id=None):
        event_detail_type = EVENT_TYPE_TO_DETAILS_MAP[event_type]
        # handle unknown previous event
        if previous_event_id is None:
            previous_event_id = 0
            if len(self.execution_history):
                previous_event_id = self.execution_history[-1]["id"]
        details = {
            "timestamp":  datetime.datetime.now(datetime.UTC).timestamp(),
            "id": len(self.execution_history) + 1,
            "type": event_type.value,
            "previousEventId": previous_event_id,
        }
        if event_detail_type:
            details[event_detail_type] = event_details
        self.execution_history.append(details)

    def export(self):
        return self.execution_history
