
import socket
import json
import time
import sys

sys.path.append('../')
from common.window_action import *

client = socket.socket()

client.connect(('134.175.49.115',4424))  #连接服务器

while True:
    #msg = input(">>:").strip()
    #if len(msg) == 0 :continue
    #client.send(msg.encode())   #发送数据

    dataStr = client.recv(1024)    #接收数据
    dataStr = dataStr.decode()
    print("返回数据:",dataStr)
    if (dataStr != ""):
        data = json.loads(dataStr)
        code = data['code']
        if (code == 'window_capture'):
            print("截图")
            imgPath = "game2.jpg"
            window_capture(imgPath)
        elif (code == 'click'):
            print("点击")
            mouse_click(data['x'],data['y'])
        elif (code == 'keyboard'):
            keyboard_press(data['key'])
        elif (code == 'shutdown'):
            print("关机")
            shutdown()
            
    time.sleep(1)

client.close()
#---------------------
#作者：wiiknow
#来源：CSDN
#原文：https://blog.csdn.net/liu915013849/article/details/78869771
#版权声明：本文为博主原创文章，转载请附上博文链接！