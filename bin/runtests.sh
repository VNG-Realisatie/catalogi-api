#!/bin/sh

set -e
set -x

python src/manage.py jenkins \
  --noinput \
  --project-apps-tests \
  --enable-coverage \
  --coverage-rcfile=setup.cfg
