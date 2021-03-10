# https://habr.com/ru/post/149077/
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind(('localhost', 1235))  # 127.0.0.1
server.listen()

while True:
    client_socket, client_address = server.accept()

    file = open('image/server_image.jpg', "wb")
    image_chunk = client_socket.recv(2048)  # stream-based protocol

    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)
        if not image_chunk:
            break

    file.close()


client_socket.close()


# нужно дописать исправление шумов
