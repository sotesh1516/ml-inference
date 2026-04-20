# ML Inference System

This project consists of:
    - a REST API gateway
    - a gRPC-based inference service

Each application runs its Python virtual environment for modularity. 

---

## Run Order

1. Start inference service (gRPC server)
2. Start gateway (REST API)

---

### Inference Service

#### Setup Python environment and packages

```bash
cd inference_worker
python -m venv inference_worker_venv
source inference_worker_venv/bin/activate
pip install -r requirements.txt
```

---

#### Generate client and server Python code

Note: Run protobuf generation from project root.

```bash
python -m grpc_tools.protoc \
  -I./protos \
  --python_out=./protobuf_generated \
  --grpc_python_out=./protobuf_generated \
  --pyi_out=./protobuf_generated \
  ./protos/inference.proto
```

---

#### Start gRPC server

```bash
source inference_worker_venv/bin/activate
python grpc_server.py
```

---

### Gateway

#### Setup Pyhon environment and packages

```bash
cd gateway
python -m venv gateway_venv
source gateway_venv/bin/activate
pip install -r requirements.txt
```

---

#### Start REST API

```bash
source gateway_venv/bin/activate
python app.py
```