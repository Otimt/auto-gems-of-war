from tkinter import *

import socket

obj = socket.socket()
obj.connect(("127.0.0.1",8765))

ret = str(obj.recv(1024),encoding="utf-8")
print(ret)


def gui_start():
    init_window = Tk()        #实例化出一个父窗口
    init_window.mainloop()    #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

#gui_start()