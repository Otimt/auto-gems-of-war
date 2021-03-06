#游戏内容相关方法

# import the module
import cv2
import time
from common.img_process import classify_hist_with_split,cat_img
from pymouse import PyMouse
m = PyMouse()

#操作系统桌面
windowsImgPath = "base\\windows.png"
windowsImg = cv2.imread(windowsImgPath)
windowsImg = cat_img(windowsImg,20,1060,40,40)

#主界面
mainPath = "base\\main.png"
mainImg = cv2.imread(mainPath)

#探索 准备界面
prepareImgPath = "base\\prepare.png"
prepareImg = cv2.imread(prepareImgPath)
prepareBtn = cat_img(prepareImg,952,1010,200,50)

#pvp 休闲战 准备界面
jjcPrepareImgPath = "base\\jjc-prepare.png"

#pvp 排位战 准备界面
realJjcPrepareImgPath = "base\\real-jjc-prepare.png"
jjcPrepareImg = cv2.imread(realJjcPrepareImgPath)
jjcPrepareBtn = cat_img(jjcPrepareImg,959,1009,241,53)

#敌方是否生存判断 2018-11-12 10:01:27 未使用这些图片
dead1ImgPath = "base\\right_dead_1.png"
dead2ImgPath = "base\\right_dead_2.png"
dead3ImgPath = "base\\right_dead_3.png"
dead4ImgPath = "base\\right_dead_4.png"
dead1Img  = cv2.imread(dead1ImgPath)
dead2Img  = cv2.imread(dead2ImgPath)
dead3Img  = cv2.imread(dead3ImgPath)
dead4Img  = cv2.imread(dead4ImgPath)

#施法中 需要点击 敌人或自己
castingPath = "base\\select-an-enemy.png"
castingImg  = cv2.imread(castingPath)

#战斗中 左上角 右上角 标记图标
fightLeftImgPath = "base\\fight_left.png"
fightRightImgPath = "base\\fight_right.png"
fightLeftImg = cv2.imread(fightLeftImgPath)
fightRightImg = cv2.imread(fightRightImgPath)

#加载中 识别标记
overImgPath = "base\\over.png"
overImg = cv2.imread(overImgPath)













jjcHuozhadanImg = cat_img(jjcPrepareImg,449,600,100,100)

dead1Img = cat_img(dead1Img,50,50,100,100)
dead2Img = cat_img(dead2Img,50,50,100,100)
dead3Img = cat_img(dead3Img,50,50,100,100)
dead4Img = cat_img(dead4Img,50,50,100,100)

#敌方数组
rightList = [{
    "x":1722,
    "y":189,
    "live":True,
    "deadImg":dead1Img
},{
    "x":1722,
    "y":442,
    "live":True,
    "deadImg":dead2Img
},{
    "x":1722,
    "y":699,
    "live":True,
    "deadImg":dead3Img
},{
    "x":1722,
    "y":952,
    "live":True,
    "deadImg":dead4Img
}]


#界面===============================================================================================
def check_windows(img):
    #截取左下角 ,比较windows 开始按钮
    btn = cat_img(img,20,1060,40,40)
    matchWindows = classify_hist_with_split(btn,windowsImg)
    print("比较桌面",matchWindows)
    if matchWindows>0.5:
        return True
    return False

#识别主界面
def check_main_view(img):
    btn = cat_img(img,360,978,80,80)
    jjcEnterImg = cat_img(mainImg,360,978,80,80)
    matchJjc = (classify_hist_with_split(btn,jjcEnterImg))
    
    btn = cat_img(img,560,978,80,80)
    gameEnterImg = cat_img(mainImg,560,978,80,80)
    matchGame = (classify_hist_with_split(btn,gameEnterImg))
    
    print("识别主界面：matchJjc",matchJjc,"matchGame",matchGame)
    
    if matchJjc>0.5 and matchGame>0.5:
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


#识别准备
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
        

#识别施法中
def check_casting(img):
    leftImg = cat_img(img,55,55,64,64)
    rightImg = cat_img(img,1865,55,64,64)
    
    castingLeftImg = cat_img(castingImg,55,55,64,64)
    castingRightImg = cat_img(castingImg,1865,55,64,64)
    
    left = classify_hist_with_split(castingLeftImg,leftImg)
    right = classify_hist_with_split(castingRightImg,rightImg)
    print("识别施法中界面 left",left,"right",right)
    if (left>0.5) or (right>0.5):
        print("施法中")
        return True
    else :
        print("未施法中")
        return False

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

    


#我方相关操作=================================================================================
#初始化我方技能检查图片
leftList = [];
def init_left(list):
    global leftList
    #for obj in list:
        #if obj["name"]:
            #path = "cast\\"+obj["name"]+".png"
            #print(path)
            #castImg = cv2.imread(path)
            #print(len(castImg))
            #obj["castImg"] = castImg
    leftList = list
    return True
    



    
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

#点击继续
resetX = 1266
def continue_click():
    
    m.click(resetX,1020)
    time.sleep(0.25)
    m.click(resetX,1020)
    time.sleep(0.25)
    #点击选择升级
    m.click(resetX-400,950)
    time.sleep(0.15)
    m.click(resetX-400,950)
    time.sleep(0.15)
    #跳过每日活动
    m.click(1902,950)
    time.sleep(0.2)
    m.click(1902,950)
    time.sleep(0.2)
    m.click(1902,950)
    time.sleep(0.2)
    clickEnemy()

#施法
def casting(leftIndex):
    obj = leftList[leftIndex]
    #if(obj["ready"]):
    if(obj["name"]):
    
        m.click(obj["x"],obj["y"])#选中军队
        time.sleep(0.15)
        m.click(950,950)#点击施法
        time.sleep(0.1)
        target=obj["target"]
        if target:
            clickEnemy()
        m.click(resetX,1020)
        time.sleep(0.1)
        
#点击敌人
def clickEnemy():
    for index,obj in enumerate(rightList):
        print("点击敌人",index,obj["live"])
        if obj["live"]:
            m.click(obj["x"],obj["y"])
            time.sleep(0.1)
    m.click(resetX-400,950)
    time.sleep(0.1)
    
        
#撤退
def retreat():
    m.click(2,2)
    time.sleep(0.2)
    m.click(1040,40)
    time.sleep(0.2)
    m.click(1000,800)
    time.sleep(0.2)
    m.click(1200,700)
    time.sleep(2)
        
#敌方相关操作=========================================================        
        
#重置敌方数组
def reset_right_list():
    for obj in rightList:
        obj["live"] = True
        

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