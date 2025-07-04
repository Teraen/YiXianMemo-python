import win32gui
import win32con
import win32api
from pynput import mouse
import ctypes
import time
from send_data import send_data


ctypes.windll.shcore.SetProcessDpiAwareness(2)
def bring_window_to_front(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

def get_window():
    hwnd = win32gui.FindWindow(None, "弈仙牌")
    if not hwnd:
        hwnd = win32gui.FindWindow(None, "Yi Xian: Cultivation Card Game")
    if hwnd:
        # bring_window_to_front(hwnd)
        rect = win32gui.GetWindowRect(hwnd)  # (left, top, right, bottom)
        screen_width = win32api.GetSystemMetrics(0)
        if screen_width != rect[2] - rect[0]:
            rect = [rect[0] + 12, rect[1] + 52, rect[2] - 12, rect[3] - 12]#去掉边框
        return hwnd, rect
    return None, [0,0,0,0]

# 获取窗口信息
hwnd, rect = get_window()
if not hwnd:
    print("未找到弈仙牌窗口")
    exit()
left, top, right, bottom = rect
width = right - left
height = bottom - top

start_pos = []
log = {}

option = [
            [int(0.324*width+left), int(0.140*width+top+0.5*height), int(0.145*width), int(0.043*width)],
            [int(0.123*width+left), int(-0.155*width+top+0.5*height), int(0.18*width), int(0.28*width)],
            [int(0.315*width+left), int(-0.155*width+top+0.5*height), int(0.18*width), int(0.28*width)],
            [int(0.507*width+left), int(-0.155*width+top+0.5*height), int(0.18*width), int(0.28*width)],
            [int(0.699*width+left), int(-0.155*width+top+0.5*height), int(0.18*width), int(0.28*width)]
          ]

def is_inside_window(x, y):
    return left <= x <= right and top <= y <= bottom

def is_window_foreground(hwnd):
    return hwnd == win32gui.GetForegroundWindow()

def on_click(x, y, button, pressed):
    global start_pos
    if not is_inside_window(x, y) or not is_window_foreground(hwnd):
        return

    if pressed:
        start_pos = (x, y)
    else:
        if start_pos:
            for i in range(5):
                if option[i][0] < start_pos[0] < option[i][0] + option[i][2] and option[i][1] < start_pos[1] < option[i][1] + option[i][3]:
                    if i != 0:
                        log["option"] = i #1,2,3,4
                        log["choose_time"] = time.time()
                    elif "choose_time" in log.keys():
                        if log["choose_time"] + 30 > time.time():
                            log["verify_time"] = time.time()
                            del log["choose_time"]
                            send_data(log)
                            del log["verify_time"]
                    break




with mouse.Listener(on_click=on_click) as listener:
    listener.join()