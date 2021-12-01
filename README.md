# Step functions state machine
Validates and can run a AWS State Language state machine (used in step functions) locally as a single process.

State machine runner is a port from https://github.com/oshikiri/fake-step-functions
Validation schemas are from https://github.com/ChristopheBougere/asl-validator


## Known limitations
### Choices
 * We treat all date strings like timestamps (i.e. if it is a date 2016-01-01 it will be treated as being at 0:00 on that date)
 * We don't distinguish between a variable in the json data being null and not present