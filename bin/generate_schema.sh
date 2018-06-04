#!/bin/bash

# Run this script from the root of the repository

if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "You need to activate your virtual env before running this script"
    exit 1
fi

src/manage.py generate_swagger \
    ./src/swagger2.0.json \
    --overwrite \
    --format=json
