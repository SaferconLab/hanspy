#!/usr/bin/env python3
"""
RealSense控制器测试脚本
用于测试RealSense控制器的基本功能
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller_server.controller.realsense_controller import RealSenseController

def test_realsense_controller():
    """测试RealSense控制器"""
    print("开始测试RealSense控制器...")
    
    # 创建配置
    config = {
        "enable_depth": True,
        "enable_color": True,
        "depth_width": 640,
        "depth_height": 480,
        "color_width": 640,
        "color_height": 480,
        "depth_fps": 30,
        "color_fps": 30
    }
    
    # 创建控制器实例
    controller = RealSenseController(config)
    
    try:
        # 测试连接
        print("1. 测试连接...")
        if controller.connect():
            print("   连接成功")
        else:
            print("   连接失败")
            return
        
        # 测试是否连接
        print("2. 测试连接状态...")
        if controller.is_connected():
            print("   相机已连接")
        else:
            print("   相机未连接")
        
        # 测试获取深度帧
        print("3. 测试获取深度帧...")
        depth_frame = controller.get_depth_frame()
        if depth_frame is not None:
            print(f"   成功获取深度帧，形状: {depth_frame.shape}")
        else:
            print("   获取深度帧失败")
        
        # 测试获取彩色帧
        print("4. 测试获取彩色帧...")
        color_frame = controller.get_color_frame()
        if color_frame is not None:
            print(f"   成功获取彩色帧，形状: {color_frame.shape}")
        else:
            print("   获取彩色帧失败")
        
        # 测试获取点云
        print("5. 测试获取点云...")
        pointcloud_data = controller.get_pointcloud()
        if pointcloud_data is not None:
            verts, texcoords = pointcloud_data
            print(f"   成功获取点云，顶点数: {len(verts)}, 纹理坐标数: {len(texcoords)}")
        else:
            print("   获取点云失败")
        
        # 测试获取相机内参
        print("6. 测试获取相机内参...")
        intrinsics = controller.get_camera_intrinsics()
        if intrinsics is not None:
            print(f"   成功获取相机内参: {intrinsics}")
        else:
            print("   获取相机内参失败")
        
        # 测试获取帧元数据
        print("7. 测试获取帧元数据...")
        metadata = controller.get_frame_metadata()
        if metadata is not None:
            print(f"   成功获取帧元数据: {metadata}")
        else:
            print("   获取帧元数据失败")
        
        # 测试断开连接
        print("8. 测试断开连接...")
        if controller.disconnect():
            print("   断开连接成功")
        else:
            print("   断开连接失败")
        
        print("测试完成")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        # 确保即使出错也要断开连接
        try:
            controller.disconnect()
        except:
            pass

if __name__ == "__main__":
    test_realsense_controller()
