# OpenAPI Notes

## Docker image

For the Python client code generation:

```
docker pull openapitools/openapi-generator-cli
```

For combining all of the OpenAPI files into one:
```
  ; cd ../dockerfiles
  ; docker build . -t swagger-cli
```

## Reference material
- Formal specification: http://spec.openapis.org/oas/v3.0.3
- Nice-looking specification: https://swagger.io/specification
- Tutorial-level: https://swagger.io/docs/specification/basic-structure
- Code generation tool: https://openapi-generator.tech/docs/installation

## Otherl link
- DRY-ing up OpenAPI: https://davidgarcia.dev/posts/how-to-split-open-api-spec-into-multiple-files/
