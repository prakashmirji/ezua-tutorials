FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

COPY src/requirements.txt src/requirements.txt
RUN pip install --upgrade pip && pip install --default-timeout=600 -r src/requirements.txt

RUN pip install chromadb==0.4.15

COPY src/model.py src/model.py
COPY src/encoder.py src/encoder.py

RUN chmod -R 777 /workspace/src

WORKDIR /workspace/src
ENTRYPOINT ["python", "model.py", "--persist-dir", ".", "--model-path", "."]
