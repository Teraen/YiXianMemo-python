from paddleocr import PaddleOCR, draw_ocr

def Card_Name_OCR(img_path):
    # img_path="C:/Users/TeraEnemy/Pictures/absorb/11.png"
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    card_name=[]
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        if res:
            for line in res:
                EdgeRatio=((float(line[0][1][0])-float(line[0][0][0]))**2+(float(line[0][1][1])-float(line[0][0][1]))**2)**0.5/((float(line[0][1][0])-float(line[0][2][0]))**2+(float(line[0][1][1])-float(line[0][2][1]))**2)**0.5
                BoxAngle=(float(line[0][1][0])-float(line[0][2][0]))/(float(line[0][1][1])-float(line[0][2][1]))
                if EdgeRatio<0.6 and abs(BoxAngle)<=0.1:
                    card_name.append(line[1][0])
    # print(result)
    return card_name[0]
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

# print(Card_Name_OCR("C:/Users/TeraEnemy/Pictures/absorb/12.png"))
