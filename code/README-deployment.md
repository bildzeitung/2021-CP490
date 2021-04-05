# Deploying COAL

COAL can be deployed as a monolithic Docker container.

Run:

```
  make clean docker
```

This will save out a Docker image that can be deployed arbitrarily.


## Running

Use something like this:

```
#!/bin/bash -ex

sudo docker run --rm \
        -d \
        --name coal \
        -p 8000:8000 \
        -p 3000:3000 \
        -v $(pwd)/dbs:/data \
        -u "$(id -u):$(id -g)" \
        --env-file /home/opc/.env \
        coal
```

* port 8000 is the proxy (API) server
* port 3000 is the Slack integration bot
* virtual directory mount /data is for SQLite DBs and slack cache
