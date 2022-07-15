#!/usr/bin/env python3

import argparse
import grpc
import kv_pb2
import kv_pb2_grpc


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')
subparsers.required = True
parser_insert = subparsers.add_parser('insert')
parser_insert.add_argument('key', type=str)
parser_insert.add_argument('value', type=str)
parser_lookup = subparsers.add_parser('lookup')
parser_lookup.add_argument('key', type=str)
parser_keys = subparsers.add_parser('keys')

args = parser.parse_args()

# TODO: connect to the server and execute RPCs

def guide_insert(stub):
    guide_get_one_feature(
        stub, route_guide_pb2.Point(latitude=409146138, longitude=-746188906))
    guide_get_one_feature(stub, route_guide_pb2.Point(latitude=0, longitude=0))

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = kv_pb2_grpc.KeyValueServiceStub(channel)
        if args.command == 'insert':
            response = stub.Insert(kv_pb2.InsertRequest(key=args.key, value=args.value))
            print(response)
        elif args.command == 'lookup':
            response = stub.Lookup(kv_pb2.LookupRequest(key=args.key))
            print(response)
        elif args.command == 'keys':
            response = stub.Keys(kv_pb2.KeysRequest())
            print(response)
       

if __name__ == '__main__':
    run()