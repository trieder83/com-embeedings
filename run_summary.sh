#!/bin/bash

#docker run -it --rm -p --name embedding embedding
volume=$PWD/data
DOCKER=docker

if [ ! -z $WINDIR ]; then
  #volume=c:\\temp\\data_mbart
  volume=c:\\temp\\data_nllb
  DOCKER="winpty podman"
fi

#$DOCKER run -p 8888:8888 -v $volume:/data -it localhost/trieder83/com-summary:gpu-0.2  flask --app createSummary_mBART.py run --host 0.0.0.0 --port 8888 
$DOCKER run -p 8888:8888 -v $volume:/data -it localhost/trieder83/com-summary:gpu-0.2  flask --app createSummary_nllb.py run --host 0.0.0.0 --port 8888 
