from OCR_xcg import Card_Name_OCR
from send_data import send_data

import re
import time
import os

pictures_path = os.path.join(os.environ['USERPROFILE'], 'Pictures')

def img_process_loop(queue_exchange, queue_absorb):
    folder_path1 = pictures_path + "/exchange/"
    folder_path2 = pictures_path + "/absorb/"
    if not os.path.exists(folder_path1):
        os.makedirs(folder_path1)
    if not os.path.exists(folder_path2):
        os.makedirs(folder_path2)   
    while True:
        rst1=process_images_and_delete(folder_path1)
        if rst1:
            queue_exchange.put(rst1)
        rst2=process_images_and_delete(folder_path2)
        if rst2:
            queue_absorb.put(rst2)
        time.sleep(1)  # 控制识别频率


def process_images_and_delete(folder_path):
    # 支持的图片扩展名列表
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    result = []
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        # 检查是否为图片文件
        if os.path.isfile(file_path) and file_ext in image_extensions:
            try:
                # 调用OCR模块识别图片
                ocr_result = Card_Name_OCR(file_path)
                ocr_result = remove_digits(ocr_result)
                result.append(ocr_result)
                send_data(ocr_result)
                # OCR成功后删除图片
                os.remove(file_path)
                
            except Exception as e:
                os.remove(file_path)
                continue # 将结果放入队列中
    if result:
        return result


def remove_digits(text):
    return re.sub(r'\d+', '', text)
