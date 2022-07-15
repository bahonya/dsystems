#!/usr/bin/env python3

from concurrent import futures
from threading import Lock
import grpc
import kv_pb2
import kv_pb2_grpc
import time


class KeyValue(kv_pb2_grpc.KeyValueService):

    def __init__(self):
        self.lock = Lock()

    def Insert(self, request, context):
        # TODO: add proper locking using `self.lock`
        print(f"Inserting {request.key}:{request.value}")
        if request.key not in key_value_store:
            time.sleep(1)
            key_value_store[request.key] = request.value
            rc = True
        else:
            rc = False
        return kv_pb2.InsertResponse(success=rc)

    def Lookup(self, request, context):
        print(f"Looking up {request.key}")
        # TODO: implement
        if request.key not in key_value_store:
            rc = "No such key in our key_value_store"
        else:
            rc = key_value_store[request.key]
        return kv_pb2.LookupResponse(value=rc)

    def Keys(self, request, context):
        print(f"Returning keys")
        # TODO: implement
        return kv_pb2.KeysResponse(keys=list(key_value_store.keys()))

key_value_store: dict[str, str] = {
    "an_initial_key": "an_initial_value"
}

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
kv_pb2_grpc.add_KeyValueServiceServicer_to_server(KeyValue(), server)
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()
