#!/usr/bin/env python3

import argparse
import codecs
import socket
from functools import partial

def rot_13(text):
    def rot_13_text(text: str):
        return codecs.encode(text, 'rot_13')
    return rot_13_text

def create_response(command: str, text: str):
    # TODO: implement responses for commands
    commands = {
        "UPPER": text.upper(),
        "LOWER": text.lower(),
        "CAMEL": text.title(),
        "ROT13": rot_13(text),
        "SWAP": text.swapcase()
    }
    response = commands[command]
    
    return response

def client(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            command = input('Enter command: ')
            text = input('Enter text: ')
            sock.sendall(f'{command}|:|{text}'.encode())
            payload = sock.recv(3)
            print(payload.decode())

def server(host: str, port: int):
    # TODO: create socket and bind it to the endpoint
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(1)
        conn, addr = sock.accept()
        with conn:
            print(f'Connected by {addr}')
            while True:
                # TODO: receive request
                raw_bytes = conn.recv(4096)
                if not raw_bytes:
                    break
                command, text = raw_bytes.decode().split("|:|")
                response = create_response(command, text)
                # TODO: send response
                conn.sendall(response.encode())

parser = argparse.ArgumentParser(description='Client and server for UDP echo', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--endpoint', type=str, default='localhost:12110', help='Endpoint on which the server runs or to which the client connects')
subparsers = parser.add_subparsers(dest='{client, server}')
subparsers.required = True
parser_client = subparsers.add_parser('client')
parser_client.set_defaults(func=client)
parser_server = subparsers.add_parser('server')
parser_server.set_defaults(func=server)

args = parser.parse_args()
host = args.endpoint.split(':')[0]
port = int(args.endpoint.split(':')[1])

args.func(host, port)
