import socket
import ssl

HOST, PORT = 'localhost', 10002
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('localhost', 10002))  # 127.0.0.1

file = open('image/foto.jpg', 'rb')
image_data = file.read(2048)
print(123)
while image_data:
    client.send(image_data)
    image_data = file.read(2048)

file.close()
client.close()
