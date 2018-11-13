import time
import win32gui, win32ui, win32con, win32api
import numpy as np
import matplotlib.pyplot as plt
import cv2
import datetime
import gc

import pythoncom

import json



from common.check_bomb import find_can_bomb_point,check64
from common.img_process import classify_hist_with_split,cat_img
from common.game_action import *
from common.window_action import *
from common.loop import Loop

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
    
    if check_windows(img):
        #检测到桌面，不执行任何动作，方便切换到cmd 结束进程
        return True
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
            else:
                uncheckedNum = uncheckedNum+1
                print("未识别可移动单元格",uncheckedNum)
                if uncheckedNum>10:
                    #10次识别不了可移动，点撤退
                    retreat()
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

    


    


def main():
    
    #初始化键盘钩子 监听 键盘事件
    Loop().initKeyboardHook(moveOnce)
    
    # 进入循环，如不手动关闭，程序将一直处于监听状态dd
    pythoncom.PumpMessages()
    
    
    
    
    
  
if __name__ == "__main__":
    main()