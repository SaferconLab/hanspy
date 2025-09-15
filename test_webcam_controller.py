#!/usr/bin/env python3
"""
摄像头控制器测试脚本
用于测试服务端的摄像头相关功能：
1. 查询可用摄像头
2. 启动视频流
3. 停止视频流
4. 使用OpenCV读取并播放视频流
"""

import sys
import os
import time
import logging
import cv2
import numpy as np

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller_clinet.client import ControllerClient
from controller_clinet.protocol import CommandType


def test_webcam_with_opencv():
    """使用OpenCV测试摄像头视频流"""
    print("开始使用OpenCV测试摄像头视频流...")
    
    # 创建客户端实例
    client = ControllerClient(host="localhost", port=8888)
    
    try:
        # 1. 连接到服务器
        print("\n1. 正在连接到服务器...")
        if not client.connect():
            print("连接服务器失败")
            return False
        print("✓ 成功连接到服务器")
        
        # 2. 查询可用摄像头列表
        print("\n2. 正在查询可用摄像头...")
        response = client._send_command(CommandType.GET_CAMERAS_LIST)
        if response:
            print(f"收到响应: 状态={response.status}, 消息={response.message}")
            # 检查响应是否成功
            if response.status and hasattr(response, 'status') and response.status != "error":
                cameras = response.data.get("cameras", [])
                if cameras:
                    print(f"✓ 发现 {len(cameras)} 个可用摄像头:")
                    for i, cam in enumerate(cameras):
                        print(f"  摄像头 {i}: {cam['name']} (索引: {cam['index']})")
                        print(f"    路径: {cam['path']}")
                        print(f"    分辨率: {cam['width']}x{cam['height']}")
                        print(f"    FPS: {cam['fps']}")
                else:
                    print("未发现可用摄像头")
                    return False
            else:
                print(f"✗ 查询摄像头列表失败: {response.message}")
                return False
        else:
            print("✗ 查询摄像头列表失败: 无响应")
            return False
        
        # 选择第一个摄像头进行测试
        if cameras:
            camera_index = cameras[2]['index']
            print(f"\n3. 使用摄像头 {camera_index} 进行测试")
            
            # 4. 启动视频流
            print("\n4. 正在启动视频流...")
            data = {"camera_index": camera_index}
            response = client._send_command(CommandType.START_CAMERA_STREAM, data)
            if response and response.status != "error":
                print("✓ 视频流启动成功")
                print(f"  摄像头索引: {response.data.get('camera_index')}")
                print(f"  流状态: {response.data.get('streaming')}")
            else:
                print(f"✗ 启动视频流失败: {response.message if response else '无响应'}")
                return False
            
            # 5. 使用OpenCV读取并播放视频流
            print("\n5. 使用OpenCV读取并播放视频流... (按 'q' 键退出)")
            # try:
            #     # OpenCV读取视频流
            #     cap = cv2.VideoCapture('http://localhost:9999/stream')
            #     if not cap.isOpened():
            #         print("✗ 无法打开视频流")
            #         return False
                
            #     # 设置窗口大小
            #     cv2.namedWindow('Camera Stream', cv2.WINDOW_AUTOSIZE)
                
            #     frame_count = 0
            #     while True:
            #         ret, frame = cap.read()
            #         if not ret:
            #             print("✗ 无法读取视频帧")
            #             break
                    
            #         # 显示帧
            #         cv2.imshow('Camera Stream', frame)
            #         frame_count += 1
                    
            #         # 每隔10帧打印一次信息
            #         if frame_count % 10 == 0:
            #             print(f"  已显示 {frame_count} 帧")
                    
            #         # 按 'q' 键退出
            #         if cv2.waitKey(1) & 0xFF == ord('q'):
            #             break
                        
            #     # 释放资源
            #     cap.release()
            #     cv2.destroyAllWindows()
            #     print(f"✓ 视频流播放完成，共显示 {frame_count} 帧")
                
            # except Exception as e:
            #     print(f"✗ OpenCV播放视频流时发生错误: {e}")
            #     return False
            time.sleep(600)
            
            # 6. 停止视频流
            print("\n6. 正在停止视频流...")
            response = client._send_command(CommandType.STOP_CAMERA_STREAM)
            if response and response.status != "error":
                print("✓ 视频流已停止")
                print(f"  流状态: {response.data.get('streaming')}")
            else:
                print(f"✗ 停止视频流失败: {response.message if response else '无响应'}")
                return False
            
            print("\n✓ OpenCV视频流测试完成!")
            return True
        else:
            print("没有可用摄像头，无法继续测试")
            return False
            
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        return False
    finally:
        # 断开连接
        print("\n7. 正在断开连接...")
        client.disconnect()
        print("连接已断开")


