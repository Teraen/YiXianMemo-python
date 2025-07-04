import time                                              # 延时控制
import sys                                               # 命令行参数处理
import os
from send_data import send_data
import traceback

dir_path = os.path.dirname(os.path.abspath(__file__))
python_path = os.path.join(dir_path, 'python.exe')
log_path = os.path.join(dir_path,"py_error_log.txt")

if __name__ == "__main__":
    runningtype = "0"  # Main.py 运行类型 
    from Main import Main

    def main():
        global runningtype
        # 处理命令行参数（允许自定义Main.py运行状态）
        if len(sys.argv) > 1:
            runningtype = sys.argv[1]

            #循环执行
        while True:
            #OCR的回传数据获取和拖动、识别监听启动
            Data = Main(runningtype)
            runningtype = "1" 
            if Data != "":
                send_data(Data)
            time.sleep(1)  # 降低 CPU 占用
    try:
        main()
    except Exception as e:
        with open(log_path, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)