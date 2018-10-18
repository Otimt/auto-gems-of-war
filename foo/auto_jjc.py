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

from common.check_bomb import find_can_bomb_point
from common.comp_img import classify_hist_with_split

# import the module
from pymouse import PyMouse
m = PyMouse()

#截取图片中心
def cat_img(img,xCenter,yCenter,imgWidth,imgHeight):
    x = int(xCenter - imgWidth/2)
    y = int(yCenter - imgHeight/2)
    imgPart = img[y:(y+imgHeight),x:(x+imgWidth)]
    return imgPart

#初始化我方技能检查图片
def init_left(leftList):
    for obj in leftList:
        if obj["name"]:
            path = "cast\\"+obj["name"]+".png"
            print(path)
            castImg = cv2.imread(path)
            print(len(castImg))
            obj["castImg"] = castImg
    return True

    
hArr = [545,662,780,899,1018,1137,1253,1373]
vArr = [140,261,378,495,618,737,851,973]

jjcEnterPath = "base\\jjc_enter.png"
prepareImgPath = "base\\prepare.png"
jjcPrepareImgPath = "base\\jjc-prepare.png"
realJjcPrepareImgPath = "base\\real-jjc-prepare.png"
rImgPath = "base\\red.jpg"
wImgPath = "base\\white.jpg"
gImgPath = "base\\green.jpg"
bImgPath = "base\\blue.jpg"
pImgPath = "base\\purple.jpg"
yImgPath = "base\\yellow.jpg"
nImgPath = "base\\brown.jpg"
dead1ImgPath = "base\\right_dead_1.png"
dead2ImgPath = "base\\right_dead_2.png"
dead3ImgPath = "base\\right_dead_3.png"
dead4ImgPath = "base\\right_dead_4.png"
fightLeftImgPath = "base\\fight_left.png"
fightRightImgPath = "base\\fight_right.png"
overImgPath = "base\\over.png"


jjcEnterImg = cv2.imread(jjcEnterPath)
prepareImg = cv2.imread(prepareImgPath)
jjcPrepareImg = cv2.imread(realJjcPrepareImgPath)
rImg = cv2.imread(rImgPath)
wImg = cv2.imread(wImgPath)
gImg = cv2.imread(gImgPath)
bImg = cv2.imread(bImgPath)
pImg = cv2.imread(pImgPath)
yImg = cv2.imread(yImgPath)
nImg = cv2.imread(nImgPath)
dead1Img  = cv2.imread(dead1ImgPath)
dead2Img  = cv2.imread(dead2ImgPath)
dead3Img  = cv2.imread(dead3ImgPath)
dead4Img  = cv2.imread(dead4ImgPath)
fightLeftImg = cv2.imread(fightLeftImgPath)
fightRightImg = cv2.imread(fightRightImgPath)
overImg = cv2.imread(overImgPath)

prepareBtn = cat_img(prepareImg,952,1010,200,50)
jjcPrepareBtn = cat_img(jjcPrepareImg,959,1009,241,53)
jjcHuozhadanImg = cat_img(jjcPrepareImg,449,600,100,100)
rImg = cat_img(rImg,60,60,76,76)
wImg = cat_img(wImg,60,60,76,76)
gImg = cat_img(gImg,60,60,76,76)
bImg = cat_img(bImg,60,60,76,76)
pImg = cat_img(pImg,60,60,76,76)
yImg = cat_img(yImg,60,60,76,76)
nImg = cat_img(nImg,60,60,76,76)
dead1Img = cat_img(dead1Img,50,50,100,100)
dead2Img = cat_img(dead2Img,50,50,100,100)
dead3Img = cat_img(dead3Img,50,50,100,100)
dead4Img = cat_img(dead4Img,50,50,100,100)
    

