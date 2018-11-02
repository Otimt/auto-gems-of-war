import cv2
from common.img_process import classify_hist_with_split,cat_img

rImgPath = "base\\red.jpg"
wImgPath = "base\\white.jpg"
gImgPath = "base\\green.jpg"
bImgPath = "base\\blue.jpg"
pImgPath = "base\\purple.jpg"
yImgPath = "base\\yellow.jpg"
nImgPath = "base\\brown.jpg"

rImg = cv2.imread(rImgPath)
wImg = cv2.imread(wImgPath)
gImg = cv2.imread(gImgPath)
bImg = cv2.imread(bImgPath)
pImg = cv2.imread(pImgPath)
yImg = cv2.imread(yImgPath)
nImg = cv2.imread(nImgPath)

rImg = cat_img(rImg,60,60,76,76)
wImg = cat_img(wImg,60,60,76,76)
gImg = cat_img(gImg,60,60,76,76)
bImg = cat_img(bImg,60,60,76,76)
pImg = cat_img(pImg,60,60,76,76)
yImg = cat_img(yImg,60,60,76,76)
nImg = cat_img(nImg,60,60,76,76)

#三消算法===============================================================================================
#查找最佳可消点
lastBombPoint = [[-1,-1],[-2,-2],[-3,-3]]
def find_can_bomb_point(colorArr,weightMap={'w':5,'y':2,'g':5,'n':5,'p':4,'r':6,'b':2,0:0,None:0}):
    global lastBombPoint
    maxBomb = None
    for y in range(8):
        for x in range(8):
            bombInfo = is_can_bomb(colorArr,x,y,weightMap)
            if bombInfo:
                print(bombInfo)
            #print (y,x,bombInfo)
            if bombInfo and (maxBomb==None or maxBomb["weight"] <= bombInfo["weight"]):
                bx = bombInfo["x1"]
                by = bombInfo["y1"]
                #防止识别失败,连续移动同一错误位置，导致游戏不能继续
                if( (bx!=lastBombPoint[0][0] and by!=lastBombPoint[0][1]) or (bx!=lastBombPoint[1][0] and by!=lastBombPoint[1][1]) or (bx!=lastBombPoint[2][0] and by!=lastBombPoint[2][1])):
                    maxBomb = bombInfo
    if maxBomb:
        del  lastBombPoint[0]
        lastBombPoint.append([maxBomb["x1"],maxBomb["y1"]])
        print("上次爆破数组",lastBombPoint)
    print(maxBomb)
    return maxBomb


def is_can_bomb(arr,x,y,weightMap):
    
    
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
    
    
#64个图标识别===============================================================================================
#识别 64个 图标存进 colorArr
uncheckedNum = 0
def check64(img,hArr,vArr):
    global uncheckedNum
    colorArr = [([0] * 8) for i in range(8)]
    
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