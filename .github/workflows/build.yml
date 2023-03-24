name: build

on:
  push:
    tags:
      - "v*.*.*"
      - "*.*.*"

jobs:
  push-images:
    runs-on: ubuntu-latest
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
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
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
