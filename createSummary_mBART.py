from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch

app = Flask(__name__)

# Load the mBART model and tokenizer
model_name = "facebook/mbart-large-50"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)  # Move model to GPU if available

# Set the default language code for your input (e.g., 'en_XX' for English)
source_language = "de_XX"  # Adjust based on input language
#target_language = "de_DE"
target_language = "de_XX"

# Summarize text using mBART model
def summarize_text(text):
    # Tokenize and set the source language for mBART
    input_ids = tokenizer(text, return_tensors="pt", max_length=512, truncation=True).input_ids.to(device)
    tokenizer.src_lang = source_language

    # Generate summary
    summary_ids = model.generate(
        input_ids,
        max_length=80,
        min_length=20,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Define a route to summarize the text
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get("text", "")

    # Validate input
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Generate summary
    summary = summarize_text(text)
    return jsonify({"summary": summary})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
