from send_data import send_data
import shutil
import time
import os
from paddleocr import PaddleOCR 

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
det_dir=os.path.join(dir_path, 'Models/det')
rec_dir=os.path.join(dir_path, 'Models/rec')
cls_dir=os.path.join(dir_path, 'Models/cls')
if not os.path.exists(det_dir):
    os.makedirs(det_dir)
if not os.path.exists(rec_dir):
    os.makedirs(rec_dir)
if not os.path.exists(cls_dir):
    os.makedirs(cls_dir)
ocr = PaddleOCR(
    use_angle_cls=True, 
    det_model_dir=det_dir, 
    rec_model_dir=rec_dir, 
    cls_model_dir=cls_dir, 
    lang="ch"
)  # need to run only once to download and load model into memory

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

def Upgrade_OCR(img_path):
    card_name=[]
    result = ocr.ocr(img_path, cls=True)
    # print(result)
    for idx in range(len(result)):
        res = result[idx]
        if res:
            for line in res:
                EdgeRatio=((float(line[0][1][0])-float(line[0][0][0]))**2+(float(line[0][1][1])-float(line[0][0][1]))**2)**0.5/((float(line[0][1][0])-float(line[0][2][0]))**2+(float(line[0][1][1])-float(line[0][2][1]))**2)**0.5
                BoxAngle=(float(line[0][1][0])-float(line[0][2][0]))/(float(line[0][1][1])-float(line[0][2][1]))
                height = float(line[0][1][0])-float(line[0][0][0])
                if EdgeRatio>1.8 and abs(BoxAngle)<=0.1:
                    # print(EdgeRatio, BoxAngle)
                    card_name.append(line[1][0])
    # # 显示结果
    # if res:
    #     result = result[0]
    #     image = Image.open(img_path).convert('RGB')
    #     boxes = [line[0] for line in result]
    #     txts = [line[1][0] for line in result]
    #     scores = [line[1][1] for line in result]
    #     im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    #     im_show = Image.fromarray(im_show)
    #     im_show.save('C:/Users/TeraEnemy/Desktop/RESULT.png')
    if card_name != []:
        return card_name[0]
    else:
        return "NotFound"


# print(Upgrade_OCR("C:/YiXianMemo/PyFiles/Pictures/backup/up_8_NotFound.png"))

def Card_Name_OCR(img_path):
    card_list = []
    full_list = []
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        if res:
            for line in res:
                EdgeRatio=((float(line[0][1][0])-float(line[0][0][0]))**2+(float(line[0][1][1])-float(line[0][0][1]))**2)**0.5/((float(line[0][1][0])-float(line[0][2][0]))**2+(float(line[0][1][1])-float(line[0][2][1]))**2)**0.5
                BoxAngle=(float(line[0][1][0])-float(line[0][2][0]))/(float(line[0][1][1])-float(line[0][2][1]))
                HoriPos = float(line[0][0][0])
                VertPos = float(line[0][0][1])
                # print(EdgeRatio)
                full_list.append([line[1][0], EdgeRatio, HoriPos, VertPos])
                if EdgeRatio<0.6 and abs(BoxAngle)<=0.1:
                    card_list.append([line[1][0], EdgeRatio, HoriPos, VertPos])
    # print(result)
    # print(card_list)
    # # 显示结果
    # from PIL import Image
    # if res:
    #     result = result[0]
    #     image = Image.open(img_path).convert('RGB')
    #     boxes = [line[0] for line in result]
    #     txts = [line[1][0] for line in result]
    #     scores = [line[1][1] for line in result]
    #     im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    #     im_show = Image.fromarray(im_show)
    #     im_show.save('C:/Users/TeraEnemy/Desktop/RESULT.png')

    if result == [None]:
        return "NotFound"
    elif card_list == [] and len(result[0]) == 2:
        if abs(full_list[0][2] - full_list[1][2]) < 3 and abs(full_list[0][3] - full_list[1][3]) < 30:
            cardname = str(full_list[0][0]) + str(full_list[1][0])
            if cardname != "":
                return cardname
        else:
            return "NotFound"
    elif len(card_list) == 1:
        if card_list[0][0] != "":
            return card_list[0][0]
    elif len(card_list) > 1:
        rightside_card = "NotFound"
        rightside_card_pos = 0
        for  idx in range(len(card_list)):
            if card_list[idx][2] > rightside_card_pos:
                rightside_card_pos = card_list[idx][2]
                rightside_card = card_list[idx][0]
        if rightside_card != "":
            return rightside_card
    else:
        return "NotFound"

# print(Card_Name_OCR("C:/YiXianMemo/PyFiles/Pictures/backup/up_24_巽卦.png"))