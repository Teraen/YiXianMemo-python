import win32gui
import mss
import os

i=0
pictures_path = os.path.join(os.environ['USERPROFILE'], 'Pictures')
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
    if capture_mode == "exchange1":
        left = int(-0.055 * width + end_pos[0])
        top = int(-0.16 * height + end_pos[1])
        width, height = int(0.11 * width), int(0.32 * height)
    elif capture_mode == "absorb2":
        left = int(-0.055 * width + end_pos[0])
        top = int(-0.16 * height + end_pos[1])
        width, height = int(0.11 * width), int(0.32 * height)
    elif capture_mode == "absorb1":
        left = int(-0.08 * width + end_pos[0])
        top = int(-0.20 * height + end_pos[1])
        width, height = int(0.12 * width), int(0.34 * height)


    with mss.mss() as sct:
        save_dir1 = pictures_path + "/exchange/"
        save_dir2 = pictures_path + "/absorb/"
        backup_dir = pictures_path + "/backup/"
        if not os.path.exists(save_dir1):
            os.makedirs(save_dir1)
        if not os.path.exists(save_dir2):
            os.makedirs(save_dir2)        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)        
        screenshot = sct.grab({"top": top, "left": left, "width": width, "height": height})
        if capture_mode == "exchange1":
            save_path = save_dir1+ str(i) +".png"
        elif capture_mode == "absorb2" or capture_mode == "absorb1":
            save_path = save_dir2+ str(i) +".png"

        i=i+1
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path) #保存本地图片
        # mss.tools.to_png(screenshot.rgb, screenshot.size, output=backup_dir + str(i) + ".png") #保存本地图片



