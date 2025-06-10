import win32clipboard as clip
import win32api
import win32con
import win32gui
import win32com.client
import pynput
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
import time

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
        text_det_unclip_ratio=1.2,
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
        text_det_unclip_ratio=1.2,
        device='CPU',
    ) 

def main():
    rect = get_window()
    if rect != None:
        move_mouse_to(0,0)
        # game_round = get_round(rect)
        # cultivation_1,cultivation_limit_1 = get_cultivation(rect)
        # health_1 = get_health(rect)
        # physique_1,physique_limit_1= get_physique(rect)
        # cards_1 = get_cards(rect)
        talents_1,swordplay_talent_cards,five_elements_pure_vase_cards = get_talents(rect)
        print("rect:",rect,"width:",rect[2] - rect[0], "height:",rect[3] - rect[1])
        # print("round:",game_round)
        # print("cultivation_1:",cultivation_1)
        # print("cultivation_limit_1:",cultivation_limit_1)
        # print("health_1:",health_1)
        # print("physique_1:",physique_1)
        # print("physique_limit_1:",physique_limit_1)
        # print("cards_1:",cards_1)
        print("talents_1",talents_1,"\nswordplay_talent_cards:",swordplay_talent_cards,"\nfive_elements_pure_vase_cards:",five_elements_pure_vase_cards)

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
    upper = numpy.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    img = 255-img

    # #保存图片
    # cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/round.png", img)
    
    result_lst = ocr.predict(img)
    try:
        text = result_lst[0]['rec_texts'][0]
        game_round = "".join(re.findall(r'\d', text))
    except:
        game_round = ""

    # #保存图片
    # for res in result_lst:
    #     res.print()
    #     res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/round/")

    return game_round

def get_cultivation(rect):
    Width = rect[2] - rect[0]
    Top = int((rect[1] + rect[3])/2 - 0.195*Width) #中心锚点的控件位置
    Left = int(rect[0] + 0.065*Width)
    Height = int(0.05*Width)
    Width = int(0.06*Width)

    img = capture(Top, Left, Width, Height)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = numpy.array([0, 0, 120])
    upper = numpy.array([179, 30, 255])
    mask = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    img = 255-img

    # #保存图片
    # cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/cult.png", img)

    result_lst = ocr.predict(img)
    try:
        text = result_lst[0]['rec_texts'][0]
        if "/" in text:
            cult = text.split("/")[0]
            cult = "".join(re.findall(r'\d', cult))
            limit = text.split("/")[1]
            limit = "".join(re.findall(r'\d', limit))
        else:
            cult = "".join(re.findall(r'\d', text))
            try:
                limit = result_lst[0]['rec_texts'][1]
                limit = "".join(re.findall(r'\d', limit))
            except:
                limit = ""
    except:
        cult = ""
        limit = ""
    
    # #保存图片
    # for res in result_lst:
    #     res.print()
    #     res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/cult/")
    
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

    # #保存图片
    # cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/health.png", img)

    result_lst = ocr.predict(img)
    try:
        health = result_lst[0]['rec_texts'][0]
    except:
        health = ""

    # #保存图片
    # for res in result_lst:
    #     res.print()
    #     res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/health/")

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

    # #保存图片
    # cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/physique.png", img)

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

    # #保存图片
    # for res in result_lst:
    #     res.print()
    #     res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/physique/")

    return physi,limit

def get_cards(rect):
    cards = get_board(rect) + get_in_hand(rect)
    return cards

def get_board(rect):
    Width = rect[2] - rect[0]
    Top = int((rect[1] + rect[3])/2 - 0.13*Width) #中心锚点的控件位置
    Left = int(rect[0] + 0.02*Width)
    distance = int(0.1205*Width)
    Height = int(0.09*Width)
    Width = int(0.05*Width)

    cards = []
    for i in range(8):

        img = capture(Top, Left, Width, Height)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = numpy.array([0, 0, 0])
        upper = numpy.array([0, 0, 255])
        mask = cv2.inRange(hsv, lower, upper)
        img = cv2.bitwise_and(img, img, mask=mask)
        img = 255-img
        img_height = img.shape[0]

        # #保存图片
        # cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/" + str(i) + "board.png", img)

        card = ""
        result_lst = ocr.predict(img)
        card = join_OCR_result(result_lst, img_height)

        # #保存图片
        # for res in result_lst:
        #     res.print()
        #     res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/board" + str(i) + "/")

        cards.append(card)
        
        Left = Left + distance
    return cards

