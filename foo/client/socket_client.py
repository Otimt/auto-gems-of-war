import socket

client = socket.socket()

client.connect(('localhost',4424))  #连接服务器

while True:
    msg = input(">>:").strip()
    if len(msg) == 0 :continue
    client.send(msg.encode())   #发送数据

    data = client.recv(1024)    #接收数据
    print("返回数据:",data.decode())


client.close()
#---------------------
#作者：wiiknow
#来源：CSDN
#原文：https://blog.csdn.net/liu915013849/article/details/78869771
#版权声明：本文为博主原创文章，转载请附上博文链接！