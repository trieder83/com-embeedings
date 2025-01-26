from flask import Flask, request, jsonify
#from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoProcessor, SeamlessM4Tv2Model
#from transformers import SeamlessM4TForTextToText
import torch
from langdetect import detect
#import torchaudio
import logging

app = Flask(__name__)

# debug
#logging.basicConfig(level=logging.DEBUG)

# Load the nllb model and tokenizer
model_name="facebook/seamless-m4t-v2-large"

#tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")


#local load
local_path = "./data/seamelessm4t"
#tokenizer = AutoTokenizer.from_pretrained(local_path, token=True)
#model = AutoModelForSeq2SeqLM.from_pretrained(local_path, token=True)

# Check if CUDA is available
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#model.to(device)  # Move model to GPU if available
#model.to("cpu")  # Move model to CPU

# Set the default language code for your input (e.g., 'en_XX' for English)

# Mapping of detected languages to NLLB codes / BCP-47
lang_code_map = {
    "af": "afr",  # Afrikaans
    "am": "amh",  # Amharic
    "ar": "arb",  # Modern Standard Arabic
    "ary": "ary", # Moroccan Arabic
    "arz": "arz", # Egyptian Arabic
    "as": "asm",  # Assamese
    "ast": "ast", # Asturian
    "az": "azj",  # North Azerbaijani
    "be": "bel",  # Belarusian
    "bn": "ben",  # Bengali
    "bs": "bos",  # Bosnian
    "bg": "bul",  # Bulgarian
    "ca": "cat",  # Catalan
    "ceb": "ceb", # Cebuano
    "cs": "ces",  # Czech
    "ckb": "ckb", # Central Kurdish
    "zh": "cmn",  # Mandarin Chinese (Simplified)
    "zh-Hant": "cmn_Hant",  # Mandarin Chinese (Traditional)
    "cy": "cym",  # Welsh
    "da": "dan",  # Danish
    "de": "deu",  # German
    "el": "ell",  # Greek
    "en": "eng",  # English
    "et": "est",  # Estonian
    "eu": "eus",  # Basque
    "fi": "fin",  # Finnish
    "fr": "fra",  # French
    "ff": "fuv",  # Nigerian Fulfulde
    "om": "gaz",  # West Central Oromo
    "ga": "gle",  # Irish
    "gl": "glg",  # Galician
    "gu": "guj",  # Gujarati
    "he": "heb",  # Hebrew
    "hi": "hin",  # Hindi
    "hr": "hrv",  # Croatian
    "hu": "hun",  # Hungarian
    "hy": "hye",  # Armenian
    "ig": "ibo",  # Igbo
    "id": "ind",  # Indonesian
    "is": "isl",  # Icelandic
    "it": "ita",  # Italian
    "jv": "jav",  # Javanese
    "ja": "jpn",  # Japanese
    "kam": "kam", # Kamba
    "kn": "kan",  # Kannada
    "ka": "kat",  # Georgian
    "kk": "kaz",  # Kazakh
    "kea": "kea", # Kabuverdianu
    "mn": "khk", # Halh Mongolian
    "km": "khm",  # Khmer
    "ky": "kir",  # Kyrgyz
    "ko": "kor",  # Korean
    "lo": "lao",  # Lao
    "lt": "lit",  # Lithuanian
    "lb": "ltz",  # Luxembourgish
    "lg": "lug",  # Ganda
    "luo": "luo", # Luo
    "lv": "lvs",  # Standard Latvian
    "mai": "mai", # Maithili
    "ml": "mal",  # Malayalam
    "mr": "mar",  # Marathi
    "mk": "mkd",  # Macedonian
    "mt": "mlt",  # Maltese
    "mni": "mni", # Meitei
    "my": "mya",  # Burmese
    "nl": "nld",  # Dutch
    "nn": "nno",  # Norwegian Nynorsk
    "nb": "nob",  # Norwegian Bokmål
    "ne": "npi",  # Nepali
    "ny": "nya",  # Nyanja
    "oc": "oci",  # Occitan
    "or": "ory",  # Odia
    "pa": "pan",  # Punjabi
    "ps": "pbt",  # Southern Pashto
    "fa": "pes",  # Western Persian
    "pl": "pol",  # Polish
    "pt": "por",  # Portuguese
    "ro": "ron",  # Romanian
    "ru": "rus",  # Russian
    "sk": "slk",  # Slovak
    "sl": "slv",  # Slovenian
    "sn": "sna",  # Shona
    "sd": "snd",  # Sindhi
    "so": "som",  # Somali
    "es": "spa",  # Spanish
    "sr": "srp",  # Serbian
    "sv": "swe",  # Swedish
    "sw": "swh",  # Swahili
    "ta": "tam",  # Tamil
    "te": "tel",  # Telugu
    "tg": "tgk",  # Tajik
    "tl": "tgl",  # Tagalog
    "th": "tha",  # Thai
    "tr": "tur",  # Turkish
    "uk": "ukr",  # Ukrainian
    "ur": "urd",  # Urdu
    "uz": "uzn",  # Northern Uzbek
    "vi": "vie",  # Vietnamese
    "xh": "xho",  # Xhosa
    "yo": "yor",  # Yoruba
    "yue": "yue", # Cantonese
    "zlm": "zlm", # Colloquial Malay
    "ms": "zsm",  # Standard Malay
    "zu": "zul"   # Zulu
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
  tokenizer.save_pretrained(local_path)
  model.save_pretrained(local_path)
  return "Success", 200

@app.route('/healthcheck')
def health_check():
    return 'This node is healthy'

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
    """
    Translate text from source_lang to target_lang using NLLB model.

    Args:
        text (str): Text to translate.
        source_lang (str): Source language code (e.g., 'eng_Latn').
        target_lang (str): Target language code (e.g., 'fra_Latn').

    Returns:
        str: Translated text
    """
    #data = request.json
    data = request.get_json(force=True)
    text = data.get("text", "")
    target_lang = data.get("tl", "deu_Latn")
    source_lang = data.get("sl", None)

    # Detect source language
    if source_lang is None:
        source_lang = detect_language(text)
        print(f"Auto detected source language: {source_lang}")
    else:
        # if BCP-47 code
        if len(source_lang) == 2:
           source_lang = lang_code_map.get(source_lang, None)
        print(f"Specified source language: {source_lang}")
    if not source_lang:
        return "Source language not supported."

    # Ensure target language is valid
    #if f"<{target_lang}>" not in tokenizer.lang_tokens:
    #    return jsonify({"error": f"Unsupported target language: {target_lang}"}), 400

    print(f"source lang {source_lang}")
    print(f"target lang {target_lang}")
    print(f"input text. {text}")

    # Tokenize the input text
    text_inputs = processor(text, src_lang=source_lang, return_tensors="pt")
    output_tokens = model.generate(**text_inputs, tgt_lang=target_lang, generate_speech=False)
    translated_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)

    return jsonify({"translation": translated_text})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
