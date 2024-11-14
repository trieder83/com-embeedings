#!/bin/sh
export FLASK_APP=./createEmbeddings2.py
#pipenv run flask --debug run -h 0.0.0.0

flask --app createEmbeddings2 run --host=0.0.0.0 --port 8888
#python $FLASK_APP
