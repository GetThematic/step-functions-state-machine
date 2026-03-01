#!/bin/bash
set -x
set -e
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
UV_PROJECT_ENVIRONMENT=env uv sync --group dev
