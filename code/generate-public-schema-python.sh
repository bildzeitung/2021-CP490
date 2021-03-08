#!/usr/bin/env bash
#
# Code generation
#
docker run --rm -v "$(pwd):/local" openapitools/openapi-generator-cli generate \
    --input-spec /local/public-schema/openapi.yaml \
    --generator-name python \
    --output /local/public-schema-client
