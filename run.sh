#!/bin/bash

#docker run -it --rm -p --name embedding embedding
volume=$PWD/data
DOCKER=docker

if [ ! -z $WINDIR ]; then
  volume=c:\\temp\\data
  DOCKER="winpty podman"
fi
#docker run -p 8888:8888 -it embeddings:latest flask --app createEmbeddings2 run --host 0.0.0.0 --port 8888 -v $volume:/data
docker run -p 8888:8888  -it embeddings:latest flask --app embeddingsolr.py run --host 0.0.0.0 --port 8888 

#$DOCKER run -p 8888:8888 -v $volume:/data -it embeddings:latest flask --app embeddingsolr.py run --host 0.0.0.0 --port 8888 
#$DOCKER run -p 8888:8888 -v $volume:/data -it docker.io/trieder83/com-summary:gpu-0.1  flask --app createSummary_mBART.py run --host 0.0.0.0 --port 8888 
