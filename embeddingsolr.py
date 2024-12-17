import asyncio
#from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from flask import Flask
from flask import Flask, jsonify, request

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define the chunking parameters
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=int(os.environ.get("CHUNK_SIZE", 100)),  # Max tokens per chunk
    chunk_overlap=int(os.environ.get("CHUNK_OVERLAP", 3)),  # Overlap to ensure continuity between chunks
    separators=["\n\n", "\n", " ", ""]  # Break on paragraphs, sentences, words
)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/healthcheck')
def health_check():
    return 'This node is healthy'


#model = SentenceTransformer("all-MiniLM-L6-v2")  # beerere multilantuage
#model.save("./data","all-MiniLM-L6-v2-local")

#Load the model from the local path
model = SentenceTransformer("/data")

# pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
#dense_model = models.Dense(
#    in_features=pooling_model.get_sentence_embedding_dimension(),
#    out_features=368,
#    activation_function=nn.Tanh(),
#)


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

