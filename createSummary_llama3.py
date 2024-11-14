from flask import Flask, request, jsonify
#from transformers import LlamaForCausalLM, LlamaTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM
from airllm import AutoModel
import torch
from torch.cuda.amp import autocast

app = Flask(__name__)

# Load the LLaMA model and tokenizer (assuming a multilingual version with German output)
#model_path = "path/to/local/llama"
#model_name = "openlm-research/llama-3b"  # Replace with the actual model name (hypothetical for LLaMA 3.2 1.23B)
#model_name = "meta-llama/Llama-3.2-1B"  # Replace with the actual model name (hypothetical for LLaMA 3.2 1.23B)

# Load model directly
# meta-llama/Llama-3.2-1B-Instruct
#tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
#model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
#model = AutoModel.from_pretrained("mlx-community/Llama-3.2-3B-Instruct-4bit")


#tokenizer = LlamaTokenizer.from_pretrained(model_name)
#model = LlamaForCausalLM.from_pretrained(model_name)

# Check if CUDA is available and set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#device = torch.device("cpu")
model.to(device)

# Set pad_token_id to eos_token_id to handle padding correctly
#model.config.pad_token_id = model.config.eos_token_id
model.config.pad_token_id = None
#model.config.eos_token_id = '<end>'

# Function to summarize text with LLaMA and set output to German
def summarize_text(text, source_language):
    print("summarize_text")
    #text += ' <end>'
    #torch.cuda.empty()
    # Prepare the prompt based on the input language
    if source_language == "en":
        prompt = f"Summarize the following text in German: {text}"
    elif source_language == "ru":
        prompt = f"Суммируйте следующий текст на немецком языке: {text}"
    else:
        prompt = f"Fasse den folgenden Text auf Deutsch zusammen: {text}"

    prompt = f"Fasse den folgenden Text auf Deutsch, mit maximal 2 Sätzen zusammen: {text}"
    prompt = f"Please summarize the following text in German (short and concise):\n{text}"
    prompt = f"Summarize the following text in German: {text}"
    prompt = f"Who is the drug suplier, A or B: {text}"

    # Tokenize and move input to device
    #input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    # Limit the text length to 512 tokens
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True )
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # Generate the summary with LLaMA
    summary_ids = model.generate(
        input_ids,
        attention_mask=attention_mask,
        #max_length=512,
        max_new_tokens=80,
        min_length=20,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
        do_sample=False  # Disable sampling for deterministic output
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Define a route to summarize the text
@app.route('/summarize', methods=['POST'])
def summarize():
    print("summarize")
    data = request.json
    text = data.get("text", "")
    source_language = data.get("source_language", "en")  # Default to English if not specified

    # Validate input
    if not text:
        return jsonify({"error": "No text provided"}), 400
    if source_language not in ["en", "ru"]:
        return jsonify({"error": "Unsupported language"}), 400

    # Generate summary
    summary = summarize_text(text, source_language)
    return jsonify({"summary": summary})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
