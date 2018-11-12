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

mainProgress = None
loopAction = None


def worker(isLoop):
    while True:
        print("循环中",isLoop)
        if isLoop:
            print("loop循环中",isLoop)
            try:
                loopAction()
            except BaseException  as e:
                print (e)
                #logging.debug('debug 信息')
                #logging.info('info 信息')
                #logging.warning('warning 信息')
                logging.error('error 信息 出错误了')
                #logging.critical('critial 信息')
            
        time.sleep(2)
        
        

def onKeyboardEvent(event):
    global isLoop
    global mainProgress
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
        isLoop = True
        mainProgress = multiprocessing.Process(target = worker, args = (isLoop,))
        mainProgress.start()
        print("设置isLoop",isLoop)
    elif  event.Key=="F":
        print("mainProgress进程",mainProgress)
        if mainProgress:
            isLoop = False
            mainProgress.terminate()
            print("设置isLoop",isLoop)
        
    
    # 同鼠标事件监听函数的返回值df
    return True

def initKeyboardHook(action):
    global loopAction
    loopAction = action
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()