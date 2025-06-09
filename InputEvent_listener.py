import win32gui
from pynput import mouse
from Capture_xcg import capture_yxp_window, capture_upgrade
from send_data import send_data
import ctypes
import traceback
import os

class DragDetector:
    def __init__(self):
        self.dragging = False  # 是否正在拖动
        self.start_pos = None  # 记录起始位置
        self.threshold = 15    # 设定触发拖动的最小移动距离（像素）
        self.window_rect = self.get_game_window()  # 获取游戏窗口坐标

    def get_game_window(self):
        global ExchArea
        global AbsoArea
        # """获取《弈仙牌》窗口的位置"""
        

        hwnd = win32gui.FindWindow(None, "弈仙牌")
        if not hwnd:
            hwnd = win32gui.FindWindow(None, "Yi Xian: Cultivation Card Game")
        if not hwnd:
            hwnd = win32gui.FindWindow(None, "YiXianPai")
        if hwnd:
            foreground_hwnd = win32gui.GetForegroundWindow()
            if foreground_hwnd == hwnd:
                # win32gui.MoveWindow(hwnd, 100, 100, 800, 600, True)
                rect = win32gui.GetWindowRect(hwnd)# (left, top, right, bottom)
                ExchArea = [int(0.8*(rect[2] - rect[0]) + rect[0]), int(0.7*(rect[3] - rect[1]) + rect[1])]
                AbsoArea = [int(0.22*(rect[2] - rect[0]) + rect[0]), int(0.7*(rect[3] - rect[1]) + rect[1])]
                # print("在最顶端",str(rect),str(rect[2] - rect[0]),str(rect[3] - rect[1]))
                return rect  # (x1, y1, x2, y2)
        
        return None
        # win = None
        # for w in gw.getWindowsWithTitle("弈仙牌"):  # 找到游戏窗口（标题匹配）
        #     win = w
        #     break
        # if not win:
        #     for w in gw.getWindowsWithTitle("Yi Xian"):  # 找到游戏窗口（标题匹配）
        #         win = w
        #         break
        # print(str(win))
        # if win:
        #     ExchArea = [int(0.8*(win.right-win.left)+win.left), int(0.7*(win.bottom-win.top)+win.top)]
        #     AbsoArea = [int(0.22*(win.right-win.left)+win.left), int(0.7*(win.bottom-win.top)+win.top)]
        #     return (win.left, win.top, win.right, win.bottom)  # (x1, y1, x2, y2)
        # return None

    def is_in_window(self, x, y):
        # """检查鼠标是否在《弈仙牌》窗口内部"""
        if self.window_rect:
            x1, y1, x2, y2 = self.window_rect
            return x1 <= x <= x2 and y1 <= y <= y2
        return False

    def on_click(self, x, y, button, pressed):
        global ExchArea
        global AbsoArea
        self.window_rect = self.get_game_window()
        if not self.is_in_window(x, y):  # 如果鼠标不在窗口内，直接忽略
            return
        print("窗口内的输入")
        if button == mouse.Button.left:
            if pressed:
                self.start_pos = (x, y)  # 记录起始位置
                self.dragging = False
            else:
                if self.dragging:
                    end_pos=(x,y)
                    if end_pos[0]>ExchArea[0] and end_pos[1]>ExchArea[1]:
                        capture_yxp_window("exchange1",end_pos)
                    elif end_pos[0]<AbsoArea[0] and end_pos[1]>AbsoArea[1]:
                        capture_yxp_window("absorb2",end_pos)
                    else:
                        capture_upgrade(end_pos)

                self.dragging = False  # 释放鼠标，拖动结束
        elif button == mouse.Button.right:
            if pressed:
                self.start_pos = (x, y)  # 记录位置

            else:
                if self.start_pos is not None and self.start_pos[1]>ExchArea[1]:
                    capture_yxp_window("absorb1",self.start_pos)


    def on_move(self, x, y):
        if not self.is_in_window(x, y):  # 只在窗口内监听鼠标移动
            return
        if self.start_pos:
            dx = abs(x - self.start_pos[0])
            dy = abs(y - self.start_pos[1])
            if dx > self.threshold or dy > self.threshold:
                self.dragging = True


# 监听鼠标事件
def start_drag_detector():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        drag_detector = DragDetector()
        with mouse.Listener(on_click=drag_detector.on_click, on_move=drag_detector.on_move) as listener:
            listener.join()
    except Exception as e:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(dir_path,"py_error_log.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
# if __name__ == "__main__":
#     # 设置为感知 DPI 的进程，防止系统自动缩放窗口坐标
#     ctypes.windll.shcore.SetProcessDpiAwareness(2)
#     start_drag_detector()