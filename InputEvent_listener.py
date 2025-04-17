import pygetwindow as gw
from pynput import mouse
from Capture_xcg import capture_yxp_window, capture_upgrade


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
        win = None
        for w in gw.getWindowsWithTitle("弈仙牌"):  # 找到游戏窗口（标题匹配）
            win = w
            break
        if not win:
            for w in gw.getWindowsWithTitle("Yi Xian"):  # 找到游戏窗口（标题匹配）
                win = w
                break
        if win:
            ExchArea = [int(0.8*(win.right-win.left)+win.left), int(0.7*(win.bottom-win.top)+win.top)]
            AbsoArea = [int(0.22*(win.right-win.left)+win.left), int(0.7*(win.bottom-win.top)+win.top)]
            return (win.left, win.top, win.right, win.bottom)  # (x1, y1, x2, y2)
        return None

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
                if self.start_pos[1]>ExchArea[1]:
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
    drag_detector = DragDetector()
    with mouse.Listener(on_click=drag_detector.on_click, on_move=drag_detector.on_move) as listener:
        listener.join()
if __name__ == "__main__":
    start_drag_detector()