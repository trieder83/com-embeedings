from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch
from langdetect import detect

app = Flask(__name__)

# Load the mBART model and tokenizer
#model_name = "facebook/mbart-large-50"
#model_name = "facebook/mbart-large-50-many-to-one-mmt"
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)  # Move model to GPU if available
#model.to("cpu")  # Move model to CPU

# Set the default language code for your input (e.g., 'en_XX' for English)
source_language = "en_XX"  # Adjust based on input language

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
        #num_beams=4,
        num_beams=8,
        early_stopping=True,
        #decoder_start_token_id=tokenizer.lang_code_to_id["de_DE"],  # German language code
        forced_bos_token_id=tokenizer.lang_code_to_id["de_DE"],
        no_repeat_ngram_size=2,  # Prevent repeating n-grams (e.g., 2-grams, 3-grams)
        top_p=0.9,  # Nucleus sampling to allow diverse but high-probability tokens
        temperature=0.7,  # Lower temperature to make the generation less random and avoid repetition
        do_sample=False  # Disable sampling to make output deterministic
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# save to model to /data
@app.route('/save', methods=['GET'])
def savemodel():
  model.save_pretrained("./data")
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
@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get("text", "")
    target_language = data.get("tl", "en_XX")
    source_language = data.get("sl", None)

    # Load the model and tokenizer

    # Detect source language if not provided
    if not source_language:
        detected_lang = detect(text)
        source_language = detected_lang.replace('-', '_') + '_XX'
        print(f"Detected source language: {detected_lang}")

    # Set tokenizer source and target language
    tokenizer.src_lang = source_language
    tokenizer.tgt_lang = target_language

    # Tokenize the input text and move tensors to the same device as the model
    inputs = tokenizer(text, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Generate translation
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_language])
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

    return jsonify({"translation": translated_text})



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
