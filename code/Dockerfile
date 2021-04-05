#
# Docker container for all of the COAL Application
#
# - runs all 4 servers (API, Game, Content, and Player)
#
# See:
#   - https://docs.docker.com/config/containers/multi-service_container/
#
# This is why I switched from Alpine to Debian:
#   - https://pythonspeed.com/articles/alpine-docker-python/
#   - https://pythonspeed.com/articles/base-image-python-docker-images/
#
FROM python:3.9-slim-buster

COPY /docker/scripts/install-packages.sh .
RUN ./install-packages.sh

WORKDIR /app
VOLUME /data

COPY /publish/* .
RUN    pip3 install --upgrade pip \
    && pip3 install wheel \
    && pip3 install connexion*.whl \
    && pip3 install coal*whl \
    && rm *whl

COPY /docker/*conf /config/
COPY /docker/scripts/run-all-servers.sh .


ENTRYPOINT [ "./run-all-servers.sh" ]