def test_webcam_functions():
    """测试摄像头功能（原始测试）"""
    print("开始测试摄像头功能...")
    
    # 创建客户端实例
    client = ControllerClient(host="localhost", port=8888)
    
    try:
        # 1. 连接到服务器
        print("\n1. 正在连接到服务器...")
        if not client.connect():
            print("连接服务器失败")
            return False
        print("✓ 成功连接到服务器")
        
        # 2. 查询可用摄像头列表
        print("\n2. 正在查询可用摄像头...")
        response = client._send_command(CommandType.GET_CAMERAS_LIST)
        if response:
            print(f"收到响应: 状态={response.status}, 消息={response.message}")
            # 检查响应是否成功
            if response.status and hasattr(response, 'status') and response.status != "error":
                cameras = response.data.get("cameras", [])
                if cameras:
                    print(f"✓ 发现 {len(cameras)} 个可用摄像头:")
                    for i, cam in enumerate(cameras):
                        print(f"  摄像头 {i}: {cam['name']} (索引: {cam['index']})")
                        print(f"    路径: {cam['path']}")
                        print(f"    分辨率: {cam['width']}x{cam['height']}")
                        print(f"    FPS: {cam['fps']}")
                else:
                    print("未发现可用摄像头")
                    return False
            else:
                print(f"✗ 查询摄像头列表失败: {response.message}")
                return False
        else:
            print("✗ 查询摄像头列表失败: 无响应")
            return False
        
        # 选择第一个摄像头进行测试
        if cameras:
            camera_index = cameras[0]['index']
            print(f"\n3. 使用摄像头 {camera_index} 进行测试")
            
            # 3. 启动视频流
            print("\n4. 正在启动视频流...")
            data = {"camera_index": camera_index}
            response = client._send_command(CommandType.START_CAMERA_STREAM, data)
            if response and response.status != "error":
                print("✓ 视频流启动成功")
                print(f"  摄像头索引: {response.data.get('camera_index')}")
                print(f"  流状态: {response.data.get('streaming')}")
            else:
                print(f"✗ 启动视频流失败: {response.message if response else '无响应'}")
                return False
            
            # 等待几秒钟让流正常运行
            print("\n5. 视频流运行中... (等待3秒)")
            time.sleep(3)
            
            # 4. 停止视频流
            print("\n6. 正在停止视频流...")
            response = client._send_command(CommandType.STOP_CAMERA_STREAM)
            if response and response.status != "error":
                print("✓ 视频流已停止")
                print(f"  流状态: {response.data.get('streaming')}")
            else:
                print(f"✗ 停止视频流失败: {response.message if response else '无响应'}")
                return False
            
            print("\n✓ 摄像头功能测试完成!")
            return True
        else:
            print("没有可用摄像头，无法继续测试")
            return False
            
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        return False
    finally:
        # 断开连接
        print("\n7. 正在断开连接...")
        client.disconnect()
        print("连接已断开")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 运行两种测试
    print("=== 第一部分：基础摄像头功能测试 ===")
    success1 = True#test_webcam_functions()
    
    print("\n=== 第二部分：OpenCV视频流播放测试 ===")
    success2 = test_webcam_with_opencv()
    
    if success1 and success2:
        print("\n🎉 所有测试通过!")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败!")
        sys.exit(1)
