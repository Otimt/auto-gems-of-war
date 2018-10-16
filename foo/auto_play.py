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

prepareImgPath = "base\\prepare.png"
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

prepareImg = cv2.imread(prepareImgPath)
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
    "name":"huozhadan",
    "target":False,
    "castImg":None,
    "order":1
},{
    "x":319,
    "y":442,
    "name":"huozhadan",
    "target":False,
    "castImg":None,
    "order":2
},{
    "x":319,
    "y":699,
    "name":"taiyangniao",
    "target":True,
    "castImg":None,
    "order":3
},{
    "x":319,
    "y":952,
    "name":False,
    "target":False,
    "castImg":None,
    "order":4
}]
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

  
def continue_click():
    #点击继续
    m.click(1002,1020)
    time.sleep(0.25)
    m.click(1002,1020)
    time.sleep(0.25)
    #点击选择升级
    m.click(1002,950)
    time.sleep(0.25)
    m.click(1002,950)
    time.sleep(0.25)
    #跳过每日活动
    m.click(1902,950)
    time.sleep(0.25)
    m.click(1902,950)
    time.sleep(0.25)


def casting(leftIndex,target=False):
    obj = leftList[leftIndex]
    #if(obj["ready"]):
    if(True):
        m.click(obj["x"],obj["y"])#选中军队
        time.sleep(0.18)
        m.click(950,950)#点击施法
        time.sleep(0.1)
        
        if target:
            for index,obj in enumerate(rightList):
                print("点击敌人",index,obj["live"])
                if obj["live"]:
                    m.click(obj["x"],obj["y"])
                    time.sleep(0.1)
                    m.click(1002,1020)
                    time.sleep(0.1)
        m.click(1002,1020)
        time.sleep(0.1)
    
    
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
            check_left(img)
            colorArr = check64(img)
            if not colorArr:
                return False
            moveInfo = find_can_bomb_point(colorArr)
            if moveInfo:
                print("moveInfo",moveInfo)
                x1 = moveInfo["x1"]
                y1 = moveInfo["y1"]
                x2 = moveInfo["x2"]
                y2 = moveInfo["y2"]
                if moveInfo["weight"] <= 10 and moveInfo["color"]!="w":
                    
                    casting(2)
                    casting(0)
                    casting(1,False)
                    #casting(1,True)
                    
                    
                    
                    
                    
                    m.click(hArr[x1],vArr[y1])
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

    
        
        
#识别准备===============================================================================================
def check_prepare(img):
    curPrepareBtn =  cat_img(img,952,1010,200,50)
    if (classify_hist_with_split(curPrepareBtn,prepareBtn)>0.5):
        #准备中
        #重置敌方数组
        reset_right_list()
        print("检查到准备中")
        #点击继续
        m.click(1002,1020)
        time.sleep(0.25)
        return True
    else:
        print("未检查到准备中")
        return False
        

#重置敌方数组
def reset_right_list():
    for obj in rightList:
        obj["live"] = True
    
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
            res = classify_hist_with_split(castImg,leftCastImg)
            ready = (res>0.5)
            obj["ready"] = ready
            print(obj["name"],"ready",ready,res)
    return True

    
#64个图标识别===============================================================================================
#识别 64个 图标存进 colorArr
def check64(img):
    colorArr = [([0] * 8) for i in range(8)]
    start = time.time()
    imgSize = 76
    for xIndex,xCenter in enumerate(hArr): 
        for yIndex,yCenter in enumerate(vArr):
            imgPart = cat_img(img,xCenter,yCenter,imgSize,imgSize)
    #         imgArr[yIndex][xIndex] = imgPart
            color = compare_color(imgPart)
            colorArr[yIndex][xIndex] = color
            if not color:
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
    if (classify_hist_with_split(imgPart,bImg)[0]>0.48):
        return "b"
    if (classify_hist_with_split(imgPart,wImg)>0.48):
        return "w"
    if (classify_hist_with_split(imgPart,yImg)>0.48):
        return "y"
    if (classify_hist_with_split(imgPart,rImg)>0.48):
        return "r"
    if (classify_hist_with_split(imgPart,pImg)>0.48):
        return "p"
    if (classify_hist_with_split(imgPart,nImg)>0.48):
        return "n"
    if (classify_hist_with_split(imgPart,gImg)>0.48):
        return "g"
    



