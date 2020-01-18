# Lab 2
The purpose of this lab is to learn about the FTP and HTTP protocols.

The goal for this lab is to create a client and a proxy server. The client accepts FTP commands and sends them as HTTP messages to the proxy server. The proxy server accepts HTTP messages from the client, unwraps the FTP command and forwards it to the FTP server. The response from the FTP server is then wrapped in an HTTP message by the proxy server and returned to the client.

The client and server are created using the socket library in Python.
