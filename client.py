import socket
import ssl
import logging

IMAGE_PATH = "image/foto.jpg"
MAX_FILE_SIZE = 2048
HOST, PORT = 'localhost', 10002
LOG_PATH = "logs/client.log"
FORMAT = "%(asctime)s - %(message)s"
SERVER_SNI_HOSTNAME = 'example.com'
SERVER_CERT = 'ssl-certs/server.crt'
CLIENT_SERT = 'ssl-certs/client.crt'
CLIENT_KEY = 'ssl-certs/client.key'

logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG, format=FORMAT)

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT)
context.load_cert_chain(certfile=CLIENT_SERT, keyfile=CLIENT_KEY)
logging.info("Поднят контекст SSL")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
conn = context.wrap_socket(client, server_side=False, server_hostname=SERVER_SNI_HOSTNAME)
conn.connect((HOST, PORT))
logging.info("Клиент подключился к серверу")
logging.info(conn.getpeercert())

file = open(IMAGE_PATH, 'rb')
logging.info("Открыт файл:{img_path}".format(img_path=IMAGE_PATH))

image_data = file.read(MAX_FILE_SIZE)

while image_data:
    conn.send(image_data)
    image_data = file.read(MAX_FILE_SIZE)

logging.info("Изображение отправлено")

conn.close()
file.close()
client.close()
logging.info("Завершение работы")
