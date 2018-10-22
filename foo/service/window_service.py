#
# request 是一个 socket 实例
#
from tkinter import *
def gui_start(sk=None):

    srv_window = Tk()        #实例化出一个父窗口


    win_title = "tk_window" if not sk else sk.client_address
    srv_window.title(win_title)   #窗口标题
    srv_window.geometry('500x130')  #窗口尺寸

    Label(srv_window,text = '1 截图').pack(side="LEFT")
    Label(srv_window,text = '2 点击').pack()
    Label(srv_window,text = '3 指令').pack()
    Label(srv_window,text = '4 开关').pack()
    Label(srv_window,text = '5 关机').pack()
    Message(srv_window,text = '6 输出').pack()

    srv_window.mainloop()    #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == "__main__":
    gui_start()



