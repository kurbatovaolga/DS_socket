import socket
import cv2
import logging
import ssl

LOG_PATH = "logs/server.log"
FORMAT = "%(asctime)s - %(message)s"
HOST, PORT = 'localhost', 1235
RECEIVED_FILE_PATH = "image/server_image.jpg"
MANAGED_FILE_PATH = "image/sp_without_noise.jpg"
SERVER_CERT = 'ssl-certs/server.crt'
SERVER_KEY = 'ssl-certs/server.key'
CLIENT_CERTS = 'ssl-certs/client.crt'
MAX_FILE_SIZE = 2048
MAX_RANG = 3

logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG, format=FORMAT)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
context.load_verify_locations(cafile=CLIENT_CERTS)

server = socket.socket()
server.bind((HOST, PORT))
server.listen(5)
logging.info("Ожидание подключения...")

while True:
    client_socket, client_address = server.accept()
    logging.info("Принято подключение клиента с url: {address}:{c_socket}"
                 .format(address=client_address, c_socket=client_socket))

    conn = context.wrap_socket(client_socket, server_side=True)

    file = open(RECEIVED_FILE_PATH, "wb")
    logging.info("Открыт файл для записи: {file_path}".format(file_path=RECEIVED_FILE_PATH))

    image_chunk = conn.recv(MAX_FILE_SIZE)
    logging.info("Получен файл от клиента")

    while image_chunk:
        file.write(image_chunk)
        image_chunk = conn.recv(MAX_FILE_SIZE)
        if not image_chunk:
            break

    file.close()
    logging.info("Необработанный файл записан")

    image = cv2.imread(RECEIVED_FILE_PATH)

    logging.info("Идет восстановление изображения")
    image = cv2.medianBlur(image, MAX_RANG)

    cv2.imwrite(MANAGED_FILE_PATH, image)
    logging.info("Изображение восстановлено")

conn.close()
client_socket.close()