#我方数组
leftList = [{
    "x":319,
    "y":189,
    "name":"shanmaifensuizhe",
    "target":False,
    "castImg":None
},{
    "x":319,
    "y":442,
    "name":"xingtian",
    "target":False,
    "castImg":None
},{
    "x":319,
    "y":699,
    "name":"duyaodashi",
    "target":False,
    "castImg":None
},{
    "x":319,
    "y":952,
    "name":"",
    "target":False,
    "castImg":None
}]
weightMap = {
    'w':5,
    'y':2,
    'g':5,
    'n':5,
    'p':4,
    'r':6,
    'b':2,
    0:0,
    None:0
}
#敌方数组
rightList = [{
    "x":1602,
    "y":189,
    "live":True,
    "deadImg":dead1Img
},{
    "x":1602,
    "y":442,
    "live":True,
    "deadImg":dead2Img
},{
    "x":1602,
    "y":699,
    "live":True,
    "deadImg":dead3Img
},{
    "x":1602,
    "y":952,
    "live":True,
    "deadImg":dead4Img
}]
init_left(leftList)

resetX = 1208
def continue_click():
    #点击继续
    m.click(resetX,1020)
    time.sleep(0.25)
    m.click(resetX,1020)
    time.sleep(0.25)
    #点击选择升级
    m.click(resetX,950)
    time.sleep(0.25)
    m.click(resetX,950)
    time.sleep(0.25)
    #跳过每日活动
    m.click(1902,950)
    time.sleep(0.25)
    m.click(1902,950)
    time.sleep(0.25)


def casting(leftIndex):
    obj = leftList[leftIndex]
    #if(obj["ready"]):
    if(True):
    
        m.click(obj["x"],obj["y"])#选中军队
        time.sleep(0.1)
        m.click(950,950)#点击施法
        time.sleep(0.1)
        target=obj["target"]
        if target:
            for index,obj in enumerate(rightList):
                print("点击敌人",index,obj["live"])
                if obj["live"]:
                    m.click(obj["x"],obj["y"])
                    time.sleep(0.1)
                    m.click(resetX,1020)
                    time.sleep(0.1)
        m.click(resetX,1020)
        time.sleep(0.1)
    
    
#移动一步
def moveOnce():
    #截屏
    imgPath = "game2.jpg"
    window_capture(imgPath)
    img = cv2.imread(imgPath)
    if(check_main_view(img)):
        return True
    if check_jjc_prepare(img):
        #竞技场准备中，刷火炸弹
        return True
    elif check_prepare(img):
        #准备中
        return True
    elif check_fight(img):
        #战斗中
        check_right(img)
        if not is_all_right_dead(img):
            #敌方未全灭
            check_left(img)
            colorArr = check64(img)
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
                    
                    casting(1)
                    casting(0)
                    casting(2)
                    #casting(2)
                    
                    
                    m.click(2,2)
                    time.sleep(0.1)
                    m.click(hArr[x1],vArr[y1])
                    time.sleep(0.2)
                
                mouse_drag(hArr[x1],vArr[y1],hArr[x2],vArr[y2])
                print(hArr[x1],vArr[y1],hArr[x2],vArr[y2])
                time.sleep(2)
        else:
            print("敌方全灭")
    else:
        continue_click()

    del img
    #print ("\nbegin collect...")
    _unreachable = gc.collect()
    #print ("unreachable object num:%d" %(_unreachable))
    #print ("garbage object num:%d" %(len(gc.garbage))   #gc.garbage是一个list对象，列表项是垃圾收集器发现的不可达（即垃圾对象）、但又不能释放(不可回收)的对象，通常gc.garbage中的对象是引用对象还中的对象。因Python不知用什么顺序来调用对象的__del__函数，导致对象始终存活在gc.garbage中，造成内存泄露 if __name__ == "__main__": test_gcleak()。如果知道一个安全次序，那么就可以打破引用焕，再执行del gc.garbage[:]从而清空垃圾对象列表
        
        
        
