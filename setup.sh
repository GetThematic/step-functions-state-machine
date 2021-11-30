#!/bin/bash
set -x
set -e
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
virtualenv --python python3 env
source env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

