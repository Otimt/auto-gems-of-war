#import socket
#server = socket.socket()             #初始化
#server.bind(('localhost',6969))      #绑定ip和端口
#
#server.listen(5)                     #监听，设置最大数量是5
#print("开始等待接受客户端数据----")
#while True:
#    conn,addr = server.accept()      #获取客户端地址
#    print(conn,addr)
#    print("客户端来数据了")
#    while True:
#        data = conn.recv(1024)       #接收数据
#        print("接受的数据：",data)
#        if not data:
#            print("client has lost")
#            break
#        conn.send(data.upper())     #返回数据
#
#serve.close()                       #关闭socket
#---------------------
#作者：wiiknow
#来源：CSDN
#原文：https://blog.csdn.net/liu915013849/article/details/78869771
#版权声明：本文为博主原创文章，转载请附上博文链接！
#这是一个能一直保持连接的程序，因为上面的步骤只是最基本的用法，所以想要能一直连接的程序，就需要使用while True保持循环，还有一个问题就是，此程序只能连接一个客户端，并不能支持多并发，所以当出现第二个客户端时，就会出现挂起不动，所以想要完成多并发，则需要使用Python中的另外一个库“socketserver”



import socketserver
from window_service import gui_start
class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        gui_start(self)
        #print("Connected from: ", self.client_address)
        #while True:
        #    recvData = self.request.recv(1024)
        #    if not recvData:
        #        break
        #
        #    self.request.sendall(recvData)
        #self.request.close()
        #print("Disconnected from: ", self.client_address)

srv = socketserver.ThreadingTCPServer(("", 4424), EchoHandler)
srv.serve_forever()   #能连接多个客户端
#srv.handle_request()   #只能连接一个客户端，其余的客户端连接的话会被拒绝