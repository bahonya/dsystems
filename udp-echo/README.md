# UDP echo

In this task we will focus on the user datagram protocol (UDP), which provides
unreliable datagram service. You will find the documentation of the
`socket` package useful: <https://docs.python.org/3/library/socket.html>

In `echo.py`, we have implemented sub-commands for a client and a server
using `argparse`. Execute the script with `-h` to understand its usage.

1. `./echo server &` will start the server in the background. Note: _This will
   not work until you have implemented the necessary server parts._

2. `./echo client` will start the command line client, from which you may interact with
   the server by typing commands into the terminal window.

The client is already implemented. It sends strings composed of the following

```text
cmd|:|txt
```

For example:

```text
UPPER|:|i want to be upper case
```

From this, the server is expected to produce the following reply:

```text
I WANT TO BE UPPER CASE
```

You may use `tcpdump` to monitor the communication:

```sh
sudo tcpdump -pi lo port 12110
```

**Tasks:**

1. Implement a UDP socket in `server()` and communicate with the client.

2. Implement each of the following commands in `create_response()`, so
   that the returned value corresponds to the expected test outcome. Here you
   are expected to implement a demultiplexer that demultiplexes the input (the
   command) so that different actions can be taken.

   | Command | Action                                                                                                  |
   |---------|---------------------------------------------------------------------------------------------------------|
   | UPPER   | Takes the provided input string `txt` and translates it to upper case using `upper()`.                  |
   | LOWER   | Same as UPPER, but lower case instead.                                                                  |
   | CAMEL   | Same as UPPER, but title or camel case instead.                                                         |
   | ROT13   | Takes the provided input string `txt` and applies the rot13 translation to it; see lab1 for an example. |
   | SWAP    | Takes the provided input string `txt` and inverts the case.                                             |

3. The server should reply `Unknown command` if it receives an unknown command
   or fails to interpret a request in any way.

4. Make sure that your server continues to function even if one client's
   connection or datagram packet caused an error.

Extras:

* In the client, we are using `sock.recvfrom(4096)`. What is the meaning
  of the parameter? Which problem could occur when you set it to a very small value?
