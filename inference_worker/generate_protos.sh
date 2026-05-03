#!/bin/bash
# This script generates the gRPC Python code from the .proto file
# It should be run from the root of the project

# Paths relative to the container root
PROTO_ROOT="/app/protobuf_generated/inference"
PROTO_FILE="$PROTO_ROOT/inference.proto"
OUTPUT_DIR="$PROTO_ROOT"

# Check if the .proto file exists
if [ ! -f "$PROTO_FILE" ]; then
    echo "Error: $PROTO_FILE not found!"
    exit 1
fi 



# Generate the gRPC code
python -m grpc_tools.protoc -I. --python_out="$OUTPUT_DIR" --grpc_python_out="$OUTPUT_DIR" "$PROTO_FILE"