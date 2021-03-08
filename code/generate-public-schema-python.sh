#!/usr/bin/env bash
#
# Code generation
#

docker run --rm -u "$(id -u):$(id -g)" \
    -v "$(pwd):/local" \
    openapitools/openapi-generator-cli \
    generate \
    --input-spec /local/public-schema/openapi.yaml \
    --generator-name python-flask \
    --output /local/public-schema-server \
    --additional-properties=packageName=coal_public_api_server
