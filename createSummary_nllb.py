from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from langdetect import detect
import logging

app = Flask(__name__)

# debug
#logging.basicConfig(level=logging.DEBUG)

# Load the nllb model and tokenizer
model_name="facebook/nllb-200-distilled-600M"
#tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

#local load
local_path = "/data/"
tokenizer = AutoTokenizer.from_pretrained(local_path, token=True)
model = AutoModelForSeq2SeqLM.from_pretrained(local_path, token=True)

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)  # Move model to GPU if available
#model.to("cpu")  # Move model to CPU

# Set the default language code for your input (e.g., 'en_XX' for English)

# Mapping of detected languages to NLLB codes / BCP-47
lang_code_map = {
    "en": "eng_Latn",  # English
    "fr": "fra_Latn",  # French
    "de": "deu_Latn",  # German
    "es": "spa_Latn",  # Spanish
    "it": "ita_Latn",  # Italian
    "zh": "zho_Hans",  # Simplified Chinese
    "zh-Hant": "zho_Hant",  # Traditional Chinese
    "ja": "jpn_Jpan",  # Japanese
    "ko": "kor_Hang",  # Korean
    "ru": "rus_Cyrl",  # Russian
    "ar": "arb_Arab",  # Arabic (Standard)
    "pt": "por_Latn",  # Portuguese
    "nl": "nld_Latn",  # Dutch
    "sv": "swe_Latn",  # Swedish
    "no": "nob_Latn",  # Norwegian Bokmål
    "da": "dan_Latn",  # Danish
    "fi": "fin_Latn",  # Finnish
    "cs": "ces_Latn",  # Czech
    "pl": "pol_Latn",  # Polish
    "hu": "hun_Latn",  # Hungarian
    "bg": "bul_Cyrl",  # Bulgarian
    "ro": "ron_Latn",  # Romanian
    "uk": "ukr_Cyrl",  # Ukrainian
    "el": "ell_Grek",  # Greek
    "hi": "hin_Deva",  # Hindi
    "bn": "ben_Beng",  # Bengali
    "ta": "tam_Taml",  # Tamil
    "te": "tel_Telu",  # Telugu
    "ml": "mal_Mlym",  # Malayalam
    "gu": "guj_Gujr",  # Gujarati
    "mr": "mar_Deva",  # Marathi
    "ur": "urd_Arab",  # Urdu
    "vi": "vie_Latn",  # Vietnamese
    "th": "tha_Thai",  # Thai
    "id": "ind_Latn",  # Indonesian
    "ms": "zsm_Latn",  # Malay
    "tl": "tgl_Latn",  # Tagalog
    "sw": "swh_Latn",  # Swahili
    "yo": "yor_Latn",  # Yoruba
    "ig": "ibo_Latn",  # Igbo
    "ha": "hau_Latn",  # Hausa
    "am": "amh_Ethi",  # Amharic
    "fa": "pes_Arab",  # Persian
    "he": "heb_Hebr",  # Hebrew
    "tr": "tur_Latn",  # Turkish
    "az": "azj_Latn",  # Azerbaijani
    "kk": "kaz_Cyrl",  # Kazakh
    "uz": "uzn_Latn",  # Uzbek
    "ky": "kir_Cyrl",  # Kyrgyz
    "pa": "pan_Guru",  # Punjabi
    "si": "sin_Sinh",  # Sinhala
    "my": "mya_Mymr",  # Burmese
    "lo": "lao_Laoo",  # Lao
    "km": "khm_Khmr",  # Khmer
    "bg": "bul_Cyrl",  # Bulgarian
    "sl": "slv_Latn",  # Slovenian
    "sk": "slk_Latn",  # Slovak
    "lt": "lit_Latn",  # Lithuanian
    "lv": "lvs_Latn",  # Latvian
    "et": "est_Latn",  # Estonian
    "is": "isl_Latn",  # Icelandic
    "ga": "gle_Latn",  # Irish
    "cy": "cym_Latn",  # Welsh
    "mt": "mlt_Latn",  # Maltese
    "af": "afr_Latn",  # Afrikaans
    "xh": "xho_Latn",  # Xhosa
    "zu": "zul_Latn",  # Zulu
    "st": "sot_Latn",  # Sotho
    "tn": "tsn_Latn",  # Tswana
    "ts": "tso_Latn",  # Tsonga
    "ve": "ven_Latn",  # Venda
    "nr": "nbl_Latn",  # Southern Ndebele
    "ss": "ssw_Latn",  # Swazi
    "hy": "hye_Armn", # Armeenian
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

    if source_lang is not None:
        text = f"<{source_lang}> {text}"

    print(f"input text. {text}")

    # Tokenize the input text
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding=False,
    )
    #print(f"input token count: {len(inputs)}")

    # Set the forced_bos_token_id for the target language
    print(f"target language: <{target_lang}>")
    #forced_bos_token_id = tokenizer.convert_tokens_to_ids(f"<{target_lang}>")
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(f"{target_lang}")

    # Generate translation
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id
    )

    # Decode the output tokens
    #translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

    return jsonify({"translation": translated_text})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
