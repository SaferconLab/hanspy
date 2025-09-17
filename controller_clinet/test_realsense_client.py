#!/usr/bin/env python3
"""
RealSense客户端测试脚本
用于测试RealSense相机控制功能
"""

import sys
import os
import time
import numpy as np
import cv2

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from controller_clinet.client import ControllerClient

def test_realsense_client():
    """测试RealSense客户端功能"""
    print("开始测试RealSense客户端...")
    
    # 创建客户端实例
    client = ControllerClient(host="localhost", port=8888)
    
    try:
        # 连接到服务器
        print("1. 连接到服务器...")
        if client.connect():
            print("   连接成功")
        else:
            print("   连接失败")
            return
        
        # 测试连接RealSense相机
        print("2. 连接RealSense相机...")
        if client.connect_realsense():
            print("   RealSense相机连接成功")
        else:
            print("   RealSense相机连接失败")
            return
        
        # 测试获取深度帧
        print("3. 获取深度帧...")
        depth_frame = client.get_depth_frame()
        if depth_frame is not None:
            print(f"   成功获取深度帧，形状: {depth_frame.shape}")
            # 保存深度帧为图片用于验证
            cv2.imwrite("test_depth_frame.png", depth_frame)
            print("   深度帧已保存为 test_depth_frame.png")
        else:
            print("   获取深度帧失败")
        
        # 测试获取彩色帧
        print("4. 获取彩色帧...")
        color_frame = client.get_color_frame()
        if color_frame is not None:
            print(f"   成功获取彩色帧，形状: {color_frame.shape}")
            # 保存彩色帧为图片用于验证
            cv2.imwrite("test_color_frame.png", color_frame)
            print("   彩色帧已保存为 test_color_frame.png")
        else:
            print("   获取彩色帧失败")
        
        # 测试获取点云
        print("5. 获取点云数据...")
        pointcloud_data = client.get_pointcloud()
        if pointcloud_data is not None:
            verts, texcoords = pointcloud_data
            print(f"   成功获取点云，顶点数: {len(verts)}, 纹理坐标数: {len(texcoords)}")
        else:
            print("   获取点云失败")
        
        # 测试断开连接
        print("6. 断开RealSense相机连接...")
        if client.disconnect_realsense():
            print("   RealSense相机连接已断开")
        else:
            print("   断开RealSense相机连接失败")
        
        # 断开服务器连接
        print("7. 断开服务器连接...")
        if client.disconnect():
            print("   服务器连接已断开")
        else:
            print("   断开服务器连接失败")
        
        print("测试完成")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        # 确保即使出错也要断开连接
        try:
            client.disconnect_realsense()
            client.disconnect()
        except:
            pass

if __name__ == "__main__":
    test_realsense_client()
