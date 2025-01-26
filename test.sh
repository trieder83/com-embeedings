#!/bin/bash

HEADER='-H "Content-Type: application/json" -H "Accept: application/json"'

#curl -X POST http://127.0.0.1:8888/summarize -H "Content-Type: application/json" -d '{"text":"The supply is getting low—when’s the next shipment arriving? Keep it discreet", "source_language":"en"}'
curl -X POST http://127.0.0.1:8888/summarize $HEADER -d '{"text":"The supply is getting low—when’s the next shipment arriving? Keep it discreet. Last time, you drew too much attention to the spot. Prices are up this week; clients aren'\''t happy, but they'\''ll come around. I’ve got a new contact asking for weight, but I don’t know if I can trust him yet. Take the back route and don’t leave a trail; there are eyes everywhere. Money'\''s been short lately; we'\''re taking too many risks without enough payoff. Let’s switch the meeting location every few days to keep it unpredictable. If we get busted, remember—you don’t know anything about me. Make sure the product’s cut right this time; no complaints from the regulars. He’s trying to move in on our turf; we need to set some boundaries.", "source_language":"en"}'
#curl -X POST http://127.0.0.1:8888/summarize -H "Content-Type: application/json" -d '{"text":"A: The supply is getting low—when’s the next shipment arriving? B: Keep it discreet. Last time, you drew too much attention to the spot. A: Prices are up this week; clients aren'\''t happy, but they'\''ll come around. B: I’ve got a new contact asking for weight, but I don’t know if I can trust him yet. A: Take the back route and don’t leave a trail; there are eyes everywhere. B: Money'\''s been short lately; we'\''re taking too many risks without enough payoff. A: Let’s switch the meeting location every few days to keep it unpredictable. B: If we get busted, remember—you don’t know anything about me. A: Make sure the product’s cut right this time; no complaints from the regulars. B: He’s trying to move in on our turf; we need to set some boundaries.", "source_language":"en"}'
#curl -X POST http://127.0.0.1:8888/translate -H "Content-Type: application/json" -d '{"tl":"de_DE","text":"The supply is getting low—when’s the next shipment arriving? Keep it discreet. Last time, you drew too much attention to the spot. Prices are up this week; clients aren'\''t happy, but they'\''ll come around. I’ve got a new contact asking for weight, but I don’t know if I can trust him yet. Take the back route and don’t leave a trail; there are eyes everywhere. Money'\''s been short lately; we'\''re taking too many risks without enough payoff. Let’s switch the meeting location every few days to keep it unpredictable. If we get busted, remember—you don’t know anything about me. Make sure the product’s cut right this time; no complaints from the regulars. He’s trying to move in on our turf; we need to set some boundaries.", "source_language":"en"}'
time curl -X POST http://127.0.0.1:8888/translate $HEADER -d '{"tl":"de_DE","text":"The supply is getting low—when’s the next shipment arriving? Keep it discreet. Last time, you drew too much attention to the spot"}'
time curl -X POST http://127.0.0.1:8888/translate $HEADER -d '{"tl":"fr_XX","text":"The supply is getting low—when’s the next shipment arriving? Keep it discreet. Last time, you drew too much attention to the spot"}'
exit 0
echo $1



if [[ "$1" -eq "e" ]]; then
  curl http://127.0.0.1:8888/embedding -H "Content-Type: application/json" --request POST  --data '{"text":"I am the vector test"}'
fi

#curl http://127.0.0.1:8888/embedding -H "Content-Type: application/json" --request POST  --data '{"text":"Vector is a robot"}'

if [[ "$1" -eq "s" ]]; then
  curl -X POST http://127.0.0.1:8888/summarize -H "Content-Type: application/json" -d '{"text": "Das ist ein Beispieltext in deutscher Sprache. Dieses Beispiel enthält zehn Sätze für eine Zusammenfassung. Die mBART-Modellarchitektur wurde entwickelt, um in verschiedenen Sprachen zu arbeiten. Mit mBART kann Text in einer Sprache zusammengefasst oder in eine andere Sprache übersetzt werden. Modelle wie mBART helfen bei der Verarbeitung natürlicher Sprache auf globaler Ebene. Sie sind nützlich für mehrsprachige Anwendungen. We are the multilingual champions"}'
fi

if [[ "$1" -eq "l" ]]; then
  curl -X POST http://127.0.0.1:8888/summarize -H "Content-Type: application/json" -d '{"text":"The supply is getting low—when’s the next shipment arriving? Keep it discreet. Last time, you drew too much attention to the spot. Prices are up this week; clients aren'\''t happy, but they'\''ll come around. I’ve got a new contact asking for weight, but I don’t know if I can trust him yet. Take the back route and don’t leave a trail; there are eyes everywhere. Money'\''s been short lately; we'\''re taking too many risks without enough payoff. Let’s switch the meeting location every few days to keep it unpredictable. If we get busted, remember—you don’t know anything about me. Make sure the product’s cut right this time; no complaints from the regulars. He’s trying to move in on our turf; we need to set some boundaries.", "source_language":"en"}'
fi

if [[ "$1" -eq "c" ]]; then
  curl -X POST http://127.0.0.1:8888/summarize -H "Content-Type: application/json" -d '{"text":"A: The supply is getting low—when’s the next shipment arriving? B: Keep it discreet. Last time, you drew too much attention to the spot. A: Prices are up this week; clients aren'\''t happy, but they'\''ll come around. B: I’ve got a new contact asking for weight, but I don’t know if I can trust him yet. A: Take the back route and don’t leave a trail; there are eyes everywhere. B: Money'\''s been short lately; we'\''re taking too many risks without enough payoff. A: Let’s switch the meeting location every few days to keep it unpredictable. B: If we get busted, remember—you don’t know anything about me. A: Make sure the product’s cut right this time; no complaints from the regulars. B: He’s trying to move in on our turf; we need to set some boundaries.", "source_language":"en"}'
fi


# windows
curl -X POST http://172.18.0.119:8888/translate -H 'Content-Type: application/json' --data '@test'

curl -X POST http://localhost:8888/translate -H 'Content-Type: application/json' --data '@test'
