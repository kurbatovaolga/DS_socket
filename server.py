import socket
import cv2
import logging

logging.basicConfig(filename="logs/server.log", level=logging.DEBUG, format="%(asctime)s - %(message)s")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind(('localhost', 1235))  # 127.0.0.1
server.listen()
logging.info("Ожидание подключения...")

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

    image = cv2.imread('image/server_image.jpg')

    logging.info("Идет восстановление изображения")
    image = cv2.medianBlur(image, 3)

    cv2.imwrite('image/sp_without_noise.jpg', image)
    logging.info("Изображение восстановлено")


client_socket.close()


