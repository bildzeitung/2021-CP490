#
# Docker container for all of the COAL Application
#
# - runs all 4 servers (API, Game, Content, and Player)
#
# See:
#   - https://docs.docker.com/config/containers/multi-service_container/
#
FROM python:3.9-alpine

WORKDIR /app
VOLUME /data

COPY /publish/* .
RUN    pip3 install --upgrade pip \
    && pip3 install connexion*.whl \
    && pip3 install coal*whl

COPY /docker/*conf /config/
COPY /docker/scripts/run-all-servers.sh .


ENTRYPOINT [ "./run-all-servers.sh" ]