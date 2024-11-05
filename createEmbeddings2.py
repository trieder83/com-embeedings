from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import nltk
import os
# used to build only - homedir nltk_data
# nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize


from flask import Flask
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/embedding',methods=['GET', 'POST'])
def get_embedding():
    embeddings = []
    data = request.json
    if not isinstance(data['text'], str):
        raise TypeError("Input should be a string")
    for sentence in sent_tokenize(data['text']):
        embedding = createEmbedding(sentence)
        #print(sentence)
        #print(get_embedding)
        embeddings.append(embedding.numpy().tolist() )
    #return jsonify(embedding)
    #print(embeddings)
    #return embedding
    #return jsonify( embeddings.numpy().tolist() )
    return jsonify( embeddings )

#print(torch.cuda.is_available())
#x = torch.rand(5, 3)
#print(x)

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


# disable cuda for testing
#device = torch.device("cpu")
device = torch.device("cuda")
# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2', device)

def createEmbedding(sentences):
  # Tokenize sentences
  encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt' )

  # Compute token embeddings
  with torch.no_grad():
      model_output = model(**encoded_input)

  # Perform pooling
  sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

  # Normalize embeddings
  sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
  return sentence_embeddings

#print("Sentence embeddings:")
#print(sentence_embeddings)
