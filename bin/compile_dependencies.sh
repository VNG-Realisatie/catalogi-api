#!/bin/bash

#
# Compile the dependencies for production, CI and development.
#
# Usage, in the root of the project:
#
#     ./bin/compile_dependencies.sh
#
# Any extra flags/arguments passed to this wrapper script are passed down to pip-compile.
# E.g. to update a package:
#
#     ./bin/compile_dependencies.sh --upgrade-package django

set -ex

toplevel=$(git rev-parse --show-toplevel)

cd $toplevel

export CUSTOM_COMPILE_COMMAND="./bin/compile_dependencies.sh"

# Base deps
pip-compile \
    --no-emit-index-url \
    --allow-unsafe \
    "$@" \
    requirements/base.in

# Production deps
pip-compile \
    --no-emit-index-url \
    --allow-unsafe \
    --output-file requirements/production.txt \
    "$@" \
    requirements/base.txt \
    requirements/production.in

# Dev deps
pip-compile \
    --no-emit-index-url \
    --allow-unsafe \
    --output-file requirements/dev.txt \
    "$@" \
    requirements/base.txt \
    requirements/testing.in \
    requirements/dev.in

# CI deps
pip-compile \
    --no-emit-index-url \
    --allow-unsafe \
    --output-file requirements/ci.txt \
    "$@" \
    requirements/base.txt \
    requirements/testing.in \
    requirements/ci.in
