#!/bin/bash

echo $1

if [[ "$1" -eq "e" ]]; then
  curl http://127.0.0.1:5000/embedding -H "Content-Type: application/json" --request POST  --data '{"text":"I am the vector test"}'
fi

#curl http://127.0.0.1:5000/embedding -H "Content-Type: application/json" --request POST  --data '{"text":"Vector is a robot"}'

if [[ "$1" -eq "s" ]]; then
  curl -X POST http://127.0.0.1:5000/summarize -H "Content-Type: application/json" -d '{"text": "Das ist ein Beispieltext in deutscher Sprache. Dieses Beispiel enthält zehn Sätze für eine Zusammenfassung. Die mBART-Modellarchitektur wurde entwickelt, um in verschiedenen Sprachen zu arbeiten. Mit mBART kann Text in einer Sprache zusammengefasst oder in eine andere Sprache übersetzt werden. Modelle wie mBART helfen bei der Verarbeitung natürlicher Sprache auf globaler Ebene. Sie sind nützlich für mehrsprachige Anwendungen. We are the multilingual champions"}'
fi
