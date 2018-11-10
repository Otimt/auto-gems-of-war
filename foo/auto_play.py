import time
import win32gui, win32ui, win32con, win32api
import numpy as np
import matplotlib.pyplot as plt
import cv2
import datetime
import gc
import pyHook
import pythoncom
import multiprocessing
import logging
import json

logging.basicConfig(
    level=logging.DEBUG,#控制台打印的日志级别
    filename='new.log',
    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    #a是追加模式，默认如果不写的话，就是追加模式
    format= '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    #日志格式
)

from common.check_bomb import find_can_bomb_point,check64
from common.img_process import classify_hist_with_split,cat_img
from common.game_action import *
from common.window_action import *

# import the module
from pymouse import PyMouse
m = PyMouse()



    
hArr = [545,662,780,899,1018,1137,1253,1373]
vArr = [140,261,378,495,618,737,851,973]






#火鸟炸弹
bombJsonPath = "strategy/bomb.json"
#贪枪
goldJsonPath = "strategy/gold.json"
#魂刷
soulJsonPath = "strategy/soul.json"
#周活动
weekJsonPath = "strategy/week.json"
#刑天
xingJsonPath = "strategy/xing.json"

strategy = json.load(open(bombJsonPath,'r'))
#我方数组
leftList = strategy["team"]
#对leftList按order排序
leftList = sorted(leftList, key=lambda student: student['order'],reverse=True)
#珠子权重
weightMap = strategy["weightMap"]
weightMap[0] = 0
weightMap[None] = 0

init_left(leftList)



    
    
#移动一步
def moveOnce():
    #截屏
    imgPath = "game2.jpg"
    window_capture(imgPath)
    img = cv2.imread(imgPath)
    
    if check_prepare(img):
        #准备中
        return True
    elif check_fight(img):
        #战斗中
        check_right(img)
        if not is_all_right_dead(img):
            #敌方未全灭
            #check_left(img)
            colorArr = check64(img,hArr,vArr)
            if not colorArr:
                return False
            moveInfo = find_can_bomb_point(colorArr,weightMap)
            if moveInfo:
                print("moveInfo",moveInfo)
                x1 = moveInfo["x1"]
                y1 = moveInfo["y1"]
                x2 = moveInfo["x2"]
                y2 = moveInfo["y2"]
                if moveInfo["weight"] <= 10:
                    
                    casting(0)
                    casting(1)
                    casting(2)
                    casting(3)
                    
                    
                    
                    
                    
                    m.click(hArr[x1],vArr[y1])
                    time.sleep(0.1)
                    m.click(hArr[x1],vArr[y1])
                    time.sleep(0.1)
                m.click(2,2)
                time.sleep(0.1)
                mouse_drag(hArr[x1],vArr[y1],hArr[x2],vArr[y2])
                print(hArr[x1],vArr[y1],hArr[x2],vArr[y2])
                time.sleep(2)
            del moveInfo,colorArr
        else:
            print("敌方全灭")
    else:
        continue_click()
        
    del img,imgPath
    print ("\nbegin collect...")
    _unreachable = gc.collect()
    print ("unreachable object num:%d" ,(_unreachable))
    #print ("garbage object num:%d" ,(len(gc.garbage))   #gc.garbage是一个list对象，列表项是垃圾收集器发现的不可达（即垃圾对象）、但又不能释放(不可回收)的对象，通常gc.garbage中的对象是引用对象还中的对象。因Python不知用什么顺序来调用对象的__del__函数，导致对象始终存活在gc.garbage中，造成内存泄露 if __name__ == "__main__": test_gcleak()。如果知道一个安全次序，那么就可以打破引用焕，再执行del gc.garbage[:]从而清空垃圾对象列表

    


    

def worker(isLoop):
    while True:
        print("循环中",isLoop)
        if isLoop:
            print("loop循环中",isLoop)
            try:
                moveOnce()
            except BaseException  as e:
                print (e)
                #logging.debug('debug 信息')
                #logging.info('info 信息')
                #logging.warning('warning 信息')
                logging.error('error 信息 出错误了')
                #logging.critical('critial 信息')
        time.sleep(1)
        
        
mainProgress = None
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
    print ("按键Key:", event.Key)
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



def main():

    
    
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()
    
        
    # 进入循环，如不手动关闭，程序将一直处于监听状态dd
    pythoncom.PumpMessages()
    
    
    
    
    
  
if __name__ == "__main__":
    main()