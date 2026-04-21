FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

#cache the downloaded package files, to avoid future downloads
RUN pip install -no-cache-dir -r requirements.txt

COPY . .

RUN sh generate_protos.sh

EXPOSE 50051

CMD ["python", "inference_server.py"]