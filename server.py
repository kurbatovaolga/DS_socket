import socket
import cv2
import logging

LOG_PATH = "logs/server.log"
FORMAT = "%(asctime)s - %(message)s"
HOST, PORT = 'localhost', 1235
RECEIVED_FILE_PATH = "image/server_image.jpg"
MANAGED_FILE_PATH = "image/sp_without_noise.jpg"
MAX_FILE_SIZE = 2048
MAX_RANG = 3

logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG, format=FORMAT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind((HOST, PORT))  # 127.0.0.1
server.listen()
logging.info("Ожидание подключения...")

while True:
    client_socket, client_address = server.accept()
    logging.info("Принято подключение клиента с url: {address}:{c_socket}"
                 .format(address=client_address, c_socket=client_socket))

    file = open(RECEIVED_FILE_PATH, "wb")
    logging.info("Открыт файл для записи: {file_path}".format(file_path=RECEIVED_FILE_PATH))

    image_chunk = client_socket.recv(MAX_FILE_SIZE)  # stream-based protocol
    logging.info("Получен файл от клиента")

    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(MAX_FILE_SIZE)
        if not image_chunk:
            break

    file.close()
    logging.info("Необработанный файл записан")

    image = cv2.imread(RECEIVED_FILE_PATH)

    logging.info("Идет восстановление изображения")
    image = cv2.medianBlur(image, MAX_RANG)

    cv2.imwrite(MANAGED_FILE_PATH, image)
    logging.info("Изображение восстановлено")

client_socket.close()


