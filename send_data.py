import socket                                            # UDP 通信                                         

# 全局变量定义
opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建 UDP 套接字
UDP_IP = "127.0.0.1"                                              # UDP 目标 IP（本地回环）
UDP_PORT = 4243                                                   # UDP 目标端口

def send_data(Data):
    # 将内容通过 UDP 发送
    byte_message = bytes(Data, "utf-8")
    opened_socket.sendto(byte_message, (UDP_IP, UDP_PORT))