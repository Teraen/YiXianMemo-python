from OCR_xcg import Card_Name_OCR
from OCR_upgrade import Upgrade_OCR
from send_data import send_data
import shutil
import time
import os

upgraded_card = "None"
m = 0
n = 0
# pictures_path = os.path.join(os.environ['USERPROFILE'], 'Pictures/YiXianMemo')
dir_path = os.path.dirname(os.path.abspath(__file__))
pictures_path = os.path.join(dir_path, 'Pictures')
backup_dir = pictures_path + "/backup/"
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
    os.makedirs(backup_dir)
else:
    os.makedirs(backup_dir)

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
            try:
                # 调用OCR模块识别图片
                ocr_result = Card_Name_OCR(file_path)
                result.append(ocr_result)
                send_data(ocr_result)
                # OCR成功后删除图片
                if ocr_result == "NotFound":
                    shutil.copy(file_path, backup_dir + str(m) + ocr_result + ".png")
                else:
                    shutil.copy(file_path, backup_dir + ocr_result + ".png")
                os.remove(file_path)
                
            except Exception as e:
                shutil.copy(file_path, backup_dir + str(m) + ocr_result + ".png")
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

