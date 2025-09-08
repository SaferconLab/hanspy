#!/usr/bin/env python3
"""
控制器服务器主程序
运行在控制机A上，接收来自上位机B的指令并控制机械臂和夹爪
"""

import sys
import os
import signal
import argparse
import json
import logging

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
    parser.add_argument('--config', '-c', default='config.json', 
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
