#Stage 1: Build 
FROM python:3.11-slim AS build

WORKDIR /app

COPY ./inference_worker/requirements.txt .

#cache the downloaded package files, to avoid future downloads
RUN pip install --no-cache-dir -r requirements.txt

COPY ./inference_worker ./inference_worker
COPY ./protobuf_generated/inference ./protobuf_generated/inference

# This will print the entire structure of the /app folder to the build logs
RUN echo "--- DEPLOYMENT TREE ---" && find /app -maxdepth 3 -not -path '*/.*'

RUN bash ./inference_worker/generate_protos.sh

#Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=build /app /app

EXPOSE 50051

CMD ["python", "-m", "inference_worker.inference_server"]