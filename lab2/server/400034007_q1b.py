import socket


def proxy_server():
    # set hostname and port number
    host = socket.gethostname()
    port = 8090

    # create headers for HTTP response message
    headers = """\
    HTTP/1.1 200 OK\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Connection: keep-alive\r
    \r\n"""

    # get socket instance
    server_socket = socket.socket()
    # bind host and port togehter
    server_socket.bind((host,port))

    # configure number of clients server can listen to at once
    server_socket.listen(0)
    # accept new connection
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        # receive HTTP POST request from client
        data = conn.recv(1024).decode()
        if not data:
            break
        # get body from HTTP POST request
        body = data.split('\r\n')[-1]
        print("Received from client: " + str(body))
        # create body of HTTP response message
        body = 'ftp response placeholder'
        # encode body and headers 
        body_bytes = body.encode('ascii')
        header_bytes = headers.format(
                content_type="text/html; encoding=utf8",
                content_length=len(body_bytes)
        ).encode('iso-8859-1')

        # send response to client
        conn.sendall(header_bytes + body_bytes)

    # close the connection
    conn.close()


if __name__ == '__main__':
    proxy_server()
