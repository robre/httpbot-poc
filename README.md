#httpbot PoC

simple httpbot

concept:
client polls server with HTTP GET every x seconds, server default response is 403. Server saves polling clients to a list.
on server side then you can pick a client which polled it. then you open a listener
on the server, default port is 1337 like this in a seperate console.

>
> nc -l -p 1337
> 

on its next poll, the client will receive a status code 200 and instead of an
empty page a page indicating the port to connect to.
The client will then open a reverse shell to the server.
