#!/usr/bin/env python3

import argparse
import codecs
from logging import exception
import socket

def create_response(command: str, text: str):
    # TODO: implement responses for commands
    try:
        match command:
            case "UPPER": 
                response = text.upper()
            case "LOWER": 
                response = text.lower()
            case "CAMEL": 
                response = text.title()
            case "ROT13": 
                response = codecs.encode(text, 'rot_13')
            case "SWAP": 
                response = text.swapcase()
            case _:
                raise SyntaxError('This command is not set: ' + repr(command))
    except SyntaxError as e:
        response = e.msg
    return response

def client(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            command = input('Enter command: ')
            text = input('Enter text: ')

            sock.sendto(f'{command}|:|{text}'.encode(), (host, port))
            payload, server = sock.recvfrom(3)
            print(payload.decode())

def server(host: str, port: int):
    # TODO: create socket and bind it to the endpoint
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))

        while True:
            # TODO: receive request
            raw_bytes, client = sock.recvfrom(2048)
            command, text = raw_bytes.decode().split("|:|")
            response = create_response(command, text)
            # TODO: send response
            sock.sendto(response.encode(), client)

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
