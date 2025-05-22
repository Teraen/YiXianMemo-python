from send_data import send_data
import shutil
import time
import os
from paddleocr import PaddleOCR
import cv2
import numpy as np
import re

upgraded_card = "None"
m = 0
n = 0
# pictures_path = os.path.join(os.environ['USERPROFILE'], 'Pictures/YiXianMemo')
dir_path = os.path.dirname(os.path.abspath(__file__))
pictures_path = os.path.join(dir_path, 'Pictures')
backup_dir = pictures_path + "/backup/"
det_dir=os.path.join(dir_path, 'Models/det')
rec_dir=os.path.join(dir_path, 'Models/rec')
ori_dir=os.path.join(dir_path, 'Models/ori')
if not os.path.exists(det_dir):
    os.makedirs(det_dir)
if not os.path.exists(rec_dir):
    os.makedirs(rec_dir)
if not os.path.exists(ori_dir):
    os.makedirs(ori_dir)
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


def img_process_loop(queue_exchange, queue_absorb):
    exchange_dir = pictures_path + "/exchange/"
    absorb_dir = pictures_path + "/absorb/"
    upgrade_dir = pictures_path + "/upgrade/"
    if not os.path.exists(exchange_dir):
        os.makedirs(exchange_dir)
    if not os.path.exists(absorb_dir):
        os.makedirs(absorb_dir) 
    if not os.path.exists(upgrade_dir):
        os.makedirs(upgrade_dir) 
    while True:
        #识别exchange图片
        result1=process_images_and_delete(exchange_dir)
        if result1:
            queue_exchange.put(result1)
        #识别absorb图片
        result2=process_images_and_delete(absorb_dir)
        if result2:
            queue_absorb.put(result2)
        # 识别upgrade图片
        result3=process_upgrade_and_delete(upgrade_dir)
        if result3:
            queue_absorb.put(result3)


        time.sleep(1)  # 控制识别频率


def process_images_and_delete(folder_path):
    global m
    # 支持的图片扩展名列表
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    result = []
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        # 检查是否为图片文件
        if os.path.isfile(file_path) and file_ext in image_extensions:
            ocr_result = "EXCEPT"
            try:
                # 调用OCR模块识别图片
                ocr_result = Card_Name_OCR(file_path)
                result.append(ocr_result)
                send_data(ocr_result)
                # OCR成功后删除图片
                if ocr_result == "NotFound":
                    shutil.copy(file_path, backup_dir + str(m) + ocr_result + ".png")
                else:
                    shutil.copy(file_path, backup_dir + str(ocr_result) + ".png")
                os.remove(file_path)
                
            except Exception as e:
                shutil.copy(file_path, backup_dir + str(m) + str(ocr_result) + ".png")
                os.remove(file_path)
                continue # 将结果放入队列中
        m += 1
    if result:
        return result

def process_upgrade_and_delete(folder_path):
    global upgraded_card
    global n
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    result = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        if os.path.isfile(file_path) and file_ext in image_extensions:
            if n%2 == 0:
                upgraded_card = Card_Name_OCR(file_path)
                if upgraded_card == None:
                    upgraded_card = "None"
                shutil.copy(file_path, backup_dir + "up_" + str(n) + "_" + upgraded_card + ".png")
                os.remove(file_path)
            else:
                is_upgrated = Upgrade_OCR(file_path)
                if "升级" in is_upgrated or "grade" in is_upgrated:
                    send_data(upgraded_card)
                    result.append(upgraded_card)
                shutil.copy(file_path, backup_dir + "up_" + str(n) + "_" + is_upgrated + ".png")
                os.remove(file_path)
                upgraded_card = "None"
        n += 1
    if result!=[]:
        return result

def Upgrade_OCR(img_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 红色范围（注意红色跨越HSV的头尾）
    lower_red1 = np.array([0, 200, 200])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 200, 200])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    red_pixel_count = np.sum(mask > 0)
    total_pixel_count = mask.size
    red_ratio = red_pixel_count / total_pixel_count

    # res = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imwrite("C:/YiXianMemo/PyFiles/pictures/res_output.png", res)
    # print("Red Ratio: ", red_ratio)
    
    if red_ratio>0.1:
        return "升级"
    else:
        return "NotFound"

# print(Upgrade_OCR("C:/YiXianMemo/PyFiles/Pictures/5.png"))


def Card_Name_OCR(img_path):
    plural_list = []
    single_list = []

    img = cv2.imread(img_path)
    height, width, channels = img.shape
    print(0.04 * height)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 0, 100])
    upper = np.array([0, 0, 255])

    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(img, img, mask=mask)
    result_list = ocr.predict(res)

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
            if EdgeRatio<0.6:
                plural_list.append([text, EdgeRatio, x1, y1, x2, y2])
            elif EdgeRatio > 0.6 and EdgeRatio < 1.05:
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
            print("offset:", offset)
            if offset > -0.07 and offset < 0.07:
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
        if offset > -0.07 and offset < 0.07:
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
            return "NotFound"
        elif len(single_list) == 2:     
            if abs(single_list[0][2] - single_list[1][2]) < 0.04 * height:
                cardname = str(single_list[0][0]) + str(single_list[1][0])
                return extract_chinese(cardname)
            else:
                return "NotFound"
        elif len(single_list) > 2:
            return "NotFound"
        else:
            return "NotFound"
    else:
        return "NotFound"


def extract_chinese(text):
    # 匹配所有汉字范围（包括简体和繁体）
    chinese_only = re.findall(r'[\u4e00-\u9fff]+', text)
    return ''.join(chinese_only)

# print(Card_Name_OCR("C:/YiXianMemo/PyFiles/Pictures/backup/0.png"))
