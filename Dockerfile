# FROM python:3
FROM python:3.8-slim
#FROM pytorch/pytorch
#FROM nvidia/cuda:12.1.1-runtime-ubuntu20.04
#FROM nvidia/cuda:12.6.2-base-ubuntu22.04


# Set environment variables.
ENV PORT 8888
ENV HOST 0.0.0.0

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#RUN apt-get update && \
#    apt-get install -y python3-pip python3-dev && \
#    rm -rf /var/lib/apt/lists/* && \
RUN    mkdir /app && \
    mkdir /.local && \
    chown 1001:1001 /app /.local

#COPY requirements.txt ./

#USER 1001:1001
WORKDIR /app
COPY . .

#RUN conda install pytorch torchvision cudatoolkit=10.0 -c pytorch && \
#RUN pip install torch --index-url https://download.pytorch.org/whl/cpu && \
RUN pip install --no-cache-dir -r requirements.txt && \
  python3 -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./app/artefacts")'
#RUN python3 ./createEmbeddings2.py
#RUN python3 ./embeddingsolr.py
#    huggingface-cli login --token xxx && \

#CMD [ "python", "./createEmbeddings2.py" ]
#CMD [ flask, --app, createEmbeddings2, "run"]
CMD [ flask, --app, embeddingsolr.py, "run"]
#CMD [ ./"bootstrap.sh"]
