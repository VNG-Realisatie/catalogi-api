#!/bin/sh

set -e
set -x

cd src
python manage.py jenkins \
  --noinput \
  --project-apps-tests \
  --enable-coverage \
  --coverage-rcfile=setup.cfg
