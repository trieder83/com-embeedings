import asyncio
#from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from flask import Flask
from flask import Flask, jsonify, request

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define the chunking parameters
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # Max tokens per chunk
    chunk_overlap=50,  # Overlap to ensure continuity between chunks
    separators=["\n\n", "\n", " ", ""]  # Break on paragraphs, sentences, words
)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/healthcheck')
def health_check():
    return 'This node is healthy'


model = SentenceTransformer("all-MiniLM-L6-v2")  # beerere multilantuage

@app.route('/embedding',methods=['GET', 'POST'])
def get_embedding():
    split = 300
    embeddings = []
    data = request.json
    if not isinstance(data['text'], str):
        raise TypeError("Input should be a string")
    if split < len(data['text']):
            chunks = text_splitter.split_text(data['text'])
            embedding = createEmbedding(chunks)
            #print(embeddings)
            embeddings.append(embedding.tolist() )
    else:
        embedding = createEmbedding(data['text'])
        print(embedding)
        embeddings.append(embedding.tolist() )
    #return jsonify(embedding)
    #print(embeddings)
    #return embedding
    #return jsonify( embeddings.numpy().tolist() )
    return jsonify( {"embeddings": embeddings })

def createEmbedding(sentences):
  # Tokenize sentences

  # Compute token embeddings
  #embeddings = model.encode(sentences,prompt_name="fact")
  embeddings = model.encode(sentences)

  # Perform pooling - applied by default

  # Normalize embeddings
  return embeddings

