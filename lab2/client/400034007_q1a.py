import socket

def client():
    # set hostname and port number
    host = socket.gethostname()
    port = 8090

    # get socket instance
    client_socket = socket.socket()
    # connect to proxy server
    client_socket.connect((host, port))

    message = input(" -> ")

    while message.lower().strip() != 'bye':
        # send message to proxy server
        client_socket.send(message.encode())
        # receive response from proxy server
        data = client_socket.recv(1024).decode()

        print("Received from server: " + data)

        message = input(" -> ")

    # close connection
    client_socket.close()


if __name__ == '__main__':
    client()
