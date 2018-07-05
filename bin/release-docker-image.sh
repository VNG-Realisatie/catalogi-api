#!/bin/bash

set -e # exit on error
set -x # echo commands

CONTAINER_REPO=nlxio/gemma-ztc


git_tag=$(git tag --points-at HEAD) &>/dev/null


if [[ -n "$git_tag" ]]; then
    echo "Building image for git tag $git_tag"
    RELEASE_TAG=$git_tag
else
    RELEASE_TAG=${RELEASE_TAG:-latest}
fi


docker build \
    --target production \
    -t ${CONTAINER_REPO}:${RELEASE_TAG} \
    -f Dockerfile .


# JOB_NAME is set by Jenkins
# only push the image if running in CI
if [[ -n "$JOB_NAME" ]]; then
    docker push ${CONTAINER_REPO}:${RELEASE_TAG}

    # if on jenkins AND it's a tagged release -> prepare deployment
    if [[ -n "$JENKINS_URL" && -n "$git_tag" ]]; then
        echo "
VERSION=${git_tag}
" > deployment-parameters
    fi
else
    echo "Not pushing image, set the JOB_NAME envvar to push after building"
fi


# If on Jenkins, write the
