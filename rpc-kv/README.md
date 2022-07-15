# RPC

A popular way to design distributed applications is by means of remote procedure
calls. gRPC is Google's remote procedure calls. You can read about remote
procedure calls and gRPC here <https://grpc.io/docs/what-is-grpc/> and here
<https://grpc.io/docs/languages/python/quickstart/>

It would be useful to also read about protocol buffers, Google's way of
serializing data: <https://developers.google.com/protocol-buffers/docs/overview>

## Install dependencies

Install gRPC and its tools for python using `pip`:

```sh
python -m pip install grpcio grpcio-tools
```

## Run an example program

There is an example program in gRPC's code called *route_guide*. Fetch the
sources:

```sh
git clone -b v1.42.0 https://github.com/grpc/grpc
```

Run the server and the client to test your installation. Open two terminals and
go to `grpc/examples/python/route_guide`. In one run the server:

```sh
python route_guide_server.py
```

If the server runs successfully, you should not see any output on this terminal.

In another terminal window, type the following to start a client that will
connect to the server:

```sh
python route_guide_client.py
```

If the client runs successfully, you should see a lot of output similar to this:

```log
...
2015/08/10 15:16:10 location:<latitude:405002031 longitude:-748407866 > 
2015/08/10 15:16:10 location:<latitude:409532885 longitude:-742200683 > 
2015/08/10 15:16:10 location:<latitude:416851321 longitude:-742674555 > 
2015/08/10 15:16:10 name:"3387 Richmond Terrace, Staten Island, NY 10303, USA" location:<latitude:406411633 longitude:-741722051 > 
2015/08/10 15:16:10 name:"261 Van Sickle Road, Goshen, NY 10924, USA" location:<latitude:413069058 longitude:-744597778 > 
2015/08/10 15:16:10 location:<latitude:418465462 longitude:-746859398 > 
2015/08/10 15:16:10 location:<latitude:411733222 longitude:-744228360 > 
2015/08/10 15:16:10 name:"3 Hasta Way, Newton, NJ 07860, USA" location:<latitude:410248224 longitude:-747127767 > 
2015/08/10 15:16:10 Traversing 74 points.
2015/08/10 15:16:10 Route summary: point_count:74 distance:720194535 
2015/08/10 15:16:10 Got message First message at point(0, 1)
2015/08/10 15:16:10 Got message Fourth message at point(0, 1)
2015/08/10 15:16:10 Got message First message at point(0, 1)
...
```

You may want to study the code for the route_guide example to try to
understand what is going on.

## Building your own RPC-based key-value storage

This folder contains code for a very simple key-value storage service, where the
keys and values are strings. It offers the method `Insert()`, which inserts a
key-value pair. A key-value pair may not be modified after it has been written.
`Insert()` returns a bool indicating success or failure.

We already generated the python classes for request and response in `kv_pb2.py`
and classes for server and client in `kv_pb2_grpc.py` for you. In case you run
into compile errors, you may try to re-generate these using:

```sh
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. kv.proto
```

**Tasks:**

1. In the client, create a connection to the server.

2. In the client, call the `Insert()` gRPC for the corresponding sub-command.

3. In the server, implement the `Lookup()` gRPC, which should return the value
   of the requested key.

4. In the server, implement the `Keys()` gRPC, which should return a list of
   the keys (not the values) back to the client.

5. In the client, call the `Lookup()` gRPC for the corresponding sub-command.

6. In the client, call the `Keys()` gRPC for the corresponding sub-command.

7. Several clients connecting to the server may read and write concurrently from
   the shared key-value dict. This will eventually cause problems when multiple
   clients try to insert a value for the same key. I.e. the server may return
   wrong results for `Insert()`. Implement locking at the appropriate location
   in the code. See
   <https://docs.python.org/3/library/threading.html#using-locks-conditions-and-semaphores-in-the-with-statement>.

Extras:

* Explain why the clients can access the dict at the server concurrently.
* If you run your server without protection on the dict, are you able to provoke
  inconsistencies in the dict?
