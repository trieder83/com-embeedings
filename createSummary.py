from flask import Flask, request, jsonify
from transformers import MT5ForConditionalGeneration, MT5Tokenizer
import torch

app = Flask(__name__)

# Load the mT5 model and tokenizer
model_name = "google/mt5-small"
tokenizer = MT5Tokenizer.from_pretrained(model_name)
model = MT5ForConditionalGeneration.from_pretrained(model_name)

# Summarize text using mT5 model
def summarize_text(text):
    # Preprocess input text
    input_ids = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)

    # Generate summary
    summary_ids = model.generate(input_ids, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
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
