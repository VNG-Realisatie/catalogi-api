#!/bin/bash

set -u

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

release_tag=$1
do_deploy=$2
shift

JOB_NAME=push ./bin/release-docker-image.sh $release_tag


deploy() {
    set +x

    # Trigger deploy
    curl https://deploy-bot-zgw.vng.cloud/api/v1/deployments \
        -H "Authorization: Token ${DEPLOY_BOT_TOKEN}" \
        -H "Content-Type: application/json" \
        --request POST \
        --data @- << EOF
{
    "name":"${DEPLOYMENT}",
    "namespace":"zgw",
    "containerName":"${DEPLOYMENT}",
    "image": "vngr/catalogi-api:${release_tag}"
}
EOF
    set -x

    echo "Deploy triggered"
}


if [[ $do_deploy == "yes" ]]; then
    deploy
fi
