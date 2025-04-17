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

    def main():
        global runningtype
        # 处理命令行参数（允许自定义Main.py运行状态）
        if len(sys.argv) > 1:
            runningtype = sys.argv[1]
        # send_data(str(get_pid_by_name_win32("python.exe")) )
        while True:
            Data = Main(runningtype)
            runningtype = "1" 
            if Data != "":
                send_data(Data)
            time.sleep(1)  # 降低 CPU 占用

    REQUIRED_PACKAGES = ['paddlepaddle', 'paddleocr', 'pynput', 'mss', 'pygetwindow']  # 你用到的库，按需填

    def install_packages():
        for pkg in REQUIRED_PACKAGES:
            try:
                __import__(pkg)
            except ImportError:
                send_data("正在安装" + pkg + "...")
                subprocess.check_call([python_path, "-m", "pip", "install", pkg])
    send_data("正在校验Python依赖完整性...")
    install_packages()
    send_data("Python依赖校验完毕")

    from Main import Main

    main()
