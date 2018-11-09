import win32gui, win32ui, win32con, win32api
import time
from pymouse import PyMouse
m = PyMouse()

#window操作========================================================================================================
#鼠标点击
def mouse_click(x,y):
    m.click(x, y)

#按键
def keyboard_press(key):
    ascii = ord(key)
    win32api.keybd_event(ascii,0,0,0) #ctrl键位码是17
    return True;
    
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
    
