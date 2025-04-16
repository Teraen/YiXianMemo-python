from paddleocr import PaddleOCR, draw_ocr

def Card_Name_OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
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
                full_list.append([line[1][0], EdgeRatio, HoriPos, VertPos])
                if EdgeRatio<0.6 and abs(BoxAngle)<=0.1:
                    card_list.append([line[1][0], EdgeRatio, HoriPos, VertPos])
    # print(result)
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

# print(Card_Name_OCR("C:/YiXianMemo/PyFiles/Pictures/backup/up_12_NotFound.png"))