name: ci

on:
  push:
    branches:
      - "develop"
  pull_request:
    branches:
      - "develop"
      - "master"

env:
  DJANGO_SETTINGS_MODULE: ztc.conf.ci
  SECRET_KEY: dummy
  DB_USER: postgres
  DB_PASSWORD: ''
  DEPLOYMENT: ztc

jobs:
  check-sort:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements/ci.txt
      - name: Run isort
        run: isort --check-only --diff .

  check-format:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements/ci.txt
      - name: Run black
        run: black --check --diff src docs

  check-oas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Use Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
      - name: Install spectral
        run: npm install -g @stoplight/spectral@5.9.2
      - name: Run OAS linter
        run: spectral lint ./src/openapi.yaml

  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        postgres: ['10', '11', '12']

    name: unit-test @postgres ${{ matrix.postgres }}

    services:
      postgres:
        image: postgres:${{ matrix.postgres }}
        env:
          POSTGRES_HOST_AUTH_METHOD: trust
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - uses: actions/setup-node@v3
        with:
          node-version: '16'

      # - name: Install system packages
      #   run: sudo apt-get install libgdal-dev gdal-bin

      - name: Install dependencies
        run: pip install -r requirements/ci.txt

      - name: Build frontend
        run: |
          npm ci
          npm run build
      - name: Run tests
        run: |
          python src/manage.py collectstatic --noinput --link
          coverage run src/manage.py test ztc
          coverage xml

  push-images:
    runs-on: ubuntu-latest
    needs:
      - check-format
      - check-sort
      - check-oas
      - unit-tests
    steps:
      -
        name: Checkout
        uses: actions/checkout@v3
      -
        name: Docker meta
        id: meta
        uses: docker/metadata-action@v4
        with:
          # list of Docker images to use as base name for tags
          images: |
            ghcr.io/VNG-Realisatie/catalogi-api
          # generate Docker tags based on the following events/attributes
          tags: |
            type=ref,event=pr
            type=ref,event=branch
            type=sha
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      -
        name: Log in to github
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GHCR_TOKEN }}

      -
        name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
