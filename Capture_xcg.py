import win32gui
import mss
import mss.tools
import os
import threading
i=0
# pictures_path = os.path.join(os.environ['USERPROFILE'], 'Pictures/YiXianMemo')
dir_path = os.path.dirname(os.path.abspath(__file__))
pictures_path = os.path.join(dir_path, 'Pictures')
def capture_yxp_window(capture_mode, end_pos):
    global i
    """截图《弈仙牌》窗口区域"""
    hwnd = win32gui.FindWindow(None, "弈仙牌")
    if not hwnd:
        hwnd = win32gui.FindWindow(None, "Yi Xian: Cultivation Card Game")

    if hwnd != win32gui.GetForegroundWindow():
        return

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width, height = right - left, bottom - top
    if capture_mode == "exchange1" or capture_mode == "absorb2" or capture_mode == "upgrade1":
        left = int(-0.07 * width + end_pos[0])
        top = int(-0.13 * height + end_pos[1])
        width, height = int(0.05 * width), int(0.17 * height)
    elif capture_mode == "absorb1":
        left = int(-0.11*width + end_pos[0])
        top = int(0.65 * height + top)
        width, height = int(0.13 * width), int(0.17 * height)
    elif capture_mode == "upgrade2":
        left = int(-0.07 * width + end_pos[0])
        top = int(-0.07 * height + end_pos[1])
        width, height = int(0.14 * width), int(0.10 * height)

    with mss.mss() as sct:
        exchange_dir = pictures_path + "/exchange/"
        absorb_dir = pictures_path + "/absorb/"
        upgrade_dir = pictures_path + "/upgrade/"
        backup_dir = pictures_path + "/backup/"
        if not os.path.exists(exchange_dir):
            os.makedirs(exchange_dir)
        if not os.path.exists(absorb_dir):
            os.makedirs(absorb_dir)        
        if not os.path.exists(upgrade_dir):
            os.makedirs(upgrade_dir) 
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)        
        screenshot = sct.grab({"top": top, "left": left, "width": width, "height": height})
        if capture_mode == "exchange1":
            save_path = exchange_dir+ str(i) +".png"
        elif capture_mode == "absorb1" or capture_mode == "absorb2":
            save_path = absorb_dir+ str(i) +".png"
        else:
            save_path = upgrade_dir+ str(i) +".png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path) #Save image
        # mss.tools.to_png(screenshot.rgb, screenshot.size, output=backup_dir + str(i) + ".png") #save image for debug 
        i=i+1

def capture_upgrade(end_pos):
    capture_yxp_window("upgrade1", end_pos)
    timer = threading.Timer(0.15, lambda: capture_yxp_window("upgrade2", end_pos))
    timer.start()




