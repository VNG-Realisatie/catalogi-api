#!/bin/bash

set -e  # exit on errors
set -x  # echo commands

if [[ -z "$WORKSPACE" ]]; then
    export WORKSPACE=$(pwd)
fi

# use the Jenkins specific override
cp bin/docker-compose.override.yml docker-compose.override.yml

docker-compose \
    -p ztc_tests \
    build tests

docker-compose \
    -p ztc_tests \
    run tests

# cleanup
git reset --hard
