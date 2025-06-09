from multiprocessing import Process, Queue
from img_process_loop import img_process_loop
from InputEvent_listener import start_drag_detector
from Match_card import Match
import os
import shutil
from send_data import send_data

result_dict = {}
queue_exchange = Queue(maxsize=20)
queue_absorb = Queue(maxsize=20)
is_running = False
processes = []
dir_path = os.path.dirname(os.path.abspath(__file__))
pictures_path = os.path.join(dir_path, 'Pictures')
backup_dir = pictures_path + "/backup/"


if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
os.makedirs(backup_dir)


# 置换卡清单
exchange_tag = ["练笔", "以画入道", "触类旁通", "妙笔生花", ]

def Main(runningtype):
    global processes, is_running
    result_dict = {}

    if runningtype == "0":
        # 启动所有子进程
        start_process()
        is_running = True
        # send_data("子进程已创建")

    if runningtype == "2":
        # 终止所有子进程
        for p in processes:
            p.terminate()
        processes.clear()  # 清空进程列表
        is_running = False
        send_data("所有子进程已终止")

    # get the result from queue_exchange and queue_draw

    while not queue_exchange.empty():
        result_ex = queue_exchange.get()
        i=0
        while i < len(result_ex):
            rs = Match(result_ex[i])
            if any(item in result_ex[i] for item in exchange_tag):
                if rs not in result_dict:
                    result_dict[rs] = -1
                else:
                    result_dict[rs] -= 1
            else:
                if rs not in result_dict:
                    result_dict[rs] = -3
                else:
                    result_dict[rs] -= 3
            i += 1
    while not queue_absorb.empty():
        result_dr = queue_absorb.get()
        i = 0
        while i < len(result_dr):
            rs = Match(result_dr[i])
            if rs not in result_dict:
                result_dict[rs] = -1
            else:
                result_dict[rs] -= 1
            i += 1
    
    if  result_dict == {}:
        result = ""
    else:
        result = str(result_dict)

    return result


def start_process():
    global processes
    process1 = Process(target=img_process_loop, args=(queue_exchange, queue_absorb))
    process2 = Process(target=start_drag_detector)
    processes = [process1, process2]
    process1.start()
    process2.start()
    send_data("识别模块已启动")