import socket
import numpy as np
import random
import cv2

#
proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
proxy.bind(('localhost', 10002))  # 127.0.0.1
proxy.listen()

client_socket, client_address = proxy.accept()

file = open('image/proxy_image.jpg', "wb") # открываем изображение
image_chunk = client_socket.recv(2048)

i = 0 # установим счетчик получения кусков изображения
while image_chunk:
    i += 1
    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)
    print("передача чанок: ", i) # выведем количество полученных частей
    if not image_chunk:
        break
file.close()
client_socket.close()


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


image = cv2.imread('image/proxy_image.jpg')
noise_img = sp_noise(image, 0.05)
cv2.imwrite('image/sp_noise.jpg', noise_img)


client_socket.close()

proxy2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

proxy2 .connect(("127.0.0.1", 1235))


# считывает и отправляет картинку
file = open('image/sp_noise.jpg', mode="rb") #считываем картинку
image_chunk = file.read(2048)

while image_chunk:

    proxy2.send(image_chunk)
    image_chunk = file.read(2048)

file.close()

