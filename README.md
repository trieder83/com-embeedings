Model Test
============


## run flask 
flask --app createEmbeddings2 run

## local model store
`find ~/.cache/huggingface/hub/`

`python3 -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./app/artefacts")'`
