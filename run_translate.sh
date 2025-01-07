#!/bin/bash

set -x 
#docker run -it --rm -p --name embedding embedding
#volume=$PWD/data
volume=$PWD/data_nllb
DOCKER=docker
volume=c:\\git\\a\\com-embeedings\\data_nllb
scriptvolume=c:\\git\\a\\com-embeedings

if [ ! -z $WINDIR ]; then
  #volume=c:\\temp\\data_mbart
  #volume=c:\\temp\\data_nllb
  DOCKER="winpty podman"
fi

#$DOCKER run -p 8888:8888 -v $volume:/data -it localhost/trieder83/com-summary:gpu-0.2  flask --app createSummary_mBART.py run --host 0.0.0.0 --port 8888 
#$DOCKER run -v $volume:/data -v $scriptvolume:/app -it localhost/trieder83/com-summary:gpu-0.2  sh -c "ls /data"
#$DOCKER run -p 8888:8888 -v $volume:/data -v $scriptvolume:/app -it localhost/trieder83/com-summary:gpu-0.2  flask --app createSummary_nllb.py run --host 0.0.0.0 --port 8888 
$DOCKER run --device nvidia.com/gpu=all --security-opt=label=disable -p 8888:8888 -v $volume:/data -v $scriptvolume:/app -it localhost/trieder83/com-transate:gpu-0.2  flask --app createSummary_nllb.py run --host 0.0.0.0 --port 8888 