#三消算法===============================================================================================
#查找最佳可消点
def find_can_bomb_point(colorArr):
    maxBomb = None
    for y in range(8):
        for x in range(8):
            bombInfo = is_can_bomb(colorArr,x,y)
            #print (y,x,bombInfo)
            if bombInfo and (maxBomb==None or maxBomb["weight"] <= bombInfo["weight"]):
                maxBomb = bombInfo
    print(maxBomb)
    return maxBomb

def is_can_bomb(arr,x,y):
    weightMap = {
        'w':6,
        'y':3,
        'g':4,
        'n':4,
        'p':3,
        'r':5,
        'b':3,
        0:0,
        None:0
    }
    
    lWeight = 0
    tWeight = 0
    rWeight = 0
    bWeight = 0
    
    t2 = arr[y-2][x] if y-2>=0 else 0
    t1 = arr[y-1][x] if y-1>=0 else 0
    b1 = arr[y+1][x] if y+1<len(arr) else 0
    b2 = arr[y+2][x] if y+2<len(arr) else 0
    l2 = arr[y][x-2] if x-2>=0 else 0
    l1 = arr[y][x-1] if x-1>=0 else 0
    r1 = arr[y][x+1] if x+1<len(arr) else 0
    r2 = arr[y][x+2] if x+2<len(arr) else 0
    
    if (b1==l1 and l1==r1) or (b1==l1 and l1==l2) or (b1==r1 and r1==r2) or (b1==t1 and t1==t2):
        bWeight = weightMap[b1]
        if (l1==l2 and l1==r1) or (r1==r2 and l1==r1):
            bWeight*=10
        if (l1==l2 and r1==r2 and l1 and r1 and l1==r1) or (l1==l2 and t1==t2 and l1 and t1 and l1==t1) or (t1==t2 and r1==r2 and t1 and r1 and t1==r1) or (r1==l1 and t1==b1 and b1==t2):
            bWeight*=100
    if (t1==l1 and l1==r1) or (t1==l1 and l1==l2) or (t1==r1 and r1==r2) or (t1==b1 and b1==b2):
        tWeight = weightMap[t1]
        if (l1==l2 and l1==r1) or (r1==r2 and l1==r1):
            tWeight*=10
        if (l1==l2 and r1==r2 and l1 and r1 and l1==r1) or (l1==l2 and b1==b2 and l1 and b1 and l1==b1) or (b1==b2 and r1==r2 and b1 and r1 and b1==r1) or (r1==l1 and t1==b1 and t1==b2):
            tWeight*=100
    if (l1==b1 and b1==t1) or (l1==t1 and t1==t2) or (l1==b1 and b1==b2) or (l1==r1 and r1==r2):
        lWeight = weightMap[l1]
        if (t1==t2 and t1==b1) or (b1==b2 and t1==b1):
            lWeight*=10
        if (b1==b2 and r1==r2 and b1 and r1 and b1==r1) or (b1==b2 and t1==t2 and b1 and t1 and b1==t1) or (t1==t2 and r1==r2 and t1 and r1 and t1==r1) or (r1==l1 and t1==b1 and l1==r2):
            lWeight*=100
    if (r1==b1 and b1==t1) or (r1==t1 and t1==t2) or (r1==b1 and b1==b2) or (r1==l1 and l1==l2):
        rWeight = weightMap[r1]
        if (t1==t2 and t1==b1) or (b1==b2 and t1==b1):
            rWeight*=10
        if (l1==l2 and t1==t2 and l1 and t1 and l1==t1) or (l1==l2 and b1==b2 and l1 and b1 and l1==b1) or (t1==t2 and b1==b2 and t1 and b1 and t1==b1) or (r1==l1 and t1==b1 and r1==l2):
            rWeight*=100
    weight = max(tWeight,rWeight,bWeight,lWeight)
    color = None
    x2 = x
    y2 = y
    if(tWeight==weight):
        direction = "t"
        color = t1
        y2 = y-1
    elif(bWeight==weight):
        direction = "b"
        color = b1
        y2 = y+1
    elif(lWeight==weight):
        direction = "l"
        color = l1
        x2 = x-1
    elif(rWeight==weight):
        direction = "r"
        color = r1
        x2 = x+1
   
    if weight==0:
         res = False
    else:
        res = {
            "color":color,
            "direction":direction,
            "weight":weight,
            "x1":x,
            "y1":y,
            "x2":x2,
            "y2":y2,
        } 
    
    return res


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

    

