#!/bin/bash

#docker build --tag 'trieder83/com-summary:gpu-0.2' -f Dockerfile_summary .
podman build --tag 'trieder83/com-translate:gpu-0.2' -f Dockerfile_translate.