def get_in_hand(rect):
    cards = []
    return cards

def get_talents(rect):
    Window_Width = rect[2] - rect[0]
    pos = [[rect[0] + 0.135*Window_Width,rect[3] - 0.025*Window_Width],
    [rect[0] + 0.088*Window_Width,rect[3] - 0.037*Window_Width],
    [rect[0] + 0.044*Window_Width,rect[3] - 0.071*Window_Width],
    [rect[0] + 0.042*Window_Width,rect[3] - 0.123*Window_Width],
    [rect[0] + 0.0670*Window_Width,rect[3] - 0.173*Window_Width]
    ]
    talents = []
    swordplay_talent_cards = []
    five_elements_pure_vase_cards = []

    Tops = [
        int(rect[3] - 0.18*Window_Width),
        int(rect[3] - 0.12*Window_Width),
        int(rect[3] - 0.15*Window_Width),
        int(rect[3] - 0.18*Window_Width),
        int(rect[3] - 0.25*Window_Width)
        ]#底部锚点的控件位置
    Heights = [
        int(0.18*Window_Width),
        int(0.10*Window_Width),
        int(0.10*Window_Width),
        int(0.10*Window_Width),
        int(0.10*Window_Width),
        ]
    for i in range(5):
        move_mouse_to(pos[i][0], pos[i][1]) 
        Left = int(pos[i][0]+ 0.04*Window_Width)
        Width = int(0.22*Window_Width)

        time.sleep(0.2)

        img = capture(Tops[i],Left,Width,Heights[i])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = numpy.array([25, 150, 0])
        upper = numpy.array([35, 195, 255])
        mask = cv2.inRange(hsv, lower, upper)
        img_talents = cv2.bitwise_and(img, img, mask=mask)
        # img = 255-img

        #保存图片
        cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/" + str(i) + "talent.png", img_talents)
        cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/" + str(i) + "description.png", img)

        result_lst = ocr.predict(img_talents)
        try:
            talent = result_lst[0]['rec_texts'][0]
            talent = extract_chinese(talent)
        except:
            talent = ""
        if talent != "":
            talents.append(talent)

        # #保存图片
        # for res in result_lst:
        #     res.print()
        #     res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/talents" + str(i) + "/")

        if talent == "悟剑天赋":
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hue = [100,136,16]
            
            for i in range(3):
                lower = numpy.array([hue[i] - 5, 120, 0])
                upper = numpy.array([hue[i] + 5, 160, 255])
                mask = cv2.inRange(hsv, lower, upper)
                img_swordplay = cv2.bitwise_and(img, img, mask=mask)
                #保存图片
                cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/" + str(i) + "img_swordplay.png", img_swordplay)

                result_lst = ocr.predict(img_swordplay)
                try:
                    swordplay_talent_card = result_lst[0]['rec_texts'][0]
                    swordplay_talent_card = extract_chinese(swordplay_talent_card)
                    swordplay_talent_cards.append(swordplay_talent_card)
                    try:
                        swordplay_talent_card = result_lst[0]['rec_texts'][1]
                        swordplay_talent_card = extract_chinese(swordplay_talent_card)
                        swordplay_talent_cards.append(swordplay_talent_card)
                    except:
                        swordplay_talent_card = ""
                except:
                    swordplay_talent_card = ""

                #保存图片
                for res in result_lst:
                    res.print()
                    res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/img_swordplay" + str(i) + "/")
            
        if talent == "五行玉瓶":
            keyboard = pynput.keyboard.Controller()
            keyboard.press("q")
            keyboard.release('q')
            time.sleep(0.5)

            Top = int((rect[1] + rect[3])/2 - 0.118*Window_Width) #中心锚点的控件位置
            Left = int(rect[0] + 0.52*Window_Width)
            distance = int(0.15*Window_Width)
            Height = int(0.1*Window_Width)
            Width = int(0.05*Window_Width)

            for i in range(3):
                img = capture(Top, Left, Width, Height)
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower = numpy.array([0, 0, 0])
                upper = numpy.array([0, 0, 255])
                mask = cv2.inRange(hsv, lower, upper)
                img = cv2.bitwise_and(img, img, mask=mask)
                img = 255-img
                img_height = img.shape[0]

                # #保存图片
                # cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/yisim/" + str(i) + "5e_vase.png", img)

                card = ""
                result_lst = ocr.predict(img)
                card = join_OCR_result(result_lst, img_height)
                
                # #保存图片
                # for res in result_lst:
                #     res.print()
                #     res.save_to_img("C:/YiXianMemo/PyFiles/pictures/yisim/5e_vase" + str(i) + "/")
                if card != "":
                    five_elements_pure_vase_cards.append(card)

                Left = Left + distance
            keyboard.press("q")
            keyboard.release('q')


    return talents,swordplay_talent_cards,five_elements_pure_vase_cards

