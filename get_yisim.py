import win32clipboard as clip
import win32api
import win32con
import win32gui
import win32com.client
from pynput.mouse import Controller
from paddleocr import PaddleOCR
import numpy
import mss
import mss.tools
import os
import shutil
import ctypes
import cv2
import re
from send_data import send_data

ctypes.windll.shcore.SetProcessDpiAwareness(2)

dir_path = os.path.dirname(os.path.abspath(__file__))
yisim_path = os.path.join(dir_path,"Pictures/yisim/")
if os.path.exists(yisim_path):
    shutil.rmtree(yisim_path)
os.makedirs(yisim_path)
det_dir=os.path.join(dir_path, 'Models/det')
rec_dir=os.path.join(dir_path, 'Models/rec')
ori_dir=os.path.join(dir_path, 'Models/ori')
try:
    ocr = PaddleOCR(
        use_doc_orientation_classify=False, 
        use_doc_unwarping=False, 
        use_textline_orientation=False,
        text_detection_model_dir=det_dir,
        # text_detection_model_name='PP-OCRv5_server_det',
        text_detection_model_name='PP-OCRv5_mobile_det',
        text_line_orientation_model_dir=ori_dir,
        text_recognition_model_dir=rec_dir,
        text_rec_score_thresh=0.7,
        text_det_box_thresh=0.3,
        text_det_thresh=0.3,
        text_det_unclip_ratio=1.0,
        device='CPU',
    ) 
except:
    ocr = PaddleOCR(
        use_doc_orientation_classify=False, 
        use_doc_unwarping=False, 
        use_textline_orientation=False,
        text_detection_model_dir=det_dir,
        text_detection_model_name='PP-OCRv5_server_det',
        # text_detection_model_name='PP-OCRv5_mobile_det',
        text_line_orientation_model_dir=ori_dir,
        text_recognition_model_dir=rec_dir,
        text_rec_score_thresh=0.7,
        text_det_box_thresh=0.3,
        text_det_thresh=0.3,
        text_det_unclip_ratio=1.0,
        device='CPU',
    ) 

def main():
    rect = get_window()
    if rect != None:
        game_round_1 = get_round(rect)
        cultivation_1,cultivation_limit_1 = get_cultivation(rect)
        health_1 = get_health(rect)
        physique_1,physique_limit_1= get_physique(rect)
        print("rect:",rect,"width:",rect[2] - rect[0], "height:",rect[3] - rect[1])
        print("round:",game_round_1)
        print("cultivation:",cultivation_1)
        print("cultivation_limit_1:",cultivation_limit_1)
        print("health:",health_1)
        print("physique:",physique_1)
        print("physique_limit_1:",physique_limit_1)


def get_window():
    hwnd = win32gui.FindWindow(None, "弈仙牌")
    if not hwnd:
        hwnd = win32gui.FindWindow(None, "Yi Xian: Cultivation Card Game")
    if hwnd:
        bring_window_to_front(hwnd)
        rect = win32gui.GetWindowRect(hwnd)# (left, top, right, bottom)
        screen_width = win32api.GetSystemMetrics(0)

        if screen_width != rect[2] - rect[0]:
            rect = [rect[0] + 11, rect[1] + 45, rect[2] - 11, rect[3] - 11]#去掉边框
        return rect
    return None

def bring_window_to_front(hwnd):
    # 如果窗口最小化了，就恢复它
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # 强制窗口置顶（临时），然后取消置顶
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_NOTOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )

    # 设置前台窗口
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')  # 发送一个 ALT 键用于打破前台锁定（有些系统限制切换）
    win32gui.SetForegroundWindow(hwnd)

def mode_check(rect):
    Width = int(0.15*(rect[2] - rect[0]))
    Height = int(0.15*(rect[3] - rect[1]))
    Top = int(rect[3] - 1.8*Height)
    Left = int(rect[2] - 1.2*Width)
    img = capture(Top, Left, Width, Height)

    # height, width, channels = img.shape
    # # print(0.04 * height)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = numpy.array([20, 20, 0])
    upper = numpy.array([35, 60, 255])
    mask = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    
    result_lst = ocr.predict(img)
    for res in result_lst:
        res.print()
        res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/")
    cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/res_cv_output.png", img)

