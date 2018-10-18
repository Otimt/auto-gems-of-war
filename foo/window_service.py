from tkinter import *

import socket

sk = socket.socket()
sk.bind(("127.0.0.1",8765))
sk.listen(5)

conn,address = sk.accept()
sk.sendall(bytes("Hello world",encoding="utf-8"))


def gui_start():
    init_window = Tk()        #实例化出一个父窗口
    init_window.mainloop()    #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

#gui_start()