import time
import pyHook
import multiprocessing
import logging

from common.game_action import *

logging.basicConfig(
    level=logging.DEBUG,#控制台打印的日志级别
    filename='new.log',
    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    #a是追加模式，默认如果不写的话，就是追加模式
    format= '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    #日志格式
)



class Loop():

    def __init__(self,interval=2):
        self.mainProgress = None
        self.loopAction = None
        self.isLoop = False
        self.interval=interval
    
    def worker(self,isLoop):
        while True:
            print("循环中",isLoop)
            if isLoop:
                print("loop循环中",isLoop)
                try:
                    print(self.loopAction)
                    self.loopAction()
                except BaseException  as e:
                    print (e)
                    #logging.debug('debug 信息')
                    #logging.info('info 信息')
                    #logging.warning('warning 信息')
                    logging.error('error 信息 出错误了')
                    #logging.critical('critial 信息')
                
            time.sleep(self.interval)

    def onKeyboardEvent(self,event):
        
        # 监听键盘事件
        #最近使用PyUserInput的KeyboardEvent的时候遇到了KeyboardSwitch() missing 8的情况;
        #该问题具体表现在当你focus的那个进程的窗口title带中文, 就会出现上面那个错误, 如果都是英文或者其他ascii字符则不会;

        #print ("MessageName:", event.MessageName)
        #print ("Message:", event.Message)
        #print ("Time:", event.Time)
        #print ("Window:", event.Window)
        #print ("WindowName:", event.WindowName)
        #print ("Ascii:", event.Ascii, chr(event.Ascii))
        print ("Key:", event.Key)
        #print ("KeyID:", event.KeyID)
        #print ("ScanCode:", event.ScanCode)
        #print ("Extended:", event.Extended)
        #print ("Injected:", event.Injected)
        #print ("Alt", event.Alt)
        #print ("Transition", event.Transition)
        #print ("---")
        
        if event.Key=="S":
            self.isLoop = True
            self.mainProgress = multiprocessing.Process(target = self.worker, args = (self.isLoop,))
            self.mainProgress.start()
            print("设置isLoop",self.isLoop)
        elif  event.Key=="F":
            print("mainProgress进程",self.mainProgress)
            if self.mainProgress:
                self.isLoop = False
                self.mainProgress.terminate()
                print("设置isLoop",self.isLoop)
            
        
        # 同鼠标事件监听函数的返回值df
        return True

    def initKeyboardHook(self,action):
        self.loopAction = action
        # 创建一个“钩子”管理对象
        hm = pyHook.HookManager()
        # 监听所有键盘事件
        hm.KeyDown = self.onKeyboardEvent
        # 设置键盘“钩子”
        hm.HookKeyboard()