def getRawKey(data):
	headers=data.decode().split("\r\n")
	for header in headers:
		s=header.split(": ")
		if s[0]=="Sec-WebSocket-Key":
			return s[1]
	print("Error. Not found key")

import socket
from time import sleep
import hashlib 
import base64
s=socket.socket()
s.bind(("localhost",5678))
s.listen(10)
print("bind")
k,addr=s.accept()
print("accept")
d=k.recv(1024)
print(f"Data:\n{d.decode()}")
keyGet=getRawKey(d)
print(keyGet)
key=keyGet+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

m = hashlib.sha1()
m.update(key.encode())
w=m.digest()
trySend=base64.b64encode(w).decode()

answer=("HTTP/1.1 101 Switching Protocols\r\n"
"Upgrade: websocket\r\n"+
"Connection: Upgrade\r\n"+
"Sec-WebSocket-Accept: "+trySend+"\r\n"+
"\r\n")
# "Sec-WebSocket-Protocol: chat\r\n\r\n")
answer=answer.encode()
print(answer)
k.sendall(answer)

text="1234567".encode()
size=len(text)
if len(text)>125:
	print("ERROR слишком большой текст.")
t1=0b10000001
t2=size
t1=t1.to_bytes(1,"little")
t2=t2.to_bytes(1,"little")
w=t1+t2+text

k.sendall(w)
sleep(5)
print("next")

text="Нигер".encode()
size=len(text)
if len(text)>125:
	print("ERROR слишком большой текст.")
t1=0b10000001
t2=size
t1=t1.to_bytes(1,"little")
t2=t2.to_bytes(1,"little")
w=t1+t2+text

k.sendall(w)
print("Отправил второе")
sleep(30)
# int_value=0b10000001
# def func(num, pos):
# 	return (num & (1 << pos)) >> pos
	
#Первые 8 - 0b10000001
#Следующие 7 -Длина тела ( 0-125) именно байт
#Следующие 4 - 0b0000
#Дальше идет тело ответа.

