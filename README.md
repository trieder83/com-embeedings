Model Test
============


## run flask 
`flask --app createEmbeddings2 run`
# --host=0.0.0.0
`curl http://127.0.0.1:5000/embedding -H "Content-Type: application/json" --request POST  --data '{"text":"xyz"}'`

## local model store
`find ~/.cache/huggingface/hub/`

`python3 -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./app/artefacts")'`


DB 
==================
* solr support no multivalued fields in 9.7
* chromadb may be limited in scaling
* pinecone is online
* milvus might be the solution for billions of embeddings
