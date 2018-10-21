import socket
ip_port = ('127.0.0.1',9999)

sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
while True:
    inp = input('数据：').strip()
    if inp == 'exit':
        break
    sk.sendto(bytes(inp,encoding='utf8'),ip_port)

sk.close()