#图片比较基础========================================================================================================
# 最简单的以灰度直方图作为相似比较的实现  
def classify_gray_hist(image1,image2,size = (256,256)):  
    # 先计算直方图  
    # 几个参数必须用方括号括起来  
    # 这里直接用灰度图计算直方图，所以是使用第一个通道，  
    # 也可以进行通道分离后，得到多个通道的直方图  
    # bins 取为16  
    image1 = cv2.resize(image1,size)  
    image2 = cv2.resize(image2,size)  
    hist1 = cv2.calcHist([image1],[0],None,[256],[0.0,255.0])  
    hist2 = cv2.calcHist([image2],[0],None,[256],[0.0,255.0])  
    # 可以比较下直方图  
    plt.plot(range(256),hist1,'r')  
    plt.plot(range(256),hist2,'b')  
    plt.show()  
    # 计算直方图的重合度  
    degree = 0  
    for i in range(len(hist1)):  
        if hist1[i] != hist2[i]:  
            degree = degree + (1 - abs(hist1[i]-hist2[i])/max(hist1[i],hist2[i]))  
        else:  
            degree = degree + 1  
    degree = degree/len(hist1)  
    return degree  
  
# 计算单通道的直方图的相似值  
def calculate(image1,image2):  
    hist1 = cv2.calcHist([image1],[0],None,[256],[0.0,255.0])  
    hist2 = cv2.calcHist([image2],[0],None,[256],[0.0,255.0])  
     # 计算直方图的重合度  
    degree = 0  
    for i in range(len(hist1)):  
        if hist1[i] != hist2[i]:  
            degree = degree + (1 - abs(hist1[i]-hist2[i])/max(hist1[i],hist2[i]))  
        else:  
            degree = degree + 1  
    degree = degree/len(hist1)  
    return degree  
  
# 通过得到每个通道的直方图来计算相似度  
def classify_hist_with_split(image1,image2,size = (256,256)):  
    # 将图像resize后，分离为三个通道，再计算每个通道的相似值  
    image1 = cv2.resize(image1,size)  
    image2 = cv2.resize(image2,size)  
    sub_image1 = cv2.split(image1)  
    sub_image2 = cv2.split(image2)  
    sub_data = 0  
    for im1,im2 in zip(sub_image1,sub_image2):  
        sub_data += calculate(im1,im2)  
    sub_data = sub_data/3  
    return sub_data  
  
# 平均哈希算法计算  
def classify_aHash(image1,image2):  
    image1 = cv2.resize(image1,(8,8))  
    image2 = cv2.resize(image2,(8,8))  
    gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)  
    gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)  
    hash1 = getHash(gray1)  
    hash2 = getHash(gray2)  
    return Hamming_distance(hash1,hash2)  
  
def classify_pHash(image1,image2):  
    image1 = cv2.resize(image1,(32,32))  
    image2 = cv2.resize(image2,(32,32))  
    gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)  
    gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)  
    # 将灰度图转为浮点型，再进行dct变换  
    dct1 = cv2.dct(np.float32(gray1))  
    dct2 = cv2.dct(np.float32(gray2))  
    # 取左上角的8*8，这些代表图片的最低频率  
    # 这个操作等价于c++中利用opencv实现的掩码操作  
    # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分  
    dct1_roi = dct1[0:8,0:8]  
    dct2_roi = dct2[0:8,0:8]  
    hash1 = getHash(dct1_roi)  
    hash2 = getHash(dct2_roi)  
    return Hamming_distance(hash1,hash2)  
  
# 输入灰度图，返回hash  
def getHash(image):  
    avreage = np.mean(image)  
    hash = []  
    for i in range(image.shape[0]):  
        for j in range(image.shape[1]):  
            if image[i,j] > avreage:  
                hash.append(1)  
            else:  
                hash.append(0)  
    return hash  
  
  
# 计算汉明距离
def Hamming_distance(hash1,hash2):  
    num = 0  
    for index in range(len(hash1)):  
        if hash1[index] != hash2[index]:  
            num += 1  
    return num  
    

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