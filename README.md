#### 截取屏幕
win32gui, win32ui, win32con, win32api  
注意垃圾回收

#### 识别图标
OpenCV是一个基于BSD许可（开源）发行的跨平台计算机视觉库，实现了图像处理和计算机视觉方面的很多通用算法。  
Python OpenCV 图像相识度对比——hist直方图比较  
相似度比较技术 轮廓发现、边缘检测、图像梯度、模板匹配、直方图  

识别桌面：停止自动游戏循环
识别主界面  
识别准备界面  
识别记载中界面  
识别[红黄蓝紫绿棕白]8种图标，塞进一个[8×8]数组

#### 角色、技能策略和消除优先级
角色数组拆分进各个 json文件  
读取json文件，角色按施法权重排序

#### 三消算法
[8×8]数组  
- 可移动检测  
三消游戏提示算法，十字检测 64*8  
todo 所有可移动步骤记录进数组  
- 下落后连续消除检测  
todo 检测4种下落后可连消形状  
  1. AAXX  
XXAA  
  2. XXAX  
XXXX    
XXXX  
AAXA　　
  3. XAX  
XAX  
XBX  
BXB  
XBX  
XAX  
XAX  
  4. XXAXX  
BXAXB  
XBBBX  
BXAXB  
XXAXX  
- 多次未能识别可移动单元格，点击撤退

#### 鼠标操作
pymouse  

#### 按键监听，启动结束进程
pyHook  
multiprocessing  

#### scoket 服务器双向通信
服务器  
1. 发送 获取截图命令  
2. 发送 控制鼠标操作命令  
3. 发送 启动/停止命令  
4. 发送 关机命令  
5. 监控程序运行状态  

客户端
1. 响应 获取截图命令  
2. 响应 控制鼠标操作命令  
3. 响应 启动/停止命令，执行/停止预置的一套操作  
4. 响应 关机命令  
5. 发送程序运行状态


#### 桌面程序GUI
1. Tkinter 是使用 python 进行窗口视窗设计的模块。Tkinter模块("Tk 接口")是Python的标准Tk GUI工具包的接口。作为 python 特定的GUI界面，是一个图像的窗口，tkinter是python 自带的，可以编辑的GUI界面。  
2. wxPython是一个开源的、跨平台的、使用C++开发的GUI工具库，目前支持Windows、大多数的Unix和Linux以及苹果Mac OSX以及手机操作系统iOS、Sybian、android等。boaconstructor可以帮助我们快速可视地构建wxwidgets界面。  
3. Qt同样是一种开源的GUI库，Qt的类库大约在300多个，函数大约在5700多个。Qt同样适合于大型应用，由它自带的qt designer可以让我们轻松来构建界面元素。

#### 异常处理
```
try：
    pass
except (IOError ,ZeroDivisionError),e:
    print e
```

#### 日志
1. 异常日志
2. 开局日志
