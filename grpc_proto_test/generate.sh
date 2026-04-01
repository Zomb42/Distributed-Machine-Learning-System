#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROTO_FILE="$ROOT_DIR/proto/connection.proto"

protoc \
  -I "$ROOT_DIR/proto" \
  --python_out="$SCRIPT_DIR" \
  --grpc_out="$SCRIPT_DIR" \
  --plugin=protoc-gen-grpc=/Users/derickshi/anaconda3/bin/grpc_python_plugin \
  "$PROTO_FILE"