#识别准备===============================================================================================
def check_main_view(img):
    
    btn = cat_img(img,360,978,80,80)
    matchJjc = (classify_hist_with_split(btn,jjcEnterImg))
    print("比较竞技场入口",matchJjc)
    print(len(jjcEnterImg))
    if matchJjc>0.5:
        #点击竞技场入口
        m.click(360,978)
        return True

def check_jjc_prepare(img):
    btn = cat_img(img,959,1009,241,53)
    if(classify_hist_with_split(btn,jjcPrepareBtn)>0.5):
        #竞技场准备
        jjcArr = [[1469,600],[959,600],[449,600]]
        #jjcArr = [[449,600]]
        for arr in jjcArr:
            target = cat_img(img,arr[0],arr[1],100,100)
            if(classify_hist_with_split(target,jjcHuozhadanImg)>0.5):
                print("遇到火炸弹，点炸弹")
                #遇到火炸弹，点炸弹
                m.click(arr[0],600);
                time.sleep(0.2)
                return True
        #未遇到火炸弹，点最左
        print("未遇到火炸弹，点中")
        m.click(jjcArr[1][0],900)
        time.sleep(0.25)
        return True
    else:
        return False
    jjcHuozhadanImg
    jjcPrepareBtn
    
    
def check_prepare(img):
    curPrepareBtn =  cat_img(img,952,1010,200,50)
    if (classify_hist_with_split(curPrepareBtn,prepareBtn)>0.5):
        #准备中
        #重置敌方数组
        reset_right_list()
        print("检查到准备中")
        #点击继续
        m.click(resetX,1020)
        time.sleep(0.25)
        return True
    else:
        print("未检查到准备中")
        return False
        

#重置敌方数组
def reset_right_list():
    for obj in rightList:
        obj["live"] = True

#战斗=================================================================================
#识别战斗中界面
def check_fight(img):
    leftImg = cat_img(img,55,55,64,64)
    rightImg = cat_img(img,1865,55,64,64)
    left = classify_hist_with_split(fightLeftImg,leftImg)
    right = classify_hist_with_split(fightRightImg,rightImg)
    print("识别战斗中界面 left",left,"right",right)
    if (left>0.5) or (right>0.5):
        print("战斗中中")
        return True
    else :
        print("未战斗中中")
        return False

#识别敌方数组
def check_right(img):
    #for index,obj in enumerate(rightList):
    #    
    #    rightImg = cat_img(img,obj["x"],obj["y"],100,100)
    #    deadImg = obj["deadImg"]
    #    live = classify_hist_with_split(rightImg,deadImg)
    #    if (live>0.5):
    #        obj["live"] = False
    #    else:
    #        obj["live"] = True
    #    print("敌人",index,"活着：",obj["live"],live)
    return True
    
#敌方全灭否
def is_all_right_dead(img):
    centerImg = cat_img(img,960,540,80,80)
    return (classify_hist_with_split(centerImg,overImg)>0.5)

    
#识别我方数组是否准备好
def check_left(img):
    for obj in leftList:
        if obj["name"]:
            castImg = obj["castImg"]
            leftCastImg = cat_img(img,obj["x"],obj["y"],100,100)
            ready = (classify_hist_with_split(castImg,leftCastImg)>0.5)
            obj["ready"] = ready
            print(obj["name"],"ready",ready)
    return True

    
#64个图标识别===============================================================================================
#识别 64个 图标存进 colorArr
uncheckedNum = 0
def check64(img):
    global uncheckedNum
    colorArr = [([0] * 8) for i in range(8)]
    start = time.time()
    imgSize = 76
    for xIndex,xCenter in enumerate(hArr): 
        for yIndex,yCenter in enumerate(vArr):
            imgPart = cat_img(img,xCenter,yCenter,imgSize,imgSize)
    #         imgArr[yIndex][xIndex] = imgPart
            color = compare_color(imgPart)
            colorArr[yIndex][xIndex] = color
            if (not color) and (uncheckedNum<5):
                uncheckedNum  += 1
                print(yIndex,xIndex ,"未识别")
                return False
    #         cv2.imwrite(str(yIndex)+str(xIndex)+".bmp",imgPart)
    #         plt.imshow(imgPart)
    #         plt.show()
    #         print(yIndex,xIndex)
    # plt.imshow(imgArr[0][0])
    # plt.show()

    end = time.time()
    print (end-start)
    print (colorArr)
    return colorArr

