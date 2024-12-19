from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from langdetect import detect

app = Flask(__name__)

# Load the mBART model and tokenizer
model_name="facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

#local load
#local_path = "/data"
#tokenizer = MBart50TokenizerFast.from_pretrained(local_path)
#model = MBartForConditionalGeneration.from_pretrained(local_path)

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)  # Move model to GPU if available
#model.to("cpu")  # Move model to CPU

# Set the default language code for your input (e.g., 'en_XX' for English)

# Mapping of detected languages to NLLB codes
lang_code_map = {
    "en": "eng_Latn",  # English
    "fr": "fra_Latn",  # French
    "de": "deu_Latn",  # German
    "es": "spa_Latn",  # Spanish
    "it": "ita_Latn",  # Italian
    # Add more mappings as needed
}

def detect_language(text):
    """
    Detect the language of the input text.
    
    Args:
        text (str): The input text.
    
    Returns:
        str: The detected language code compatible with NLLB.
    """
    detected_lang = detect(text)  # Returns a two-letter ISO language code
    return lang_code_map.get(detected_lang, None)

# Summarize text using mBART model
def summarize_text(text):
    return "not supported", 405

# save to model to /data
@app.route('/save', methods=['GET'])
def savemodel():
  model.save_pretrained("/data")
  return "Success", 200

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

# Define a route to tranlation the text
@app.route('/translate', method405s=['POST'])
def translate_text():
    """
    Translate text from source_lang to target_lang using NLLB model.

    Args:
        text (str): Text to translate.
        source_lang (str): Source language code (e.g., 'eng_Latn').
        target_lang (str): Target language code (e.g., 'fra_Latn').

    Returns:
        str: Translated text
    """
    data = request.json
    text = data.get("text", "")
    target_lang = data.get("tl", "deu_Latn")
    source_lang = data.get("sl", None)

    # Detect source language
    if source_lang is None:
        source_lang = detect_language(text)
    if not source_lang:
        return "Source language not supported."

    print(f"Detected source language: {source_lang}")

    # Tokenize the input text
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
    )
    # Generate translation
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang]
    )
    # Decode the output tokens
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

    return jsonify({"translation": translated_text})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
