# Dockerfile to build image for swagger/openAPI tools
#
# see: https://github.com/APIDevTools/swagger-cli
# and: https://davidgarcia.dev/posts/how-to-split-open-api-spec-into-multiple-files/
#
# It seems like connexion and client generator dislike multiple files, so
# using this tool is our way of generating the necessary single YAML file.
#
FROM node:latest

RUN npm install -g @apidevtools/swagger-cli

ENTRYPOINT [ "swagger-cli" ]
