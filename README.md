#httpbot PoC

This script is a simple python backdoor Proof of Concept using HTTP GET
requests as the main form of communication.

##Concept / Usage

The idea is simple. We have a server and a client. The server is a simple HTTP
server. The scripts work as follows.

#####Main routine
The client polls the server every X seconds, sending a GET request, passing its
IP and hostname as arguments. 
The server logs the requests arguments and responds with a 403 Forbidden status
code.

#####Interaction / popping a shell
To get a shell, you need to interrupt the server with Ctrl-C. A menu will open,
allowing to pick a client. Here a IP or hostname is to be specified.

Furthermore, you will need to open another terminal on the servers host, and
run a listener. The default port to listen on is 1337.
>
> nc -l -p 1337
>

The client will poll the server again soon. When this happens, the server will
recognize the clients IP or hostname, and adjust its landing page.

Instead of a 403 response, the server sends a 200 "OK" response code. 

Also, the server will provide the port number to which the client should
connect as the HTTP body. 

Receiving this information, the client will spawn a shell and connect to the
server on the specified port, giving you a shell.

