#!/bin/bash
set -e
cd "${BASH_SOURCE%/*}"

coverage run --source=step_functions_local -m pytest test && coverage report -m