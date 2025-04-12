import socket                                            # UDP 通信                                         
import time                                              # 延时控制
import sys                                               # 命令行参数处理

from Main import Main

if __name__ == "__main__":
    # 全局变量定义
    opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建 UDP 套接字
    runningtype = "0"  # Main.py 运行类型 
    UDP_IP = "127.0.0.1"                                              # UDP 目标 IP（本地回环）
    UDP_PORT = 4243                                                   # UDP 目标端口


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

    def send_data(Data):
        # 将内容通过 UDP 发送
        byte_message = bytes(Data, "utf-8")
        opened_socket.sendto(byte_message, (UDP_IP, UDP_PORT))

    main()
