from socket import *

PROMPT = "> "
HOST = "127.0.0.1"
PORT = 8090
HEADERS = """\
    POST /auth HTTP/1.1\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""


def create_http_request(body):
    global HOST, PORT, HEADERS

    body_bytes = body.encode('ascii')
    header_bytes = HEADERS.format(
        content_type="application/x-www-form-urlencoded",
        content_length=len(body_bytes),
        host=str(HOST) + ":" + str(PORT)
    ).encode('iso-8859-1')

    return header_bytes + body_bytes


def unwrap_http_response(http_response):
    http_response_arr = http_response.split('\r\n')
    if (http_response_arr[-1] == ''):
        return http_response_arr[-2]
    else:
        return http_response_arr[-1]


def client():
    global PROMPT, HOST, PORT

    # get socket instance
    client_socket = socket()
    # connect to proxy server
    client_socket.connect((HOST,PORT))

    while True:
        # get input from user 
        ftp_cmd = input(PROMPT)

        # create and encode HTTP POST request
        encoded_http_request = create_http_request(ftp_cmd)

        # send HTTP POST request to proxy server
        client_socket.sendall(encoded_http_request)
        
        # receive response from proxy server
        http_response = client_socket.recv(1024).decode()
        ftp_response = unwrap_http_response(http_response)

        print(ftp_response)

        if (ftp_response.split(' ')[0] == "220"):
            PROMPT = "ftp> "
        elif (ftp_response.split(' ')[0] == "221"):
            PROMPT = "> "

    # close connection
    client_socket.close()


if __name__ == '__main__':
    client()
