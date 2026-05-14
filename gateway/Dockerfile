#Stage 1: Build
FROM python:3.12-slim AS build

WORKDIR /app

COPY ./gateway/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./gateway ./gateway
COPY ./models ./models
COPY ./protobuf_generated/inference ./protobuf_generated/inference
COPY ./protobuf_generated/generate_protos.sh ./protobuf_generated/generate_protos.sh

# This will print the entire structure of the /app folder to the build logs
RUN echo "--- DEPLOYMENT TREE ---" && find /app -maxdepth 3 -not -path '*/.*'

RUN bash ./protobuf_generated/generate_protos.sh

#Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=build /app /app

ENV FASTAPI_HOST=0.0.0.0

ENV FASTAPI_PORT=5000

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", ${FASTAPI_HOST}, "--port", ${FASTAPI_PORT}]