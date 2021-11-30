#!/bin/bash
set -e
cd "${BASH_SOURCE%/*}"

nosetests --with-xunit --with-coverage --cover-xml --cover-inclusive \
    --cover-package=step_functions_local \
    --cover-erase \
    . -s -v