#!/usr/bin/env python3
"""
控制器服务器主程序
运行在控制机A上，接收来自上位机B的指令并控制机械臂和夹爪,把相机采集的视频流传输给上位机B
"""

import sys
import os
import signal
import argparse
import json
import logging
import socket

# 添加项目根目录到Python路径，以便能够正确导入lib模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from server.tcp_server import ControllerServer


def load_config(config_path: str = "config.json") -> dict:
    """
    加载配置文件
    
    Args:
        config_path (str): 配置文件路径
        
    Returns:
        dict: 配置信息
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_local_ip():
    """
    获取本机局域网IP地址
    
    Returns:
        str: 局域网IP地址，如果获取失败则返回'127.0.0.1'
    """
    try:
        # 创建一个UDP连接来获取本地IP地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不实际发送数据，只是用来获取本地IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def signal_handler(sig, frame):
    """
    信号处理器，用于优雅关闭服务器
    """
    print('\n正在关闭控制器服务器...')
    if 'server' in globals():
        server.stop()
    print('服务器已关闭')
    sys.exit(0)


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='控制器服务器')
    parser.add_argument('--config', '-c', default='/home/pku/pyprojects/HansPy/controller_server/config.json', 
                       help='配置文件路径 (默认: config.json)')
    args = parser.parse_args()
    
    try:
        # 加载配置
        print("加载配置文件...")
        config = load_config(args.config)
        print("配置文件加载成功")
        
        # 创建服务器实例
        print("创建控制器服务器...")
        global server
        server = ControllerServer(config)
        print("控制器服务器创建成功")
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # 启动服务器
        print("启动控制器服务器...")
        server.start()
        print("控制器服务器已启动，等待客户端连接...")
        
        # 打印服务器访问信息
        try:
            local_ip = get_local_ip()
            server_port = config['server']['port']
            stream_port = config['webcam']['stream_port']
            print(f"\n=== 服务器访问信息 ===")
            print(f"服务器IP地址: {local_ip}")
            print(f"服务器端口: {server_port}")
            print(f"视频流端口: {stream_port}")
            print(f"视频流访问地址: http://{local_ip}:{stream_port}/stream")
            print("=====================\n")
        except Exception as e:
            print(f"获取服务器访问信息时出错: {e}")
        
        # 保持程序运行
        try:
            while True:
                signal.pause()  # 等待信号
        except KeyboardInterrupt:
            print("\n接收到中断信号")
            
    except Exception as e:
        print(f"程序运行时发生错误: {e}")
        logging.error(f"程序运行时发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
