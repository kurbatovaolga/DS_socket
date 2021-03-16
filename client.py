import socket
import ssl
import logging

IMAGE_PATH = "image/foto.jpg"
MAX_FILE_SIZE = 2048
HOST, PORT = 'localhost', 10002
LOG_PATH = "logs/client.log"
FORMAT = "%(asctime)s - %(message)s"

logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG, format=FORMAT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect((HOST, PORT))  # 127.0.0.1
logging.info("Клиент подключился к серверу")

file = open(IMAGE_PATH, 'rb')
logging.info("Открыт файл:{img_path}".format(img_path=IMAGE_PATH))

image_data = file.read(MAX_FILE_SIZE)

while image_data:
    client.send(image_data)
    image_data = file.read(MAX_FILE_SIZE)

logging.info("Изображение отправлено")

file.close()
client.close()
logging.info("Завершение работы")
