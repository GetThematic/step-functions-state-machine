#!/bin/bash
set -e
cd "${BASH_SOURCE%/*}"

nosetests --with-xunit --with-coverage --cover-xml --cover-inclusive \
    --cover-package=thematic_actions \
    --cover-erase \
    . -s -v