def get_round(rect):
    Width = rect[2] - rect[0]
    Top = int((rect[1] + rect[3])/2 - 0.28*Width) #中心锚点的控件位置
    Left = int(rect[2] - 0.12*Width)
    Height = int(0.05*Width)
    Width = int(0.1*Width)

    img = capture(Top, Left, Width, Height)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = numpy.array([0, 0, 115])
    upper = numpy.array([179, 30, 255])
    mask = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    img = 255-img

    cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/round.png", img)
    
    result_lst = ocr.predict(img)
    try:
        text = result_lst[0]['rec_texts'][0]
        game_round = "".join(re.findall(r'\d', text))
    except:
        game_round = ""

    for res in result_lst:
        res.print()
        res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/round/")

    return game_round

def get_cultivation(rect):
    Width = rect[2] - rect[0]
    Top = int((rect[1] + rect[3])/2 - 0.19*Width) #中心锚点的控件位置
    Left = int(rect[0] + 0.065*Width)
    Height = int(0.04*Width)
    Width = int(0.06*Width)

    img = capture(Top, Left, Width, Height)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = numpy.array([0, 0, 120])
    upper = numpy.array([179, 30, 255])
    mask = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    img = 255-img
    cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/cult.png", img)

    result_lst = ocr.predict(img)
    try:
        text = result_lst[0]['rec_texts'][0]
        if "/" in text:
            cult = text.split("/")[0]
            limit = text.split("/")[1]
        else:
            cult = text
            try:
                limit = result_lst[0]['rec_texts'][1]
            except:
                limit = ""
    except:
        cult = ""
        limit = ""
    
    for res in result_lst:
        res.print()
        res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/cult/")
    
    return cult,limit

def get_health(rect):
    Width = rect[2] - rect[0]
    Top = int((rect[1] + rect[3])/2 - 0.19*Width) #中心锚点的控件位置
    Left = int(rect[0] + 0.175*Width)
    Height = int(0.04*Width)
    Width = int(0.06*Width)

    img = capture(Top, Left, Width, Height)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = numpy.array([0, 0, 120])
    upper = numpy.array([179, 30, 255])
    mask = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    img = 255-img
    cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/health.png", img)

    result_lst = ocr.predict(img)
    try:
        health = result_lst[0]['rec_texts'][0]
    except:
        health = ""

    for res in result_lst:
        res.print()
        res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/health/")
    return health

def get_physique(rect):
    Width = rect[2] - rect[0]
    Top = int((rect[1] + rect[3])/2 - 0.19*Width) #中心锚点的控件位置
    Left = int(rect[0] + 0.28*Width)
    Height = int(0.04*Width)
    Width = int(0.06*Width)

    img = capture(Top, Left, Width, Height)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = numpy.array([0, 0, 120])
    upper = numpy.array([179,30, 255])
    mask = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    img = 255-img
    cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/physique.png", img)

    result_lst = ocr.predict(img)
    try:
        text = result_lst[0]['rec_texts'][0]
        if "/" in text:
            physi = text.split("/")[0]
            limit = text.split("/")[1]
        else:
            physi = text
            try:
                limit = result_lst[0]['rec_texts'][1]
            except:
                limit = ""
    except:
        physi = ""
        limit = ""
    
    for res in result_lst:
        res.print()
        res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/physique/")
    return physi,limit

def get_board(game_round):
    pass

# def OCR_board():
#     pass

def get_in_hand():
    pass

# def OCR_in_hand():
#     pass

def get_talents():
    pass
    # return char,talents,param

# def OCR_talents():
#     pass

def get_plant_effectS():
    pass

def OCR():
    pass

def capture(top,left,width,height):
    with mss.mss() as sct:    
        screenshot = sct.grab({"top": top, "left": left, "width": width, "height": height})
        img = numpy.array(screenshot)
        img = img[:, :, :3] #[:, :, ::-1]
        # save_path = os.path.join(yisim_path,"Test.png")
        # mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)
    return img

def set_clipboard_text(text):
    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_UNICODETEXT, text)
    clip.CloseClipboard()


def move_mouse_to(x,y):
    mouse = Controller()
    # 设置鼠标绝对位置
    mouse.position = (x, y)
    # 相对移动鼠标
    # mouse.move(100, -50)

main()