#!/usr/bin/env bash
#
# Code generation
#

docker run --rm -v "$(pwd):/local" -u "$(id -u):$(id -g) openapitools/openapi-generator-cli generate \
    --input-spec /local/public-schema/openapi.yaml \
    --generator-name python-flask \
    --output /local/public-schema-server
