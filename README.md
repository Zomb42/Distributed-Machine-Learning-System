# Distributed Machine Learning System

This repo now has two very small gRPC connection samples.

## What the samples do

- `grpc_connection_test/`: a minimal gRPC sample using JSON serializers
- `grpc_proto_test/`: a more normal gRPC sample using a `.proto` file and generated stubs

Both versions prove "two Python processes can talk over gRPC."

## Quick start

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the single dependency:

```bash
python -m pip install -r requirements.txt
```

3. Start the minimal JSON-based server:

```bash
python -m grpc_connection_test.server --port 50051
```

4. In a second terminal, run the minimal client:

```bash
python -m grpc_connection_test.client --host localhost --port 50051
```

5. Or run the minimal one-command smoke test:

```bash
python -m grpc_connection_test.smoke_test
```

6. To try the protobuf-based version, start the proto server:

```bash
python -m grpc_proto_test.server --port 50052
```

7. In a second terminal, run the proto client:

```bash
python -m grpc_proto_test.client --host localhost --port 50052
```

The proto client now calls two server RPCs:

- `Ping`: proves the connection works
- `GetMockTask`: returns a fake MNIST-style task assignment from the server

## Proto sample files

- `proto/connection.proto`: the API definition
- `grpc_proto_test/connection_pb2.py`: generated protobuf messages
- `grpc_proto_test/connection_pb2_grpc.py`: generated gRPC client/server stubs

## Why there are two versions

- The JSON version is easier to read on day one.
- The protobuf version is closer to how real gRPC projects are built.

If you are learning gRPC for class, focus on the proto version next.
