#图像处理相关方法

import cv2
import numpy as np
import collections


#截取图片中心
def cat_img(img,xCenter,yCenter,imgWidth,imgHeight):
    x = int(xCenter - imgWidth/2)
    y = int(yCenter - imgHeight/2)
    imgPart = img[y:(y+imgHeight),x:(x+imgWidth)]
    return imgPart
    

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


def getColorList():
    dict = collections.defaultdict(list)

    # 棕色
    # lower_black = np.array([0, 60, 26])
    # upper_black = np.array([15, 130, 160])
    # color_list = []
    # color_list.append(lower_black)
    # color_list.append(upper_black)
    # dict['n'] = color_list
    # 棕色2
    lower_black = np.array([155, 60, 26])
    upper_black = np.array([180, 130, 160])
    color_list = []
    color_list.append(lower_black)
    color_list.append(upper_black)
    dict['n'] = color_list

    # 白色
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([50, 52, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['w'] = color_list
    # 白色2
    lower_white = np.array([0, 26, 143])
    upper_white = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['w2'] = color_list
    # 白色3（黑色部分）
    # lower_white = np.array([100, 0, 0])
    # upper_white = np.array([180, 76, 76])
    # color_list = []
    # color_list.append(lower_white)
    # color_list.append(upper_white)
    # dict['w3'] = color_list

    # 红色
    lower_red = np.array([0, 180, 135])
    upper_red = np.array([5, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['r'] = color_list

    # 红色2
    lower_red = np.array([175, 180, 135])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['r'] = color_list

    # 黄色
    lower_yellow = np.array([16, 97, 138])
    upper_yellow = np.array([26, 230, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['y'] = color_list

    # 绿色
    lower_green = np.array([43, 148, 107])
    upper_green = np.array([64, 234, 236])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['g'] = color_list

    # 蓝色
    lower_blue = np.array([91, 122, 112])
    upper_blue = np.array([121, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(upper_blue)
    dict['b'] = color_list

    # 紫色
    lower_purple = np.array([130, 153, 115])
    upper_purple = np.array([148, 231, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(upper_purple)
    dict['p'] = color_list

    return dict


def get_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        cv2.imwrite(d + '.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=2)
        img, cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        if sum > maxsum:
            maxsum = sum
            color = d

    return color[0]
