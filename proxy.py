import socket
import numpy as np
import random
import cv2
import ssl

RECEIVED_IMAGE_PATH = "image/proxy_image.jpg"
NOISE_IMAGE_PATH = 'image/sp_noise.jpg'
HOST, CLIENT_PORT, SERVER_PORT = 'localhost', 10002, 1235
SERVER_SNI_HOSTNAME = 'example.com'
SERVER_CERT = 'ssl-certs/server.crt'
SERVER_KEY = 'ssl-certs/server.key'
CLIENT_CERT = 'ssl-certs/client.crt'
CLIENT_KEY = 'ssl-certs/client.key'
MAX_FILE_SIZE = 2048


# вносим шум
def sp_noise(image, prob):
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
context.load_verify_locations(cafile=CLIENT_CERT)

proxy = socket.socket()
proxy.bind((HOST, CLIENT_PORT))
proxy.listen(5)

client_socket, client_address = proxy.accept()
conn_client = context.wrap_socket(client_socket, server_side=True)

file = open(RECEIVED_IMAGE_PATH, "wb")
image_chunk = conn_client.recv(MAX_FILE_SIZE)

i = 0 # установим счетчик получения кусков изображения
while image_chunk:
    i += 1
    file.write(image_chunk)
    image_chunk = conn_client.recv(MAX_FILE_SIZE)
    print("передача чанок: ", i) # выведем количество полученных частей
    if not image_chunk:
        break
file.close()
conn_client.close()
client_socket.close()

image = cv2.imread(RECEIVED_IMAGE_PATH)
noise_img = sp_noise(image, 0.05)
cv2.imwrite(NOISE_IMAGE_PATH, noise_img)

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT)
context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_server = context.wrap_socket(client, server_side=False, server_hostname=SERVER_SNI_HOSTNAME)
conn_server.connect((HOST, SERVER_PORT))

# считывает и отправляет картинку
file = open(NOISE_IMAGE_PATH, mode="rb") #считываем картинку
image_chunk = file.read(MAX_FILE_SIZE)

while image_chunk:
    conn_server.send(image_chunk)
    image_chunk = file.read(MAX_FILE_SIZE)

file.close()

