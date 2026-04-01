from __future__ import annotations

import argparse
import socket
import sys
import time
from concurrent import futures
from pathlib import Path
import grpc

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from grpc_proto_test import connection_pb2
from grpc_proto_test import connection_pb2_grpc


class ConnectionService(connection_pb2_grpc.ConnectionServiceServicer):
    def Ping( #functions that the client calls
        self,
        request: connection_pb2.PingRequest,
        context: grpc.ServicerContext,
    ) -> connection_pb2.PingReply:
        return connection_pb2.PingReply(
            message=f"pong: {request.message}",
            server_hostname=socket.gethostname(),
            server_time_ms=int(time.time() * 1000),
        )

    def GetMockTask(
        self,
        request: connection_pb2.MockTaskRequest,
        context: grpc.ServicerContext,
    ) -> connection_pb2.MockTaskReply:
        worker_name = request.worker_name or "unnamed-worker"
        return connection_pb2.MockTaskReply(
            task_id=f"mock-task-for-{worker_name}",
            dataset_name="MNIST",
            shard_index=1,
            total_shards=4,
            epochs=2,
            batch_size=64,
            learning_rate=0.01,
            notes="Mock assignment from the coordinator. No real training yet.",
        )


def serve(port: int) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    connection_pb2_grpc.add_ConnectionServiceServicer_to_server(
        ConnectionService(),
        server,
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Proto gRPC server listening on localhost:{port}")
    server.wait_for_termination()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a protobuf-based gRPC test server.")
    parser.add_argument("--port", type=int, default=50052)
    args = parser.parse_args()
    serve(args.port)


if __name__ == "__main__":
    main()
