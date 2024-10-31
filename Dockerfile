FROM python:3

WORKDIR /usr/src/app

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    python3 -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./app/artefacts")'
#    huggingface-cli login --token xxx && \

COPY . .

CMD [ "python", "./createEmbeddings.py" ]
