import socket
import ssl
import logging
from PIL import Image
import io

IMAGE_PATH = "image/foto.jpg"
MAX_FILE_SIZE = 2048
HOST, PORT = 'localhost', 10002
LOG_PATH = "logs/client.log"
FORMAT = "%(asctime)s - %(message)s"
SERVER_SNI_HOSTNAME = 'example.com'
SERVER_CERT = 'ssl-certs/server.crt'
CLIENT_SERT = 'ssl-certs/client.crt'
CLIENT_KEY = 'ssl-certs/client.key'


def image_to_byte_array(image: Image):
    roi_img = image.crop()
    img_byte_arr = io.BytesIO()
    roi_img.save(img_byte_arr, format=image.format)
    return img_byte_arr.getvalue()


logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG, format=FORMAT)

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT)
context.load_cert_chain(certfile=CLIENT_SERT, keyfile=CLIENT_KEY)
logging.info("Поднят контекст SSL")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
conn = context.wrap_socket(client, server_side=False, server_hostname=SERVER_SNI_HOSTNAME)
conn.connect((HOST, PORT))
logging.info("Клиент подключился к серверу")
logging.info(conn.getpeercert())

img = Image.open(IMAGE_PATH)
logging.info("Открыт файл:{img_path}".format(img_path=IMAGE_PATH))

width, height = img.size
width, height = bytes(str(width), 'utf8'), bytes(str(height), 'utf8')

img_byte = image_to_byte_array(img)

conn.send(width)
conn.send(height)
split = [img_byte[i:i+MAX_FILE_SIZE] for i in range(0, len(img_byte), MAX_FILE_SIZE)]

for i in split:
    conn.send(i)
logging.info("Изображение отправлено")

conn.close()
client.close()
logging.info("Завершение работы")
