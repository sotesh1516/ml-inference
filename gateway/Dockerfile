FROM python:3.12-slim

WORKDIR /app

ENV FASTAPI_HOST=0.0.0.0

ENV FASTAPI_PORT=5000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", ${FASTAPI_HOST}, "--port", ${FASTAPI_PORT}]