def get_plant_effectS():
    pass

def join_OCR_result(result_list, height):
    plural_list = []
    single_list = []
    texts = result_list[0]['rec_texts']
    boxes = result_list[0]['rec_boxes']
    for idx in range(len(texts)):
        text = texts[idx]
        # print(text)
        if text:
            EdgeRatio=float((boxes[idx][2]-boxes[idx][0])/(boxes[idx][3]-boxes[idx][1]))
            x1 = boxes[idx][0]
            y1 = boxes[idx][1]
            x2 = boxes[idx][2]
            y2 = boxes[idx][3]
            if EdgeRatio<=0.65:
                plural_list.append([text, EdgeRatio, x1, y1, x2, y2])
            elif EdgeRatio > 0.65 and EdgeRatio < 1.2:
                single_list.append([text, EdgeRatio, x1, y1, x2, y2])

    # print(result_list)
    # cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/backup/res_output.png", res)
    # print(plural_list)
    # print(single_list)

    if len(plural_list) == 1:
        if len(single_list) == 0:
            return extract_chinese(plural_list[0][0])
        elif len(single_list) > 0:
            offset = ((plural_list[0][3] + plural_list[0][5]) / 2 - height / 2) / height
            # print("offset:", offset)
            if offset > -0.08 and offset < 0.08:
                return extract_chinese(plural_list[0][0])
            else:
                for idx in range(len(single_list)):
                    if abs(single_list[idx][2] - plural_list[0][2]) < 0.04 * height:
                        if offset < -0.07:
                            card_name = plural_list[0][0] + single_list[idx][0]
                        else:
                            card_name = single_list[idx][0] + plural_list[0][0]
                        return extract_chinese(card_name)
                return extract_chinese(plural_list[0][0])
            
    elif len(plural_list) == 2:
        if abs(plural_list[0][2]-plural_list[1][2]) < 0.04 * height:
            card_name = plural_list[0][0] + plural_list[1][0]
            return extract_chinese(card_name)
        elif plural_list[0][2] > plural_list[1][2]:
            index = 0
        else:
            index = 1
        offset = ((plural_list[index][3] + plural_list[index][5]) / 2 - height / 2) / height
        print("offset:", offset)
        if offset > -0.08 and offset < 0.08:
            return extract_chinese(plural_list[index][0])
        elif len(single_list) == 0:
            return extract_chinese(plural_list[index][0])
        else:
            for idx in range(len(single_list)):
                if abs(single_list[idx][2] - plural_list[index][2]) < 0.04 * height:
                    if offset < -0.07:
                        card_name = plural_list[index][0] + single_list[idx][0]
                    else:
                        card_name = single_list[idx][0] + plural_list[index][0]
                    return extract_chinese(card_name)
            return extract_chinese(plural_list[index][0])
                
    elif len(plural_list) == 0:
        if len(single_list) < 2:
            return ""
        elif len(single_list) == 2:     
            if abs(single_list[0][2] - single_list[1][2]) < 0.04 * height:
                cardname = str(single_list[0][0]) + str(single_list[1][0])
                return extract_chinese(cardname)
            else:
                return ""
        elif len(single_list) > 2:
            return ""
        else:
            return ""
    else:
        return ""

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
    # mouse.move(-1000, -50)

def extract_chinese(text):
    # 匹配所有汉字范围
    chinese_only = re.findall(r'[\u4e00-\u9fff]+', text)
    return ''.join(chinese_only)
main()