#识别7种颜色
def compare_color(imgPart):
    compValue = 0.49
    if (classify_hist_with_split(imgPart,bImg)[0]>compValue):
        return "b"
    if (classify_hist_with_split(imgPart,wImg)>compValue):
        return "w"
    if (classify_hist_with_split(imgPart,yImg)>compValue):
        return "y"
    if (classify_hist_with_split(imgPart,rImg)>compValue):
        return "r"
    if (classify_hist_with_split(imgPart,pImg)>compValue):
        return "p"
    if (classify_hist_with_split(imgPart,nImg)>compValue):
        return "n"
    if (classify_hist_with_split(imgPart,gImg)>compValue):
        return "g"
    






#window操作========================================================================================================
#鼠标拖拽
def mouse_drag(x,y,x2,y2):
    # instantiate an mouse object
    screen_size = m.screen_size()
    m.move(x, y)    #鼠标移动到  
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)    #左键按下
    time.sleep(0.05)
    SW = screen_size[0]
    SH = screen_size[1]
    mw = int(x2 * 65535 / SW) 
    mh = int(y2 * 65535 / SH)
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE + win32con.MOUSEEVENTF_MOVE, mw, mh, 0, 0)    
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
#截屏
def window_capture(filename):
    hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
	#ReleaseDC函数
    #函数功能：函数释放设备上下文环境（DC）供其他应用程序使用。函数的效果与设备上下文环境类型有关。它只释放公用的和设备上下文环境，对于类或私有的则无数。
    #函数原型：int ReleaseDC(HWND hWnd, HDC hdc)；
    #参数：
    #hWnd：指向要释放的设备上下文环境所在的窗口的句柄。
    #hDC：指向要释放的设备上下文环境的句柄。
    #返回值：返回值说明了设备上下文环境是否释放；如果释放成功，则返回值为1；如果没有释放成功，则返回值为0。
    #注释：每次调用GetWindowDC和GetDC函数检索公用设备上下文环境之后，应用程序必须调用ReleaseDC函数来释放设备上下文环境。
    #应用程序不能调用ReleaseDC函数来释放由CreateDC函数创建的设备上下文环境，只能使用DeleteDC函数。
    win32gui.ReleaseDC(hwnd,hwndDC)
    

    


    
    


def worker(isLoop):
    while True:
        print("循环中",isLoop)
        if isLoop:
            print("loop循环中",isLoop)
            moveOnce()
        time.sleep(1)
        
        
mainProgress = None
def onKeyboardEvent(event):
    global isLoop
    global mainProgress
    # 监听键盘事件
    #最近使用PyUserInput的KeyboardEvent的时候遇到了KeyboardSwitch() missing 8的情况;
    #该问题具体表现在当你focus的那个进程的窗口title带中文, 就会出现上面那个错误, 如果都是英文或者其他ascii字符则不会;

    print ("MessageName:", event.MessageName)
    print ("Message:", event.Message)
    print ("Time:", event.Time)
    print ("Window:", event.Window)
    print ("WindowName:", event.WindowName)
    print ("Ascii:", event.Ascii, chr(event.Ascii))
    print ("Key:", event.Key)
    print ("KeyID:", event.KeyID)
    print ("ScanCode:", event.ScanCode)
    print ("Extended:", event.Extended)
    print ("Injected:", event.Injected)
    print ("Alt", event.Alt)
    print ("Transition", event.Transition)
    print ("---")
    
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