import time                                              # 延时控制
import sys                                               # 命令行参数处理
import os
import subprocess
from send_data import send_data

dir_path = os.path.dirname(os.path.abspath(__file__))
python_path = os.path.join(dir_path, 'python.exe')

if __name__ == "__main__":
    # 全局变量定义
    runningtype = "0"  # Main.py 运行类型 
    from Main import Main

    def main():
        global runningtype
        # 处理命令行参数（允许自定义Main.py运行状态）
        if len(sys.argv) > 1:
            runningtype = sys.argv[1]
        while True:
            Data = Main(runningtype)
            runningtype = "1" 
            if Data != "":
                send_data(Data)
            time.sleep(1)  # 降低 CPU 占用
    main()
