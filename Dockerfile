# FROM python:3
# FROM python:3.8-slim
FROM pytorch/pytorch

	
WORKDIR /usr/src/app

# Set environment variables.
ENV PORT 8888
ENV HOST 0.0.0.0

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt bootstrap.sh ./

USER 1001:1001

#RUN conda install pytorch torchvision cudatoolkit=10.0 -c pytorch && \
RUN pip install --no-cache-dir -r requirements.txt && \
    python3 -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./app/artefacts")' && \
    python3 ./createEmbeddings2.py
#    huggingface-cli login --token xxx && \

COPY . .

#CMD [ "python", "./createEmbeddings2.py" ]
#CMD [ flask, --app, createEmbeddings2, "run"]
CMD [ ./"bootstrap.sh"]
