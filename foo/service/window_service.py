#
# request 是一个 socket 实例
#
from tkinter import *
def gui_start(sk=None):

    
    win_title = "tk_window" if not sk else sk.client_address
    btn_jt,input_dj,btn_dj,btn_zl,btn_s,btn_f,btn_gj,msgBox,srv_window = init_window(win_title)

    
    #Text(frameR1).pack()
    print(msgBox)
    
    srv_window.mainloop()    #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    
    while True:
        recvData = sk.request.recv(1024)
        msgBox.insert(END, "收到："+recvData,'green')

    
    


    
def init_window(title):
    srv_window = Tk()        #实例化出一个父窗口
    srv_window.title(title)   #窗口标题
    srv_window.geometry('500x200')  #窗口尺寸

    frameL1 = Frame(width=200, height=40,bg="#ffffff")
    frameL2 = Frame(width=200, height=40,bg="#ffffff")
    frameL3 = Frame(width=200, height=40,bg="#ffffff")
    frameL4 = Frame(width=200, height=40,bg="#ffffff")
    frameL5 = Frame(width=200, height=40,bg="#ffffff")
    frameR1 = Frame(width=300,height=200,bg="#ffffff")
    
    
    frameL1.grid_propagate(0)
    frameL2.grid_propagate(0)
    frameL3.grid_propagate(0)
    frameL4.grid_propagate(0)
    frameL5.grid_propagate(0)
    frameR1.grid_propagate(0)

    frameL1.grid(column=0,row=0)
    frameL2.grid(column=0,row=1)
    frameL3.grid(column=0,row=2)
    frameL4.grid(column=0,row=3)
    frameL5.grid(column=0,row=4)
    frameR1.grid(column=1,row=0,rowspan=5)

    Label(frameL1,text = '1 截图：').grid(column=0,row=0)
    Label(frameL2,text = '2 点击：').grid(column=0,row=0)
    Label(frameL3,text = '3 指令：').grid(column=0,row=0)
    Label(frameL4,text = '4 开关：').grid(column=0,row=0)
    Label(frameL5,text = '5 关机：').grid(column=0,row=0)
    
    btn_jt = Button(frameL1,text = '截图')
    btn_jt.grid(column=1,row=0,padx=5)
    input_dj = Entry(frameL2,width=9)
    input_dj.grid(column=1,row=0,padx=5)
    btn_dj = Button(frameL2,text = '点击')
    btn_dj.grid(column=2,row=0,padx=5)
    btn_zl = Button(frameL3,text = '指令')
    btn_zl.grid(column=1,row=0,padx=5)
    btn_s = Button(frameL4,text = '启动')
    btn_s.grid(column=1,row=0,padx=5)
    btn_f = Button(frameL4,text = '停止')
    btn_f.grid(column=2,row=0,padx=5)
    btn_gj = Button(frameL5,text = '关机')
    btn_gj.grid(column=1,row=0,padx=5)
    msgBox = Text(frameR1)
    msgBox.grid()
    
    
    
    return btn_jt,input_dj,btn_dj,btn_zl,btn_s,btn_f,btn_gj,msgBox,srv_window
    
if __name__ == "__main__":
    gui_start()



