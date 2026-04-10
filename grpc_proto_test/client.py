from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import grpc

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from grpc_proto_test import connection_pb2
from grpc_proto_test import connection_pb2_grpc


def ping(host: str, port: int, timeout: float = 3.0) -> dict:
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        grpc.channel_ready_future(channel).result(timeout=timeout)
        stub = connection_pb2_grpc.ConnectionServiceStub(channel)
        started = time.perf_counter()
        response = stub.Ping(
            connection_pb2.PingRequest(
                message="hello from proto client",
                client_time_ms=int(time.time() * 1000),
            ),
            timeout=timeout,
        )
        return {
            "message": response.message,
            "server_hostname": response.server_hostname,
            "server_time_ms": response.server_time_ms,
            "latency_ms": round((time.perf_counter() - started) * 1000, 2),
        }


def get_mock_task( host: str, port: int, worker_name: str, timeout: float = 3.0, ) -> dict:
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        grpc.channel_ready_future(channel).result(timeout=timeout)
        stub = connection_pb2_grpc.ConnectionServiceStub(channel)
        response = stub.GetMockTask(
            connection_pb2.MockTaskRequest(worker_name=worker_name),
            timeout=timeout,
        )
        return {
            "task_id": response.task_id,
            "dataset_name": response.dataset_name,
            "shard_index": response.shard_index,
            "total_shards": response.total_shards,
            "epochs": response.epochs,
            "batch_size": response.batch_size,
            "learning_rate": response.learning_rate,
            "notes": response.notes,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a protobuf-based gRPC test client.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=50052)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--worker-name", default="worker-1")
    args = parser.parse_args()
    print("Ping response:")
    print(ping(args.host, args.port, timeout=args.timeout))
    print("Mock task response:")
    print(
        get_mock_task(
            args.host,
            args.port,
            worker_name=args.worker_name,
            timeout=args.timeout,
        )
    )


if __name__ == "__main__":
    main()
