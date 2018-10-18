#三消算法===============================================================================================
#查找最佳可消点
lastBombPoint = [[-1,-1],[-2,-2],[-3,-3]]
def find_can_bomb_point(colorArr,weightMap={'w':5,'y':2,'g':5,'n':5,'p':4,'r':6,'b':2,0:0,None:0}):
    global lastBombPoint
    maxBomb = None
    for y in range(8):
        for x in range(8):
            bombInfo = is_can_bomb(colorArr,x,y,weightMap)
            #print (y,x,bombInfo)
            if bombInfo and (maxBomb==None or maxBomb["weight"] <= bombInfo["weight"]):
                bx = bombInfo["x1"]
                by = bombInfo["y1"]
                #防止识别失败,连续移动同一错误位置，导致游戏不能继续
                if( (bx!=lastBombPoint[0][0] and by!=lastBombPoint[0][1]) or (bx!=lastBombPoint[1][0] and by!=lastBombPoint[1][1]) or (bx!=lastBombPoint[2][0] and by!=lastBombPoint[2][1])):
                    maxBomb = bombInfo
    del  lastBombPoint[0]
    lastBombPoint.append([maxBomb["x1"],maxBomb["y1"]])
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