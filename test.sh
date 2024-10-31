#!/bin/sh

curl http://127.0.0.1:5000/embedding -H "Content-Type: application/json" --request POST  --data '{"text":"I am the vector test"}'

#curl http://127.0.0.1:5000/embedding -H "Content-Type: application/json" --request POST  --data '{"text":"Vector is a robot"}'
