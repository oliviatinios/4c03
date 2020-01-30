from socket import *

HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8090
HTTP_SOCKET = None
FTP_HOST = None
FTP_PORT = 21
FTP_SOCKET = None
HEADERS = """\
    HTTP/1.1 200 OK\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Connection: keep-alive\r
    \r\n"""


def send_ftp_msg(socket_instance,data):
    socket_instance.sendall(data.encode('ascii'))


def receive_ftp_msg(socket_instance):
    data = socket_instance.recv(64000).decode()
    print('Received from FTP server: {}' .format(data))
    return data


def handle_ftp_cmd(cmd, args):
    global FTP_HOST, FTP_PORT, FTP_SOCKET

    if (FTP_SOCKET is None and cmd.lower() != "ftp"):
        return "No FTP connection."

    elif (cmd.lower() == "ftp"):
        if (len(args) == 0):
            return "Please provide hostname."
        # get socket instance
        FTP_HOST = args[0]
        FTP_SOCKET = socket()
        # connect to ftp server
        FTP_SOCKET.connect((FTP_HOST,FTP_PORT))
        return receive_ftp_msg(FTP_SOCKET)

    elif (cmd.lower() == "user" or cmd.lower() == "pass"):
        user = args[0]
        ftp_cmd = "{} {}\r\n" .format(cmd,user)
        send_ftp_msg(FTP_SOCKET,ftp_cmd)
        return receive_ftp_msg(FTP_SOCKET)

    elif (cmd.lower() == "pwd" or cmd.lower() == "help" or cmd.lower() == "cdup"
            or cmd.lower() == "syst" or cmd.lower() == "cwd"):
        ftp_cmd = "{}\r\n" .format(cmd)
        send_ftp_msg(FTP_SOCKET,ftp_cmd)
        return receive_ftp_msg(FTP_SOCKET)

    elif (cmd.lower() == "quit"):
        ftp_cmd = "{}\r\n" .format(cmd)
        send_ftp_msg(FTP_SOCKET,ftp_cmd)
        response = receive_ftp_msg(FTP_SOCKET)
        # close the socket connection
        FTP_SOCKET.close()
        FTP_SOCKET = None
        return response

    else:
        ftp_cmd = "{}\r\n" .format(cmd)
        send_ftp_msg(FTP_SOCKET,ftp_cmd)
        return receive_ftp_msg(FTP_SOCKET)


# receives HTTP POST request over socket connection and unwraps it
def receive_http_request(conn):
    # receive HTTP POST request from client
    data = conn.recv(1024).decode()
    if not data:
        return None, None
    # get body from HTTP POST request
    body = data.split('\r\n')[-1]
    print("Received from client: " + str(body))

    # parse body of HTTP request to get FTP command and arguments
    body_arr = body.split(' ')
    ftp_cmd = body_arr[0]
    if (len(body_arr) > 1):
        ftp_args = body_arr[1:]
    else:
        ftp_args = []

    return ftp_cmd, ftp_args


# sends HTTP response over socket connection
def send_http_response(conn,data):
    global HEADERS

    # encode body and headers 
    body_bytes = data.encode('ascii')
    header_bytes = HEADERS.format(
            content_type="text/html; encoding=utf8",
            content_length=len(body_bytes)
    ).encode('iso-8859-1')

    # send response to client
    conn.sendall(header_bytes + body_bytes)


def proxy_server():
    # get socket instance
    HTTP_SOCKET = socket()
    # bind host and port togehter
    HTTP_SOCKET.bind((HTTP_HOST,HTTP_PORT))

    # configure number of clients server can listen to at once
    HTTP_SOCKET.listen(0)
    # accept new connection
    conn, address = HTTP_SOCKET.accept()
    print("Connection from: " + str(address))

    while True:
        # receive HTTP POST request from client and get FTP command
        ftp_cmd, ftp_args = receive_http_request(conn)
        if (ftp_cmd is None):
            break

        # send FTP command and get response message
        ftp_response = handle_ftp_cmd(ftp_cmd,ftp_args)

        # send response to client
        send_http_response(conn,ftp_response)

    # close the connection
    conn.close()


if __name__ == '__main__':
    proxy_server()
