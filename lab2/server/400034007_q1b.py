import socket


def proxy_server():
    # set hostname and port number
    host = socket.gethostname()
    port = 8090

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
        # receive data packet
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Received from client: " + str(data))
        data = input(' -> ')
        # send response to client
        conn.send(data.encode())

    # close the connection
    conn.close()


if __name__ == '__main__':
    proxy_server()
