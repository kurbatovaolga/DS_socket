server:
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt

client:
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt