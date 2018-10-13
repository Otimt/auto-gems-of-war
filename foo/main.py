import time
import pygame                   # 导入pygame库
import auto_jjc 
import pyHook
# 定义窗口的分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

  
# 初始化游戏
pygame.init()                   # 初始化pygame
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])     # 初始化窗口
pygame.display.set_caption('This is my first pygame-program')       # 设置窗口标题


isLoop=False

# 事件循环(main loop)
while True:                                        
    
    if isLoop:
        auto_jjc.moveOnce()
        time.sleep(1)
        #auto_jjc.move
    
    # 处理游戏退出
    # 从消息队列中循环取
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Python中没有switch-case 多用字典类型替代
        # 控制方向 == new add ==        
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_UP:
                isLoop = True
            elif event.key == pygame.K_DOWN:
                isLoop = False
